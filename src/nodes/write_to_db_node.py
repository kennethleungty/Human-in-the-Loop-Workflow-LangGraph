from src.state import State


def write_to_db_node(state: State) -> State:
    """Node that writes data to database after approval"""
    # Placeholder - will implement actual DB logic later

    return {**state, "status": "approved"}


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add project root to path for direct execution
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    import json

    print("Testing write_to_db_node...")
    print("=" * 60)

    test_action_details = json.dumps(
        {
            "post_content": "Sample X post about OpenAI news",
            "raw_content": "Full article content...",
            "title": "OpenAI Announcement",
            "url": "https://example.com/article",
            "published_date": "2024-02-11",
        }
    )

    test_state: State = {
        "search_results": "{}",
        "action_details": test_action_details,
        "status": "pending",
    }

    result = write_to_db_node(test_state)

    print("\nResult:")
    print(f"Status: {result['status']}")
    print("\nAction Details:")
    print(result["action_details"])
