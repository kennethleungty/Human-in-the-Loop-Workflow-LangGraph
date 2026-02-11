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


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add project root to path for direct execution
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    print("Testing approval_node...")
    print("=" * 60)
    print(
        "Note: This node uses interrupt() which requires running in a LangGraph workflow."
    )
    print("It cannot be tested standalone. Run via main.py instead.")
    print("=" * 60)
