from typing import TypedDict, Optional, Literal


class State(TypedDict):
    """State definition for the workflow"""

    search_results: str
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]
