from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import State
from src.nodes import (
    web_search_node,
    content_creation_node,
    review_node,
    approve_node,
    reject_node,
)
from src.utils import save_mermaid_diagram


def create_workflow_graph():
    """Create and compile the LangGraph workflow with checkpointer"""
    # Build the graph
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("web_search", web_search_node)
    builder.add_node("content_creation", content_creation_node)
    builder.add_node("review", review_node)
    builder.add_node("approve", approve_node)
    builder.add_node("reject", reject_node)

    # Define edges
    builder.add_edge(START, "web_search")
    builder.add_edge("web_search", "content_creation")
    builder.add_edge("content_creation", "review")
    # review_node returns Command with goto, so no edge needed from review
    builder.add_edge("approve", END)
    builder.add_edge("reject", END)

    # Compile with checkpointer for interrupt support
    checkpointer = MemorySaver()
    compiled_graph = builder.compile(checkpointer=checkpointer)

    # Save Mermaid diagram
    save_mermaid_diagram(compiled_graph, output_path="assets/graph_setup.png")

    return compiled_graph


def create_thread_config(thread_id: str):
    """Create thread configuration for workflow execution"""
    return {"configurable": {"thread_id": thread_id}}


# Create the compiled graph instance
graph = create_workflow_graph()
