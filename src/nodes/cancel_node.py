from src.state import State


def cancel_node(state: State) -> State:
    """Node that handles cancellation"""
    return {**state, "status": "rejected"}


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add project root to path for direct execution
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    print("Testing cancel_node...")
    print("=" * 60)

    test_state: State = {
        "search_results": "{}",
        "action_details": "{}",
        "status": "pending",
    }

    result = cancel_node(test_state)

    print("\nResult:")
    print(f"Status: {result['status']}")
    print("Action cancelled successfully.")
