# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI research assistant built with LangChain that helps users generate research papers. The application uses a tool-calling agent architecture with multiple LLM providers (OpenAI GPT-4o-mini and Anthropic Claude Sonnet 4) and integrates web search, Wikipedia, and file saving capabilities.

## Key Architecture

- **main.py**: Entry point with agent setup and execution flow
- **tools.py**: Custom LangChain tools for search, Wikipedia queries, and file saving
- **Agent Pattern**: Uses `create_tool_calling_agent` with `AgentExecutor` for tool orchestration
- **Structured Output**: Enforces JSON responses via Pydantic `ResearchResponse` model with fields: topic, summary, sources, tools_used
- **Dual LLM Setup**: Primary agent uses OpenAI (llm), secondary Anthropic model available (llm2)

## Environment Setup

Requires `.env` file with API keys:
- `OPENAI_API_KEY` 
- `ANTHROPIC_API_KEY`

## Common Commands

**Install dependencies:**
```bash
uv sync
```

**Run the application:**
```bash
python main.py
```

**Install new dependencies:**
```bash
uv add <package-name>
```

## Tools Integration

The agent has access to three tools:
1. `search_tool`: DuckDuckGo web search
2. `wiki_tool`: Wikipedia queries (limited to 5 results, 100 chars max)
3. `save_tool`: Saves research output to timestamped text files

## Response Format

All agent responses must conform to the `ResearchResponse` Pydantic schema. The application includes error handling for parsing failures and will display raw responses when structured parsing fails.