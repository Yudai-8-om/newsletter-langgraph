from backend.graph import build_curation_agent
import asyncio

async def run_newsletter_agent():
    """
    Run the newsletter generation agent
    """
    newsletter_agent_graph = build_curation_agent()
    await newsletter_agent_graph.ainvoke({})

if __name__ == "__main__":
    asyncio.run(run_newsletter_agent())