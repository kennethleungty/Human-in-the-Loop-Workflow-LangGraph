from typing import Literal
from langgraph.types import Command, interrupt
from src.state import State
import json


def human_review_node(state: State) -> Command[Literal["approve", "reject"]]:
    """Node that pauses for human review with edit capability"""
    # Expose details so the caller can render them in a UI
    decision = interrupt(
        {
            "action": "review_content_generation",
            "question": "Approve, reject, or edit this post?",
            "details": state["post_data"],
        }
    )

    # Handle three cases: True (approve), False (reject), or string (edited content)
    if isinstance(decision, str):
        # User provided edited content - update post_data and auto-approve
        post_data = json.loads(state["post_data"])
        post_data["post_content"] = decision
        updated_post_data = json.dumps(post_data, indent=2)

        return Command(goto="approve", update={"post_data": updated_post_data})
    elif decision is True:
        # Approved - proceed to approve node
        return Command(goto="approve")
    else:
        # Rejected - go to reject node
        return Command(goto="reject")
