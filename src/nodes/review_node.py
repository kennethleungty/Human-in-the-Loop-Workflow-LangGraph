from typing import Literal
from langgraph.types import Command, interrupt
from src.state import State
import json


def review_node(state: State) -> Command[Literal["approve", "reject"]]:
    """Node that pauses for human review with edit capability"""
    # Expose details so the caller can render them in a UI
    decision = interrupt(
        {
            "question": "Approve, reject, or edit this post?",
            "details": state["action_details"],
        }
    )

    # Handle three cases: True (approve), False (reject), or string (edited content)
    if isinstance(decision, str):
        # User provided edited content - update action_details and auto-approve
        action_details = json.loads(state["action_details"])
        action_details["post_content"] = decision
        updated_action_details = json.dumps(action_details, indent=2)

        return Command(
            goto="approve", update={"action_details": updated_action_details}
        )
    elif decision is True:
        # Approved - proceed to approve node
        return Command(goto="approve")
    else:
        # Rejected - go to reject node
        return Command(goto="reject")
