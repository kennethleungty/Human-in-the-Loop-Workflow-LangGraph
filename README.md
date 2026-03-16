# Human-in-the-Loop Bluesky Post Workflow

LangGraph workflow that searches for news via Tavily, generates a Bluesky post using GPT-5-mini, and requires human approval before publishing.

## How It Works

1. **Web Search** — Fetches latest news via Tavily API based on a configurable query
2. **Content Creation** — Generates a punchy Bluesky post using OpenAI Responses API
3. **Human Review** — Pauses for review: approve, reject, or edit the draft in-terminal
4. **Publish Confirmation** — Second checkpoint before posting to Bluesky
5. **Action** — Posts to Bluesky if confirmed, discards if rejected or cancelled

## Key Features

- Two-stage `interrupt()`-based human-in-the-loop approval
- Persistent state checkpointing with SqliteSaver
- Explicit routing via `Command(goto=...)` across all nodes
- Editable draft text with readline pre-fill
- Auto-generated Mermaid diagram (`assets/graph_setup.png`)

## Setup

### API Keys

1. **OpenAI** — Create a key at [OpenAI Platform](https://platform.openai.com/)
2. **Tavily** — Get a key from [Tavily](https://tavily.com/) (free tier: 1,000 credits/month)
3. **Bluesky** — Create an app password at [Bluesky](https://bsky.app/) → Settings → App Passwords

### Installation

```bash
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your OpenAI, Tavily, and Bluesky credentials

source .env
python main.py
```

## Project Structure

```
src/
├── nodes/
│   ├── web_search_node.py          # Tavily news search
│   ├── content_generation_node.py  # OpenAI post generation
│   ├── human_review_node.py        # Interrupt for review
│   ├── decision_approve_node.py    # Publish approved post
│   └── decision_reject_node.py     # Handle rejection
├── graph.py                        # LangGraph workflow definition
├── state.py                        # TypedDict state schema
├── prompts.py                      # AI prompt templates
├── tools.py                        # Tavily search & Bluesky publish tools
└── utils.py                        # Mermaid diagram helper
config.py                           # LLM settings (model, temperature)
main.py                             # Workflow execution entry point
```
