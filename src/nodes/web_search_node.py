from typing import Literal
from src.state import State
from src.tools import tavily_search
from langgraph.types import Command


def web_search_node(state: State) -> Command[Literal["content_creation"]]:
    """Perform web search using the Tavily tool."""
    search_results = tavily_search.invoke({"query": state["query"]})

    return Command(
        update={**state, "search_results": search_results, "status": "pending"},
        goto="content_creation",
    )
