from src.state import State
from src.prompts import X_POST_PROMPT
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

    # Format the prompt with article data
    prompt = X_POST_PROMPT.format(
        title=search_data.get("title", "N/A"),
        url=search_data.get("url", "N/A"),
        published_date=search_data.get("published_date", "N/A"),
        content=search_data.get("content", "N/A"),
    )

    # Generate X post using OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a sharp tech commentator for X (Twitter).",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=300,
    )

    post_content = response.choices[0].message.content.strip()

    # Create action_details JSON with post and article metadata
    action_details = json.dumps(
        {
            "post_content": post_content,
            "raw_content": search_data.get("raw_content", ""),
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
    print("Testing content_creation_node...")
    print("=" * 60)

    sample_search_results = json.dumps(
        {
            "query": "latest top news about openAI",
            "title": "OpenAI Announces GPT-5",
            "url": "https://example.com/gpt5-announcement",
            "published_date": "2024-02-11",
            "content": "OpenAI has announced GPT-5, the next generation of their language model with significant improvements in multimodal capabilities.",
            "raw_content": "Full article content here...",
            "score": 0.95,
            "answer": "OpenAI announced GPT-5 with enhanced capabilities.",
            "images": [],
            "response_time": 1.2,
        }
    )

    test_state: State = {
        "search_results": sample_search_results,
        "action_details": "",
        "status": "pending",
    }

    result = content_creation_node(test_state)

    print("\nGenerated Action Details:")
    action_data = json.loads(result["action_details"])
    print("\nX Post Content:")
    print(action_data["post_content"])
    print("\n" + "=" * 60)
    print("Full Action Details JSON:")
    print(result["action_details"])
