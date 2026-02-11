from typing import Literal
from langgraph.types import Command, interrupt
from src.state import State


def approval_node(state: State) -> Command[Literal["write_to_db", "cancel"]]:
    """Node that pauses for human approval"""
    # Expose details so the caller can render them in a UI
    decision = interrupt(
        {
            "question": "Approve this action?",
            "details": state["action_details"],
        }
    )

    # Route to the appropriate node after resume
    return Command(goto="write_to_db" if decision else "cancel")
