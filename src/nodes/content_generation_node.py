from typing import Literal
from src.state import State
from src.prompts import X_POST_INSTRUCTIONS
from config import LLM_MODEL, TEMPERATURE
from openai import OpenAI
from langgraph.types import Command
import os
import json


def content_generation_node(state: State) -> Command[Literal["review"]]:
    """Node that generates X (Twitter) post from search results using OpenAI"""
    # Parse the search results JSON
    search_data = json.loads(state["search_results"])

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Combine instructions and article data into single input
    # Using direct dict access to fail loudly if required keys are missing
    input_text = f"""{X_POST_INSTRUCTIONS}

    ## Article Information
    Title: {search_data['title']}
    URL: {search_data['url']}
    Published Date: {search_data['published_date']}

    ## Article Content
    {search_data['content']}
    """

    # Generate X post using OpenAI Responses API
    response = client.responses.create(
        model=LLM_MODEL,
        input=input_text,
        temperature=TEMPERATURE,
    )

    # Create output JSON with generated post and article metadata
    post_data = json.dumps(
        {
            "post_content": response.output_text,
            "title": search_data["title"],
            "url": search_data["url"],
            "published_date": search_data["published_date"],
        },
        indent=2,
    )

    return Command(
        update={**state, "post_data": post_data, "status": "pending"}, goto="review"
    )
