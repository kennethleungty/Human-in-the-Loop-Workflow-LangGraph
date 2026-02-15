from src.state import State
from langgraph.types import Command
from langgraph.graph import END


def decision_reject_node(state: State) -> Command:
    """Handle rejection — mark status and end."""
    return Command(update={**state, "status": "rejected"}, goto=END)
