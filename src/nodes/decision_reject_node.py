from src.state import State
from langgraph.types import Command
from langgraph.graph import END


def decision_reject_node(state: State) -> Command:
    """Node that handles rejection"""
    print("\n=== POST REJECTED ===")
    print("Content NOT posted to X")

    return Command(update={**state, "status": "rejected"}, goto=END)
