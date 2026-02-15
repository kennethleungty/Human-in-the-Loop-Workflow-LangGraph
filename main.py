from langgraph.types import Command
from src.graph import graph
import json
import readline
from datetime import datetime


def prefill_input(prompt: str, prefill: str = "") -> str:
    """Input prompt with pre-filled text that user can edit"""
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def display_content_review(result: dict):
    """Display generated content for review"""
    post_data = json.loads(result["post_data"])
    print(f"\n📰 {post_data['title']}")
    print(f"🔗 {post_data['url']}")
    print(f"\n{post_data['post_content']}")
    return post_data


def get_content_decision(post_data: dict) -> bool | str:
    """Get user decision for content (approve/reject/edit)"""
    while True:
        user_input = input("\n(a)pprove | (r)eject | (e)dit: ").lower().strip()

        if user_input in ["a", "approve"]:
            return True
        elif user_input in ["r", "reject"]:
            return False
        elif user_input in ["e", "edit"]:
            edited_content = prefill_input("> ", post_data["post_content"]).strip()
            if edited_content:
                return edited_content
        else:
            print("Invalid input. Enter 'a', 'r', or 'e'.")


def handle_content_interrupt(result: dict, config: dict):
    """Handle content review interrupt"""
    post_data = display_content_review(result)
    decision = get_content_decision(post_data)
    return graph.invoke(Command(resume=decision), config=config)


def display_publish_confirmation(interrupt_value: dict):
    """Display post details for final publish confirmation"""
    print("\n✅ Ready to publish:")
    print(interrupt_value["post_content"])


def get_publish_decision() -> dict:
    """Get user decision (confirm/cancel) for publishing"""
    while True:
        user_input = input("\n(c)onfirm | (x) cancel: ").lower().strip()
        if user_input in ["c", "confirm"]:
            return {"action": "confirm"}
        elif user_input in ["x", "cancel"]:
            return {"action": "cancel"}
        else:
            print("Invalid input. Enter 'c' or 'x'.")


def handle_publish_interrupt(interrupt_value: dict, config: dict):
    """Handle publish confirmation interrupt"""
    display_publish_confirmation(interrupt_value)
    resume_data = get_publish_decision()
    return graph.invoke(Command(resume=resume_data), config=config)


def run_hitl_workflow():
    """Run the human-in-the-loop workflow with interrupts"""
    # Generate unique thread_id for each workflow run
    thread_id = f"workflow-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "messages": [],
        "search_results": "",
        "post_data": "",
        "status": "pending",
    }

    result = graph.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0]
        interrupt_value = (
            interrupt_data.value if hasattr(interrupt_data, "value") else interrupt_data
        )

        if interrupt_value["action"] == "review_content_generation":
            result = handle_content_interrupt(result, config)
        elif interrupt_value["action"] == "confirm_publish":
            result = handle_publish_interrupt(interrupt_value, config)
        else:
            raise ValueError(
                f"Unknown interrupt action: {interrupt_value.get('action')}"
            )


if __name__ == "__main__":
    run_hitl_workflow()
