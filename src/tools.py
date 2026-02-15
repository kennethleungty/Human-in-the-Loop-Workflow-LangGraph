from langchain_core.tools import tool
from langgraph.types import interrupt
from tavily import TavilyClient
import os
import json


@tool
def tavily_search(query: str) -> str:
    """Search for latest news articles using Tavily API."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    search_response = tavily_client.search(
        query=query,
        max_results=1,
        topic="news",
        search_depth="advanced",
        include_answer=False,
        include_raw_content=False,
        include_images=False,
    )

    result = search_response["results"][0] if search_response["results"] else {}

    return json.dumps(
        {
            "query": query,
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "published_date": result.get("published_date", ""),
            "content": result.get("content", ""),
        }
    )


@tool
def publish_post(post_content: str, title: str, url: str) -> str:
    """Publish a post to X. Interrupts for human confirmation before executing."""
    # Interrupt BEFORE the side effect — safe on re-execution
    response = interrupt(
        {
            "action": "confirm_publish",
            "post_content": post_content,
            "title": title,
            "url": url,
        }
    )

    if response.get("action") == "confirm":
        # Mock publish — replace with actual X/Twitter API call
        return "Post successfully posted on X"

    return "Post publishing cancelled by user"
