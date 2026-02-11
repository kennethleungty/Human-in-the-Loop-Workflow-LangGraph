from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import State
from src.nodes import (
    web_search_node,
    content_creation_node,
    approval_node,
    write_to_db_node,
    cancel_node,
)


# Build the graph
builder = StateGraph(State)

# Add nodes
builder.add_node("web_search", web_search_node)
builder.add_node("content_creation", content_creation_node)
builder.add_node("approval", approval_node)
builder.add_node("write_to_db", write_to_db_node)
builder.add_node("cancel", cancel_node)

# Define edges
builder.add_edge(START, "web_search")
builder.add_edge("web_search", "content_creation")
builder.add_edge("content_creation", "approval")
# approval_node returns Command with goto, so no edge needed from approval
builder.add_edge("write_to_db", END)
builder.add_edge("cancel", END)

# Use a more durable checkpointer in production
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
