from src.graph import graph
from src.handlers import handle_content_interrupt, handle_publish_interrupt
from datetime import datetime


def run_hitl_workflow(query: str):
    """
    Runs the HITL workflow for a given query.
    """
    thread_id = f"workflow-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "query": query,
        "search_results": "",
        "post_data": "",
        "status": "pending",
    }

    result = graph.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        interrupt_value = result["__interrupt__"][0].value
        action = interrupt_value["action"]

        if action == "handle_content_interrupt":
            result = handle_content_interrupt(result, config)
        elif action == "handle_publish_interrupt":
            result = handle_publish_interrupt(interrupt_value, config)
        else:
            raise ValueError(f"Unknown interrupt action: {action}")

    if result.get("status") == "approved":
        print("\nPost successfully published on Bluesky")
    elif result.get("status") == "cancelled":
        print("\nPublishing cancelled — not posted")
    elif result.get("status") == "rejected":
        print("\nPost rejected — not published")


if __name__ == "__main__":
    run_hitl_workflow(query="latest top news about Anthropic")
