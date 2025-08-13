import json
import asyncio
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from backend.tools import fetch_news_api, send_email
from backend.state import AgentState
from backend.prompts import writer_system_prompt, marketer_non_sub_system_prompt, marketer_sub_system_prompt, validator_system_prompt
from backend.settings import settings
from langgraph.prebuilt import create_react_agent
from backend.db import get_pg_async_session
from backend.models import Newsletter, User
from sqlalchemy import select
from stripe_agent_toolkit.langchain.toolkit import StripeAgentToolkit


def list_trending_news(state: AgentState) -> AgentState:
    """
    Langgraph node that finds trending news 
    """
    response = fetch_news_api(state.country)
    state.trending_news = response["trending_news"]
    return state

def generate_newsletter(state: AgentState) -> AgentState:
    """
    Langgraph node that generates newsletter
    """
    # If you use local Ollama, uncomment this
    # chat_ollama = ChatOllama(
    #     base_url=settings.OLLAMA_BASE_URL, 
    #     model=settings.LLM_MODEL_LIGHT, 
    #     num_ctx=4096,
    #     format="json"
    #     )
    chat_openai = ChatOpenAI(
        model=settings.OPENROUTER_MODEL, 
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    news_str = "\n".join(f"<trending_news> Title: {news['title']} \nContent: {news['content']}</trending_news>" for news in state.trending_news[:3])
    print(f"passed news: {news_str}")
    user_message = [SystemMessage(content=writer_system_prompt.format(news=news_str)), HumanMessage(content="Using the given trending news, write a newsletter")]
    result = chat_openai.invoke(user_message)
    try:
        result_json = json.loads(result.content)
        state.newsletter_title = result_json["Title"]
        state.newsletter_content = result_json["Content"]
    except (json.JSONDecodeError, KeyError):
        state.newsletter_title = "Today's Newsletter"
        state.newsletter_content = result.content
    return state

def fix_json(state: AgentState) -> AgentState:
    if state.newsletter_title == "Today's Newsletter":
        print("Fixing Json")
        chat_openai = ChatOpenAI(
            model=settings.OPENROUTER_MODEL, 
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
        )
        user_message = [SystemMessage(content=validator_system_prompt.format(news_content=state.newsletter_content)), HumanMessage(content="Fix the malformated Json and return in proper Json format.")]
        result = chat_openai.invoke(user_message)
        try:
            result_json = json.loads(result.content)
            state.newsletter_title = result_json["Title"]
            state.newsletter_content = result_json["Content"]
        except (json.JSONDecodeError, KeyError):
            state.newsletter_title = "Today's Newsletter (Sorry for the broken newsletter body😣)"
            state.newsletter_content = result.content
    return state


async def save_newsletter(state: AgentState) -> AgentState:
    """
    Langgraph node that saves newsletter to the database
    """
    async with get_pg_async_session() as session:
        new_newsletter = Newsletter(
            title=state.newsletter_title,
            content=state.newsletter_content
        )
        session.add(new_newsletter)
        await session.commit()
        await session.refresh(new_newsletter)
    return state


def generate_email_for_sub(state: AgentState) -> AgentState:
    """
    Langgraph node that generates a promotion email for subscriber
    """
    state.agent_type = "marketing"
    # If you use local Ollama, uncomment this
    # chat_ollama = ChatOllama(
    #     base_url=settings.OLLAMA_BASE_URL, 
    #     model=settings.LLM_MODEL_LIGHT, 
    #     num_ctx=4096,
    #     format="json"
    #     )
    chat_openai = ChatOpenAI(
        model=settings.OPENROUTER_MODEL, 
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    user_message = [SystemMessage(content=marketer_non_sub_system_prompt.format(newsletter=state.newsletter_content)), HumanMessage(content="Using the generated newsletter, write a email for our subscribers.")]
    result = chat_openai.invoke(user_message)
    try:
        result_json = json.loads(result.content)
        state.email_sub_subject = result_json["Subject"]
        state.email_sub_body = result_json["HTML"]
    except (json.JSONDecodeError, KeyError):
        state.email_sub_subject = "Thank you for reading our newsletter💌"
        state.email_sub_body = result.content
    return state

def generate_email_for_non_sub(state: AgentState) -> AgentState:
    """
    Langgraph node that generates an email for non subscriber
    """
    # If you use local Ollama, uncomment this
    # chat_ollama = ChatOllama(
    #     base_url=settings.OLLAMA_BASE_URL, 
    #     model=settings.LLM_MODEL_LIGHT, 
    #     num_ctx=4096,
    #     format="json"
    #     )
    chat_openai = ChatOpenAI(
        model=settings.OPENROUTER_MODEL, 
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    user_message = [SystemMessage(content=marketer_non_sub_system_prompt.format(newsletter=state.newsletter_content)), HumanMessage(content="Using the generated newsletter, write a promotion email for our non-subscribers.")]
    result = chat_openai.invoke(user_message)
    try:
        result_json = json.loads(result.content)
        state.email_non_sub_subject = result_json["Subject"]
        state.email_non_sub_body = result_json["HTML"]
    except (json.JSONDecodeError, KeyError):
        state.email_non_sub_subject = "Join our newsletter family🔥"
        state.email_non_sub_body = result.content
    return state

async def send_email_to_users(state: AgentState) -> AgentState:
    """
    Langgraph node that sends daily email
    """
    async with get_pg_async_session() as session:
        result = await session.execute(select(User.email, User.is_subscribed))
        all_users = result.all()
    for email, subscribed in all_users:
        if subscribed:
            await asyncio.to_thread(send_email, email, state.email_sub_subject, state.email_sub_body)
        else: 
            await asyncio.to_thread(send_email, email, state.email_non_sub_subject, state.email_non_sub_body)
        print(email, subscribed)
    return state


#Unused node, generated just for tool calling
def charge_subscription_fee(state: AgentState) -> AgentState:
    """
    Langgraph node that charges monthly subscription fee, $1/month
    """
    chat_ollama = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL, 
            model=settings.LLM_MODEL, 
        )
    stripe_agent_toolkit = StripeAgentToolkit(
        secret_key=settings.STRIPE_SECRET_KEY,
        configuration={
            "actions": {
                "payment_links": {
                    "create": True,
                },
                "products": {
                    "create": True,
                    },
                "prices": {
                    "create": True,
                    },
                }
            },
        )
    tools = stripe_agent_toolkit.get_tools()
    langgraph_agent_executor = create_react_agent(chat_ollama, tools)
    input_state = {
    "messages": """
        Create a payment link for a new product called 'Newsletter Subscription' with a price
        of $1.
    """,
    }
    state.billing_result = langgraph_agent_executor.invoke(input_state)
    state.subscribed = True
    return state

builder = StateGraph(AgentState)
builder.add_node("charge_subscription_fee", charge_subscription_fee)
builder.add_node("generate_newsletter", generate_newsletter)
builder.add_node("list_trending_news", list_trending_news)
builder.add_node("fix_json", fix_json)
builder.add_node("save_newsletter", save_newsletter)
builder.add_node("generate_email_for_sub", generate_email_for_sub)
builder.add_node("generate_email_for_non_sub", generate_email_for_non_sub)
builder.add_node("send_email_to_users", send_email_to_users)

builder.add_edge(START, "list_trending_news")
builder.add_edge("list_trending_news", "generate_newsletter")
builder.add_edge("generate_newsletter", "fix_json")
builder.add_edge("fix_json", "save_newsletter")
builder.add_edge("save_newsletter", "generate_email_for_sub")
builder.add_edge("generate_email_for_sub", "generate_email_for_non_sub")
builder.add_edge("generate_email_for_non_sub", "send_email_to_users")
builder.add_edge("send_email_to_users", END)
graph = builder.compile()

def build_curation_agent():
    """
    Build the Langgraph agent for newsletter generation and marketing
    """
    return graph