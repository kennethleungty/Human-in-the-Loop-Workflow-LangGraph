"""
Tools module for the workflow.

Contains reusable tools that can be called from nodes.

- tavily_search: Pure search tool (no interrupt).
- publish_post: Tool with interrupt BEFORE the side effect (like send_email
  in the LangGraph docs). Safe because inputs are deterministic and the
  action only executes after approval.
"""

from langchain_core.tools import tool
from langgraph.types import interrupt
from tavily import TavilyClient
import os
import json


@tool
def tavily_search(query: str) -> str:
    """
    Search for latest news articles using Tavily API.
    Use this tool to find current news and information.

    Args:
        query: Search query string (e.g., "latest news about OpenAI")

    Returns:
        JSON string containing search results with title, url, published_date, and content
    """
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

    # Extract and format results
    result = search_response["results"][0] if search_response["results"] else {}

    formatted_results = {
        "query": query,
        "title": result.get("title", ""),
        "url": result.get("url", ""),
        "published_date": result.get("published_date", ""),
        "content": result.get("content", ""),
    }

    return json.dumps(formatted_results)


@tool
def publish_post(post_content: str, title: str, url: str) -> str:
    """Publish a post to X (Twitter).

    Pauses for final human confirmation before publishing.
    This follows the interrupt-before-action pattern: the interrupt
    gates the side effect, so re-execution on resume is safe.

    Args:
        post_content: The post text to publish
        title: The article title (for reference)
        url: The article URL (for reference)

    Returns:
        Confirmation message or cancellation notice
    """
    # Pause BEFORE publishing; payload surfaces in result["__interrupt__"]
    response = interrupt(
        {
            "action": "confirm_publish",
            "post_content": post_content,
            "title": title,
            "url": url,
            "message": "Ready to publish this post to X. Confirm?",
        }
    )

    if response.get("action") == "confirm":
        response.get("post_content", post_content)
        # Mock publish — replace with actual X/Twitter API call
        return "✓ Post successfully posted on X"

    return "Post publishing cancelled by user"
