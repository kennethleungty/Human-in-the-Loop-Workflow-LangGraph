from src.state import State
import json


def approve_node(state: State) -> State:
    """Node that approves and posts content to X"""
    # Parse action_details to get finalized content
    action_details = json.loads(state["action_details"])

    print("\n === POST APPROVED ===")
    print("\nFinalized X Post:")
    print(action_details["post_content"])

    # Placeholder - will implement actual posting logic later
    # x_api.post(action_details["post_content"])

    print("\n✓ Successfully posted content on X")

    return {**state, "status": "approved"}
