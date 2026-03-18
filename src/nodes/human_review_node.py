from typing import Literal
from langgraph.types import Command, interrupt
from src.state import State
import json


def human_review_node(state: State) -> Command[Literal["approve", "reject"]]:
    """Pause for human review. Interrupt surfaces post details to the caller."""
    decision = interrupt(
        {
            "action": "handle_content_interrupt",
            "details": state["post_data"],
        }
    )

    # True = approve, False = reject, str = edited content (auto-approve)
    if isinstance(decision, str):
        post_data = json.loads(state["post_data"])
        post_data["post_content"] = decision
        return Command(goto="approve", update={"post_data": json.dumps(post_data)})
    elif decision is True:
        return Command(goto="approve")
    else:
        return Command(goto="reject")
