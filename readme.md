
# AI Second Brain Lab

This repository contains small Python utilities for generating and managing Obsidian notes using agentic LLM workflows (Ollama, LangGraph, and MCP). The tools are lightweight examples for building a personal "second brain" that can generate, search, read, and save Markdown notes inside an Obsidian vault.

Contents
- `project1_note_assistant.py` — simple Ollama-based note generator that saves to an Obsidian vault `00-Inbox`.
- `project2_mcp_obsidian_server.py` — an MCP server exposing vault operations (list, read, search, create, append).
- `project3_langgraph_agent.py` — a LangGraph state-graph agent that builds an explanation, quiz, and project ideas, then saves a compiled note in the vault.
- `requirements.txt` — Python dependencies used by these scripts.

Prerequisites
- Python 3.8+ (3.10+ recommended)
- A running Ollama environment and Python `ollama` client (the projects call `ollama.chat`). See Ollama docs for installing and running a local model.
- An Obsidian vault folder on your machine (the scripts write into this vault).
- Install dependencies (recommended in a virtualenv).

Install

PowerShell (recommended on Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

OR Bash / macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Environment configuration
- The scripts read configuration from a `.env` file located in the repository root (or from environment variables). Create a `.env` file with the following key:

```
OBSIDIAN_VAULT=C:\Path\To\Your\Obsidian\Vault
```

Replace the path with your real Obsidian vault path. On Windows use double backslashes or plain backslashes as shown.

If you prefer, you can set the variable in PowerShell for the current session:

```powershell
$env:OBSIDIAN_VAULT = "C:\Users\You\Documents\Obsidian\AI-Second-Brain"
```

Notes about Ollama
- The scripts use the Python `ollama` package to call local models. Ensure your Ollama runtime is running and that the model referenced in the scripts (`llama3.2:3b`) exists or update `MODEL` inside the scripts to a model you have available.

Repository scripts

1) project1_note_assistant.py — AI Note Assistant
- Purpose: Interactively generate a beginner-friendly Obsidian note for a user-provided topic and save it under `00-Inbox` inside your vault.
- Key behavior:
	- Loads `.env` (if present) and reads `OBSIDIAN_VAULT`.
	- Prompts for a topic, requests a structured note from Ollama, and saves a Markdown file with frontmatter under `00-Inbox`.
- Run (PowerShell):

```powershell
python project1_note_assistant.py
```

You will be prompted for a topic. The generated note is saved to `<OBSIDIAN_VAULT>/00-Inbox/<safe-title>.md`.

2) project2_mcp_obsidian_server.py — MCP Obsidian Server
- Purpose: Provide MCP tools for interacting with an Obsidian vault programmatically. Exposes tools for listing, reading, searching, creating, and appending notes.
- Key behavior:
	- Uses `mcp.server.fastmcp.FastMCP` to define tools decorated with `@mcp.tool()`.
	- Tools include `list_notes(folder="")`, `read_note(note_path)`, `search_notes(query)`, `create_note(note_path, content)`, and `append_to_note(note_path, content)`.
	- Includes a `--self-test` mode that runs a simple local test without an MCP client.
- Run (PowerShell):

Self-test (no MCP client required):
```powershell
python project2_mcp_obsidian_server.py --self-test
```

Run as MCP server (normal):
```powershell
python project2_mcp_obsidian_server.py
```

In a new powershell terminal start:
```powershell
npx @modelcontextprotocol/inspector .venv\Scripts\python.exe project2_mcp_obsidian_server.py
```

You can try any of these tools in tools selection:
```
list_notes
search_notes
read_note
create_note
append_to_note

Example (1):
search_notes
query = MCP

Example (2):
read_note
note_path = 02-Concepts/MCP.md
```

When running as a server, the MCP framework will start and listen for clients (see `mcp` docs for CLI flags and configuration).

3) project3_langgraph_agent.py — LangGraph Research Agent
- Purpose: Use a LangGraph StateGraph to orchestrate several Ollama prompts to produce an explanation, quiz, and project ideas, assemble a Markdown note, and save it to `01-Learning-Roadmap` in the vault.
- Key behavior:
	- Loads `.env` and reads `OBSIDIAN_VAULT`.
	- Prompts for a topic, then runs a LangGraph workflow consisting of: generate_explanation → generate_quiz → generate_project_ideas → assemble_note → save_to_obsidian.
	- Writes the final note into `<OBSIDIAN_VAULT>/01-Learning-Roadmap/`.
- Run (PowerShell):

```powershell
python project3_langgraph_agent.py
```

You will be prompted for a topic. The saved file path is printed at the end.

Dependencies
- See `requirements.txt`. The primary packages used are:
	- `ollama` — Python client to call Ollama models
	- `langgraph` — state graph orchestration used by `project3_langgraph_agent.py`
	- `mcp` — MCP server and tooling used by `project2_mcp_obsidian_server.py`
	- `python-dotenv` — loads `.env` file

Troubleshooting
- OBISIDIAN_VAULT not set: the scripts will raise a helpful error explaining how to set `OBSIDIAN_VAULT` in `.env` or environment.
- Ollama errors: ensure Ollama daemon is running and the model name in `MODEL` exists. You can change `MODEL` constant in each script if needed.
- Permissions: the MCP server script uses `safe_vault_path()` to prevent access outside the vault. Ensure the `OBSIDIAN_VAULT` path is correct and the user running the script has filesystem permissions.

Contributing
- These scripts are examples and meant for experimentation. If you extend them, consider:
	- Adding CLI flags (argparse) to set model name, output folder, or dry-run mode.
	- Adding logging instead of print statements.
	- Adding unit tests for file-path safety helpers.




