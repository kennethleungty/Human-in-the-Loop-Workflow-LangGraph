from src.state import State
from src.tools import publish_post
from langgraph.types import Command
from langgraph.graph import END
import json


def decision_approve_node(state: State) -> Command:
    """Node that publishes approved content to X using the publish_post tool.

    The publish_post tool uses interrupt-before-action pattern:
    it pauses for final confirmation before actually publishing.
    """
    post_data = json.loads(state["post_data"])

    # Call the publish_post tool (which interrupts for final confirmation)
    publish_post.invoke(
        {
            "post_content": post_data["post_content"],
            "title": post_data["title"],
            "url": post_data["url"],
        }
    )

    return Command(update={**state, "status": "approved"}, goto=END)
