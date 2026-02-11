from src.state import State


def write_to_db_node(state: State) -> State:
    """Node that writes data to database after approval"""
    # Placeholder - will implement actual DB logic later

    return {**state, "status": "approved"}
