from langchain_core.tools import tool
from langgraph.types import interrupt
from tavily import TavilyClient
from datetime import datetime, timezone
import os
import json
import requests


@tool
def tavily_search(query: str) -> str:
    """Search for latest news articles using Tavily API."""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    search_response = tavily_client.search(
        query=query,
        max_results=1,
        topic="news",
        search_depth="advanced",
        include_answer=False,
        include_raw_content=False,
        include_images=False,
    )

    result = search_response["results"][0] if search_response["results"] else {}

    return json.dumps(
        {
            "query": query,
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "published_date": result.get("published_date", ""),
            "content": result.get("content", ""),
        }
    )


@tool
def publish_post(post_content: str, title: str, url: str) -> str:
    """Publish a post to Bluesky. Interrupts for human confirmation before executing."""
    # Interrupt BEFORE the action — safe on re-execution
    response = interrupt(
        {
            "action": "confirm_publish",
            "post_content": post_content,
            "title": title,
            "url": url,
        }
    )

    if response.get("action") == "confirm":
        # Authenticate with Bluesky
        handle = os.getenv("BLUESKY_HANDLE")
        app_password = os.getenv("BLUESKY_APP_PASSWORD")

        if not handle or not app_password:
            return "Error: BLUESKY_HANDLE and BLUESKY_APP_PASSWORD must be set"

        try:
            # Login to get access token
            auth_response = requests.post(
                "https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": handle, "password": app_password},
            )
            auth_response.raise_for_status()
            auth = auth_response.json()

            access_token = auth["accessJwt"]
            did = auth["did"]

            # Create post with current timestamp
            post_response = requests.post(
                "https://bsky.social/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {access_token}"},
                json={
                    "repo": did,
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

    return "Post publishing cancelled by user"
