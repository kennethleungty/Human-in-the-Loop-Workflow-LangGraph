from src.state import State


def cancel_node(state: State) -> State:
    """Node that handles cancellation"""
    return {**state, "status": "rejected"}
