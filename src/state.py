from typing import TypedDict, Optional, Literal


class State(TypedDict):
    search_results: str
    post_data: str
    status: Optional[Literal["pending", "approved", "rejected"]]
