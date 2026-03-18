"""Utility functions for the workflow"""

from pathlib import Path
from datetime import datetime, timezone
import logging
import os
import requests

logger = logging.getLogger(__name__)


def save_mermaid_diagram(graph, output_path: str = "assets/graph_setup.png"):
    """Save the workflow graph visualization to a file.

    Args:
        graph: The compiled LangGraph to visualize
        output_path: Path to save the visualization PNG
    """
    try:
        # Create directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate visualization using LangGraph's built-in method
        graph_png = graph.get_graph(xray=True).draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(graph_png)
        logger.info(f"Mermaid diagram saved to: {output_path}")
        print(f"Graph visualization saved to: {output_path}")
    except Exception as e:
        logger.error(f"Could not generate diagram: {e}")
        print(f"Warning: Could not generate diagram: {e}")


def publish_to_bluesky(post_content: str) -> str:
    """Authenticate with Bluesky and publish a post. Returns a status message."""
    handle = os.getenv("BLUESKY_HANDLE")
    app_password = os.getenv("BLUESKY_APP_PASSWORD")

    if not handle or not app_password:
        return "Error: BLUESKY_HANDLE and BLUESKY_APP_PASSWORD must be set"

    try:
        auth_response = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": handle, "password": app_password},
        )
        auth_response.raise_for_status()
        auth = auth_response.json()

        post_response = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {auth['accessJwt']}"},
            json={
                "repo": auth["did"],
                "collection": "app.bsky.feed.post",
                "record": {
                    "text": post_content,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                },
            },
        )
        post_response.raise_for_status()

        return "Post successfully posted on Bluesky"

    except requests.exceptions.RequestException as e:
        return f"Error posting to Bluesky: {str(e)}"
