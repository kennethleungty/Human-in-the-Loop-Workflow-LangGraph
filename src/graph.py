from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from src.state import State
from src.nodes import (
    web_search_node,
    content_generation_node,
    human_review_node,
    decision_approve_node,
    decision_reject_node,
)
from src.utils import save_mermaid_diagram

import sqlite3


def create_workflow_graph():
    builder = StateGraph(State)

    builder.add_node("web_search", web_search_node)
    builder.add_node("content_creation", content_generation_node)
    builder.add_node("review", human_review_node)
    builder.add_node("approve", decision_approve_node)
    builder.add_node("reject", decision_reject_node)

    # Only START edge needed — all nodes use Command(goto=...) for routing
    builder.add_edge(START, "web_search")

    # check_same_thread=False is needed because LangGraph internally uses a
    # thread pool for checkpoint writes, which differs from the thread that
    # created the connection. The docs example omits this but it's required
    # in newer LangGraph versions that parallelize checkpointer operations.
    # checkpointer = InMemorySaver()
    checkpointer = SqliteSaver(sqlite3.connect("hitl_workflow.db", check_same_thread=False))

    compiled_graph = builder.compile(checkpointer=checkpointer)

    save_mermaid_diagram(compiled_graph, output_path="assets/graph_setup.png")
    return compiled_graph


graph = create_workflow_graph()
