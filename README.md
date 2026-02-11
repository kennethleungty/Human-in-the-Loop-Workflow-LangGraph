# Human-in-the-Loop X Post Workflow

LangGraph workflow that searches for OpenAI news, generates X posts using GPT-5.2, and requires human approval before publishing.

## How It Works

1. **Web Search** - Fetches latest OpenAI news via Tavily API
2. **Content Creation** - Generates sharp X post using OpenAI Responses API
3. **Review** - Pauses workflow for human review (approve/reject/edit in terminal)
4. **Action** - Posts to X if approved, discards if rejected

## Key Features

- LangGraph interrupt-based approval with checkpointing
- OpenAI Responses API (gpt-5.2, temperature=1.0)
- Tavily news search with advanced depth
- Auto-generated Mermaid diagram visualization
- Modular node architecture

## Setup

### Get API Keys

1. **OpenAI API Key**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Navigate to API Keys section
   - Create new secret key

2. **Tavily API Key**
   - Sign up at [Tavily](https://tavily.com/)
   - Get your API key from dashboard
   - Free tier: 1,000 API credits/month

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables in .env file
cp .env.example .env
# Edit .env with your Tavily and OpenAI API keys

# Load environment variables
source .env

# Run workflow
python main.py
```

## Project Structure

```
src/
├── nodes/          # Individual workflow nodes
├── graph.py        # LangGraph workflow definition
├── state.py        # State type definition
├── prompts.py      # AI prompts
└── utils.py        # Helper functions
config.py           # LLM settings
main.py             # Workflow execution
```

## References

- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [Tavily Search API](https://docs.tavily.com/)
