from typing import TypedDict, Optional, Literal
from typing_extensions import Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    """State definition for the workflow"""

    messages: Annotated[list, add_messages]  # For agent communication
    search_results: str
    post_data: str  # JSON string containing post content, title, url, published_date
    status: Optional[Literal["pending", "approved", "rejected"]]
