from typing import Literal
from src.state import State
from src.tools import tavily_search
from langgraph.types import Command


def web_search_node(state: State) -> Command[Literal["content_creation"]]:
    """Node that performs web search using the Tavily search tool."""
    query = "latest top news about OpenAI"

    # Call the tool — pure search, no interrupt here
    search_results = tavily_search.invoke({"query": query})

    return Command(
        update={**state, "search_results": search_results, "status": "pending"},
        goto="content_creation",
    )
