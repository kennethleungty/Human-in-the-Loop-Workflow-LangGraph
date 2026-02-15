from src.state import State
from src.tools import publish_post
from langgraph.types import Command
from langgraph.graph import END
import json


def decision_approve_node(state: State) -> Command:
    """Publish approved content using the publish_post tool (which interrupts for confirmation)."""
    post_data = json.loads(state["post_data"])

    # Use post publishing tool
    publish_post.invoke(
        {
            "post_content": post_data["post_content"],
            "title": post_data["title"],
            "url": post_data["url"],
        }
    )

    return Command(update={**state, "status": "approved"}, goto=END)
