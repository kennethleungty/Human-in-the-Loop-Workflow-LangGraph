from typing import TypedDict, Optional, Literal


class State(TypedDict):
    query: str
    search_results: str
    post_data: str
    status: Optional[Literal["pending", "approved", "rejected", "cancelled"]]
