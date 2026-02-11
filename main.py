from langgraph.types import Command
from src.graph import graph, create_thread_config
import json


def main():
    """Example usage of the workflow with interrupts"""

    # Configuration with thread_id for checkpointing
    config = create_thread_config("workflow-001")

    # Initial state
    initial_state = {"search_results": "", "action_details": "", "status": "pending"}

    # Step 1: Start the workflow - it will run until the interrupt
    print("=" * 60)
    print("Starting workflow...")
    print("=" * 60)
    result = graph.invoke(initial_state, config=config)

    # The workflow pauses at the approval_node interrupt
    if "__interrupt__" in result:
        print("WORKFLOW PAUSED - APPROVAL REQUIRED")
        # Parse and display the action_details
        action_details = json.loads(result["action_details"])

        print("\nArticle Details:")
        print(f"Title: {action_details['title']}")
        print(f"URL: {action_details['url']}")
        print(f"Published: {action_details['published_date']}")

        print("\nGenerated X Post:")
        print("-" * 60)
        print(action_details["post_content"])
        print("-" * 60)

        # Step 2: Get user decision
        while True:
            user_input = input("Approve this post? (y/yes or n/no): ").lower().strip()
            if user_input in ["y", "yes"]:
                decision = True
                break
            elif user_input in ["n", "no"]:
                decision = False
                break
            else:
                print("Invalid input. Please enter 'y', 'yes', 'n', or 'no'.")

        # Step 3: Resume with the decision (True -> write_to_db, False -> cancel)
        print(
            f"Resuming workflow with decision: {'APPROVED' if decision else 'REJECTED'}"
        )
        resumed = graph.invoke(Command(resume=decision), config=config)

        print("WORKFLOW COMPLETED")
        print(f"Final Status: {resumed['status']}")
    else:
        print("\nError: No interrupt occurred (unexpected)")


if __name__ == "__main__":
    main()
