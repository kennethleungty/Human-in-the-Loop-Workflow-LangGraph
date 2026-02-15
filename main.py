from langgraph.types import Command
from src.graph import graph
import json
import readline
from datetime import datetime


def prefill_input(prompt: str, prefill: str = "") -> str:
    """Input prompt pre-filled with editable text."""
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def handle_content_interrupt(result: dict, config: dict):
    """Display generated post and get approve/reject/edit decision."""
    post_data = json.loads(result["post_data"])
    print(f"\n{post_data['title']}")
    print(f"{post_data['url']}")
    print(f"\n{post_data['post_content']}")

    while True:
        choice = input("\n(a)pprove | (r)eject | (e)dit: ").lower().strip()
        if choice in ["a", "approve"]:
            # Resume via Command. Note that the resume value does not have a required format.
            # It's just whatever we want interrupt() to return inside the node/tool.
            return graph.invoke(Command(resume=True), config=config)
        elif choice in ["r", "reject"]:
            return graph.invoke(Command(resume=False), config=config)
        elif choice in ["e", "edit"]:
            edited = prefill_input("> ", post_data["post_content"]).strip()
            if edited:
                return graph.invoke(Command(resume=edited), config=config)
        else:
            print("Invalid input. Enter 'a', 'r', or 'e'.")


def handle_publish_interrupt(interrupt_value: dict, config: dict):
    """Show final post and get confirm/cancel decision."""
    print(f"\nReady to publish on Bluesky:\n{interrupt_value['post_content']}")

    while True:
        choice = input("\n(c)onfirm | (x) cancel: ").lower().strip()
        if choice in ["c", "confirm"]:
            return graph.invoke(Command(resume={"action": "confirm"}), config=config)
        elif choice in ["x", "cancel"]:
            return graph.invoke(Command(resume={"action": "cancel"}), config=config)
        else:
            print("Invalid input. Enter 'c' or 'x'.")


def run_hitl_workflow(query: str):
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
        # Get interrupt value at point of interrupt
        interrupt_value = result["__interrupt__"][0].value
        
        # Get action at point of interrupt
        action = interrupt_value["action"]

        if action == "review_content_generation":
            result = handle_content_interrupt(result, config)
        elif action == "confirm_publish":
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
