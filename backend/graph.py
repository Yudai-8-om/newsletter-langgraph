import json
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from tools import fetch_news_api
from state import AgentState
from prompts import writer_system_prompt
from settings import settings
from langgraph.prebuilt import create_react_agent
from db import get_pg_async_session
from models import Newsletter
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
        # raise ValueError("Failed to parse JSON response from the model. Please check the model's output format.")    
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

def generate_query(state: AgentState) -> AgentState:
    """
    Langgraph node that generates query
    """
    chat_ollama = ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.LLM_MODEL_LIGHT, 
        )
    user_message = HumanMessage(content=f"Hello, what is {state.topic}?")
    result = chat_ollama.invoke([user_message])
    state.final_output = result.content
    return state

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
        Create a payment link for a new product called 'test' with a price
        of $1.
    """,
    }
    state.billing_result = langgraph_agent_executor.invoke(input_state)
    state.subscribed = True
    state.topic = "Stripe"
    return state

builder = StateGraph(AgentState)
builder.add_node("charge_subscription_fee", charge_subscription_fee)
builder.add_node("generate_newsletter", generate_newsletter)
builder.add_node("list_trending_news", list_trending_news)
builder.add_node("save_newsletter", save_newsletter)

builder.add_edge(START, "list_trending_news")
builder.add_edge("list_trending_news", "generate_newsletter")
builder.add_edge("generate_newsletter", "save_newsletter")
builder.add_edge("save_newsletter", END)
graph = builder.compile()

def build_curation_agent():
    """
    Build the Langgraph agent for newsletter generation
    """
    return graph