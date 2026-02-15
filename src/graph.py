from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from src.state import State
from src.nodes import (
    web_search_node,
    content_generation_node,
    human_review_node,
    decision_approve_node,
    decision_reject_node,
)
from src.utils import save_mermaid_diagram


def create_workflow_graph():
    """Create and compile the LangGraph workflow with checkpointer"""
    # Build the graph
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("web_search", web_search_node)
    builder.add_node("content_creation", content_generation_node)
    builder.add_node("review", human_review_node)
    builder.add_node("approve", decision_approve_node)
    builder.add_node("reject", decision_reject_node)

    # Define edges
    # Only START edge needed - all nodes use Command with goto for routing
    builder.add_edge(START, "web_search")

    # Compile with checkpointer for interrupt support
    # InMemorySaver: Fast, data cleared on process restart
    # SqliteSaver: Persistent across restarts, useful for resuming interrupted workflows
    checkpointer = InMemorySaver()
    # checkpointer = SqliteSaver(sqlite3.connect("approval.db"))
    compiled_graph = builder.compile(checkpointer=checkpointer)

    # Save Mermaid diagram
    save_mermaid_diagram(compiled_graph, output_path="assets/graph_setup.png")

    return compiled_graph


# Create the compiled graph instance
# This checkpointer persists for the lifetime of the Python process
# Each workflow run uses a unique thread_id to avoid state collision
graph = create_workflow_graph()
