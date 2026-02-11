from langgraph.types import Command
from src.graph import graph, create_thread_config
import json
import readline


def main():
    """Example usage of the workflow with interrupts"""

    # Configuration with thread_id for checkpointing
    config = create_thread_config("workflow-001")

    # Initial state
    initial_state = {"search_results": "", "action_details": "", "status": "pending"}

    # Step 1: Start the workflow - it will run until the interrupt
    print("\nStarting workflow...\n")
    result = graph.invoke(initial_state, config=config)

    # The workflow pauses at the review_node interrupt
    # Loop to handle edit cycles
    while "__interrupt__" in result:
        print("\nWORKFLOW PAUSED - REVIEW REQUIRED")

        # Parse and display the action_details
        action_details = json.loads(result["action_details"])

        print("\nArticle Details:")
        print(f"Title: {action_details['title']}")
        print(f"URL: {action_details['url']}")
        print(f"Published: {action_details['published_date']}")

        print("\nGenerated X Post:")
        print(action_details["post_content"])

        # Step 2: Get user decision (approve/reject/edit)
        while True:
            user_input = (
                input("Choose action - (a)pprove, (r)eject, or (e)dit: ")
                .lower()
                .strip()
            )
            if user_input in ["a", "approve"]:
                decision = True
                break
            elif user_input in ["r", "reject"]:
                decision = False
                break
            elif user_input in ["e", "edit"]:
                print("\nEdit the post content (pre-filled with current content):")

                # Pre-fill input with existing content using readline
                def prefill_input(prompt, prefill=""):
                    readline.set_startup_hook(lambda: readline.insert_text(prefill))
                    try:
                        return input(prompt)
                    finally:
                        readline.set_startup_hook()

                edited_content = prefill_input(
                    "> ", action_details["post_content"]
                ).strip()
                if edited_content:
                    decision = edited_content
                    break
                else:
                    print("Edit cancelled - content cannot be empty.")
            else:
                print("Invalid input. Please enter 'a', 'r', or 'e'.")

        # Step 3: Resume with the decision
        if isinstance(decision, str):
            print("\nResuming workflow with edited content (auto-approving)...")
            # Edit auto-approves and goes to approve node
            result = graph.invoke(Command(resume=decision), config=config)
            break
        else:
            print(f"\nResuming workflow: {'APPROVED' if decision else 'REJECTED'}")
            # Approve/reject goes to approve or reject node
            result = graph.invoke(Command(resume=decision), config=config)
            break

    # Final status is printed by approve_node or reject_node


if __name__ == "__main__":
    main()
