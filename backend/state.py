"""
state.py

Defines states shared between agents as well as the input and output types for the agents.
"""

from pydantic import BaseModel
from typing import Deque, List, Optional, Tuple, Dict

class AgentState(BaseModel):
    """Internal state shared between agents in the graph."""
    interests: Optional[List[str]] = None
    country: str = "US"
    agent_type: str = "curation"
    trending_news: Optional[List[Dict[str, str]]] = None
    sources_used: Optional[List[str]] = None
    is_subscribed: Optional[bool] = None
    payment_status: Optional[str] = None
    newsletter_title: Optional[str] = None
    newsletter_content: Optional[str] = None