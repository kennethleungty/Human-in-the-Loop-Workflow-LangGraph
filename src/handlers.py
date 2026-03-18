from langgraph.types import Command
from src.graph import graph
import json
import readline


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
