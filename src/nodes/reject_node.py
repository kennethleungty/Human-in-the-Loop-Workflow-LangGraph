from src.state import State


def reject_node(state: State) -> State:
    """Node that handles rejection"""
    print("\n=== POST REJECTED ===")
    print("Content NOT posted to X")

    return {**state, "status": "rejected"}
