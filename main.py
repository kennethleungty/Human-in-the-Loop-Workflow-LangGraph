from langgraph.types import Command
from src.graph import graph


def main():
    """Example usage of the workflow with interrupts"""

    # Configuration with thread_id for checkpointing
    config = {"configurable": {"thread_id": "workflow-001"}}

    # Initial state
    initial_state = {"search_results": "", "action_details": "", "status": "pending"}

    # Step 1: Start the workflow - it will run until the interrupt
    print("=" * 60)
    print("Starting workflow...")
    print("=" * 60)
    initial = graph.invoke(initial_state, config=config)

    # The workflow pauses at the approval_node interrupt
    if "__interrupt__" in initial:
        print("\nWorkflow paused for approval:")
        print(initial["__interrupt__"])

        # Show current state
        print("\nCurrent State:")
        print(f"Status: {initial['status']}")
        print(f"\n{initial['__interrupt__'][0].value['question']}")
        print(f"Details:\n{initial['__interrupt__'][0].value['details']}")

        # Step 2: Resume with the decision
        # Set to True to approve (routes to write_to_db), False to reject (routes to cancel)
        print("\n" + "=" * 60)
        print("Resuming with approval decision: True")
        print("=" * 60)
        resumed = graph.invoke(Command(resume=True), config=config)

        print("\nWorkflow completed!")
        print(f"Status: {resumed['status']}")
    else:
        print("No interrupt occurred (unexpected)")


def main_reject():
    """Example showing rejection flow"""

    config = {"configurable": {"thread_id": "workflow-002"}}

    initial_state = {"search_results": "", "action_details": "", "status": "pending"}

    print("\n" + "=" * 60)
    print("Testing rejection flow...")
    print("=" * 60)

    initial = graph.invoke(initial_state, config=config)

    if "__interrupt__" in initial:
        print("\nWorkflow paused for approval")
        print("\n" + "=" * 60)
        print("Resuming with rejection decision: False")
        print("=" * 60)

        resumed = graph.invoke(Command(resume=False), config=config)

        print("\nWorkflow cancelled!")
        print(f"Status: {resumed['status']}")


if __name__ == "__main__":
    # Run approval flow
    main()

    # Run rejection flow
    print("\n" + "=" * 60)
    main_reject()
