from src.state import State
from tavily import TavilyClient
import os
import json


def web_search_node(state: State) -> State:
    """Node that performs web search using Tavily"""
    query = "latest top news about openAI"

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not set")

    tavily_client = TavilyClient(api_key=api_key)

    # Perform search with comprehensive parameters
    response = tavily_client.search(
        query=query,
        max_results=1,
        topic="news",  # Use news topic for latest news
        search_depth="advanced",  # Get more detailed content
        include_answer=False,  # Include LLM-generated answer
        include_raw_content=False,  # Include full cleaned HTML content
        include_images=False,  # Include related images
    )

    # Extract single result (max_results=1)
    result = response["results"][0] if response["results"] else {}

    # Format search results as a structured string for next node
    search_results = json.dumps(
        {
            # "query": query,
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "published_date": result.get("published_date", ""),
            "content": result.get("content", ""),
            # "answer": response.get('answer', ''),
            # "raw_content": result.get('raw_content', ''),
            # "score": result.get('score', 0),
            # "images": response.get('images', []),
            # "response_time": response.get('response_time', 0)
        },
        indent=2,
    )

    return {**state, "search_results": search_results, "status": "pending"}


# For testing
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add project root to path for direct execution
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    # Test the node
    print("Running web_search_node...")
    print("=" * 60)

    init_state: State = {
        "search_results": "",
        "action_details": "",
        "status": "pending",
    }
    result = web_search_node(init_state)

    print("\nSearch Results:")
    print(result["search_results"])
