from src.state import State
from src.prompts import X_POST_INSTRUCTIONS
from config import LLM_MODEL, TEMPERATURE
from openai import OpenAI
import os
import json


def content_creation_node(state: State) -> State:
    """Node that generates X (Twitter) post from search results using OpenAI"""

    # Parse the search results JSON
    search_data = json.loads(state["search_results"])

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    # Combine instructions and article data into single input
    input_text = f"""{X_POST_INSTRUCTIONS}

    Article Information:

    Title: {search_data.get('title', 'N/A')}
    URL: {search_data.get('url', 'N/A')}
    Published Date: {search_data.get('published_date', 'N/A')}

    Article Content:
    {search_data.get('content', 'N/A')}
    """

    # Generate X post using OpenAI Responses API
    response = client.responses.create(
        model=LLM_MODEL,
        input=input_text,
        temperature=TEMPERATURE,
    )

    # Extract text content from response output
    post_content = response.output_text

    # Create action_details JSON with post and article metadata
    action_details = json.dumps(
        {
            "post_content": post_content,
            "title": search_data.get("title", ""),
            "url": search_data.get("url", ""),
            "published_date": search_data.get("published_date", ""),
        },
        indent=2,
    )

    return {**state, "action_details": action_details, "status": "pending"}


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add project root to path for direct execution
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    # Test the node with sample search results
    print("Running content_creation_node...")
    print("=" * 60)

    sample_search_results = json.dumps(
        {
            "title": "OpenAI Announces GPT-5",
            "url": "https://example.com/gpt5-announcement",
            "published_date": "2024-02-11",
            "content": "OpenAI has announced GPT-5, the next generation of their language model with significant improvements in multimodal capabilities.",
        }
    )

    init_state: State = {
        "search_results": sample_search_results,
        "action_details": "",
        "status": "pending",
    }

    result = content_creation_node(init_state)

    print("\nGenerated Action Details:")
    action_data = json.loads(result["action_details"])
    print("\nX Post Content:")
    print(action_data["post_content"])
