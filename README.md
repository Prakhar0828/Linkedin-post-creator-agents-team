# Linked-Writer-Agent

CrewAI workflow that researches a topic (web + YouTube), drafts a LinkedIn post, and optionally generates a DALL-E image.

## Prerequisites

- Python 3.10+
- API keys in environment (see below)

## Install

From this directory, install dependencies your environment already uses for CrewAI (for example the `writer_agent` project’s `uv sync` if you use that venv), or install `crewai` / `crewai-tools` to match `writer_agent/pyproject.toml`.

## Environment variables

Set in `.env` or the shell (names only; do not commit secret values):

- `OPENAI_API_KEY` (and any other keys required by your tools, e.g. search APIs if you use Serper)

## Run

```bash
python main.py
```

You will be prompted for:

1. **Topic** for the LinkedIn post  
2. **YouTube video URL** to analyze  

Output is written to `linkedin_post.md` by the crew configuration.

## Tests

There is no dedicated `pytest` suite at the repository root for `main.py`. The nested `writer_agent` package follows CrewAI’s standard layout (`writer_agent/README.md`).

## Project layout

- `main.py` — entrypoint for the LinkedIn crew run  
- `linkedin_crew.py` — shared crew utilities / imports as used by your setup  
- `Knowledge/` — example post text files for writer grounding  
- `skills/` — CrewAI skill folders (e.g. LinkedIn writing)  
