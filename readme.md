# Obsidian AI Agent

A local-first AI second-brain lab for learning and building agentic AI systems using **Obsidian**, **Markdown**, **Ollama**, **LangGraph**, **MCP**, and **ChromaDB**.

This repository contains a staged set of Python projects that gradually upgrade a simple Obsidian note generator into a multi-agent, MCP-enabled, vector-search-powered AI second brain.



---

## What This Project Does

This project helps you build an AI-powered second brain where agents can:

- Generate Markdown notes for Obsidian
- Save notes into your Obsidian vault
- Search and read existing notes
- Expose Obsidian as MCP tools
- Run LangGraph workflows
- Coordinate multiple specialist agents
- Build a local vector database over your notes
- Ask RAG-style questions over your Obsidian vault

---

## Project Progression

| Project | File | Purpose |
|---|---|---|
| Project 1 | `project1_note_assistant.py` | Generate an Obsidian note from a topic using Ollama |
| Project 2 | `project2_mcp_obsidian_server.py` | Expose Obsidian vault operations as MCP tools |
| Project 3 | `project3_langgraph_agent.py` | Use LangGraph to generate explanation, quiz, and project ideas |
| Project 4 | `project4_multi_agent_orchestrator.py` | Coordinate Notes, Research, Quiz, Coding, and Reflection agents |
| Project 5 | `project5_vector_search_obsidian.py` | Build semantic search and RAG over Obsidian using ChromaDB |

---

## Architecture

```text
User Input
   ↓
Ollama Local Model
   ↓
LangGraph / Multi-Agent Workflow
   ↓
MCP Obsidian Tools
   ↓
Obsidian Markdown Vault
   ↓
ChromaDB Vector Search
   ↓
RAG Answer Generation
```

---

## Prerequisites

Install the following:

- Python 3.10 or higher
- Git
- Obsidian
- Ollama
- Node.js, only needed for MCP Inspector

Recommended Ollama models:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Check installed models:

```powershell
ollama list
```

---

## Setup

Clone the repository:

```powershell
git clone https://github.com/rohan-mn/obsidian-ai-agent.git
cd obsidian-ai-agent
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the repository root:

```env
OBSIDIAN_VAULT=C:\Path\To\Your\Obsidian\Vault
```

Example:

```env
OBSIDIAN_VAULT=C:\Users\rohan\Documents\Obsidian\AI-Second-Brain
```

You can also set it temporarily in PowerShell:

```powershell
$env:OBSIDIAN_VAULT="C:\Users\rohan\Documents\Obsidian\AI-Second-Brain"
```

---

## Project 1: AI Note Assistant

File:

```text
project1_note_assistant.py
```

Purpose:

Generates a structured Markdown note from a topic and saves it inside:

```text
<OBSIDIAN_VAULT>/00-Inbox
```

Run:

```powershell
python project1_note_assistant.py
```

Example topic:

```text
MCP vs API
```

Output:

```text
00-Inbox/MCP vs API.md
```

---

## Project 2: MCP Obsidian Server

File:

```text
project2_mcp_obsidian_server.py
```

Purpose:

Exposes your Obsidian vault as MCP tools.

Available tools:

```text
list_notes
read_note
search_notes
create_note
append_to_note
```

Run self-test:

```powershell
python project2_mcp_obsidian_server.py --self-test
```

Run as MCP server:

```powershell
python project2_mcp_obsidian_server.py
```

Test with MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector .venv\Scripts\python.exe project2_mcp_obsidian_server.py
```

Useful test inputs:

```text
search_notes
query = MCP
```

```text
read_note
note_path = 02-Concepts/MCP.md
```

---

## Project 3: LangGraph Research Agent

File:

```text
project3_langgraph_agent.py
```

Purpose:

Runs a LangGraph workflow that creates:

- Explanation
- Quiz
- Project ideas
- Final Markdown note

Workflow:

```text
Topic
   ↓
Generate Explanation
   ↓
Generate Quiz
   ↓
Generate Project Ideas
   ↓
Assemble Markdown
   ↓
Save to Obsidian
```

Run:

```powershell
python project3_langgraph_agent.py
```

Output folder:

```text
<OBSIDIAN_VAULT>/01-Learning-Roadmap
```

---

## Project 4: Multi-Agent Orchestrator

File:

```text
project4_multi_agent_orchestrator.py
```

Purpose:

Coordinates multiple specialist agents using LangGraph.

Agents:

| Agent | Role |
|---|---|
| Supervisor Agent | Plans which agents are needed |
| Notes Agent | Searches Obsidian notes |
| Research Agent | Explains the topic |
| Quiz Agent | Creates questions |
| Coding Agent | Creates implementation guidance |
| Reflection Agent | Reviews output quality |
| Save Agent | Saves final Markdown note |

Run:

```powershell
python project4_multi_agent_orchestrator.py
```

Example task:

```text
Give me a complete learning note and mini project for Advanced MCP Security
```

Output folder:

```text
<OBSIDIAN_VAULT>/06-Advanced-Agent-Engineering/Multi-Agent Runs
```

---

## Project 5: Vector Search and RAG over Obsidian

File:

```text
project5_vector_search_obsidian.py
```

Purpose:

Builds a local ChromaDB vector index over your Obsidian Markdown notes and allows semantic search and RAG-style Q&A.

Flow:

```text
Obsidian Markdown Notes
   ↓
Chunking
   ↓
Ollama Embeddings
   ↓
ChromaDB
   ↓
Semantic Search
   ↓
RAG Answer
```

Required Ollama models:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Index notes:

```powershell
python project5_vector_search_obsidian.py index
```

Show database stats:

```powershell
python project5_vector_search_obsidian.py stats
```

Semantic search:

```powershell
python project5_vector_search_obsidian.py search "How do AI agents use memory and tools?"
```

Ask a RAG question:

```powershell
python project5_vector_search_obsidian.py ask "How do MCP and LangGraph work together?"
```

Save a RAG answer to Obsidian:

```powershell
python project5_vector_search_obsidian.py save-answer "How do MCP and LangGraph work together?"
```

Output folder:

```text
<OBSIDIAN_VAULT>/06-Advanced-Agent-Engineering/Vector Search Runs
```

Local ChromaDB folder:

```text
chroma_obsidian_db/
```

---

## Recommended Learning Path

Use the projects in this order:

```text
1. Project 1 - Basic AI note generation
2. Project 2 - MCP access to Obsidian
3. Project 3 - LangGraph workflow
4. Project 4 - Multi-agent orchestration
5. Project 5 - Vector database and RAG
```

This progression teaches:

```text
Markdown
Obsidian
Ollama
MCP
LangGraph
Multi-agent orchestration
Vector databases
RAG
```

---

## Troubleshooting

### `OBSIDIAN_VAULT` not set

Create a `.env` file:

```env
OBSIDIAN_VAULT=C:\Path\To\Your\Obsidian\Vault
```

Or set it in PowerShell:

```powershell
$env:OBSIDIAN_VAULT="C:\Path\To\Your\Obsidian\Vault"
```

### Vault path does not exist

Open Obsidian, right-click a note, choose **Show in system explorer**, and copy the actual vault folder path.

### Ollama model not found

Pull the required models:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### MCP Inspector error: `spawn uv ENOENT`

Use Python directly instead of `uv`:

```powershell
npx @modelcontextprotocol/inspector .venv\Scripts\python.exe project2_mcp_obsidian_server.py
```

### Project 5 error: `model "nomic-embed-text" not found`

Run:

```powershell
ollama pull nomic-embed-text
```

Then rerun:

```powershell
python project5_vector_search_obsidian.py index
```

### ChromaDB import error

Make sure `chromadb` is installed:

```powershell
pip install chromadb
```

Also ensure it is present in `requirements.txt`.

---

## Security Notes

This project is intended for local learning.

The MCP server includes path-safety checks to prevent access outside the configured Obsidian vault. However, before using this with remote clients or production systems, add:

- Read-only mode
- Write confirmation
- Audit logging
- Folder allowlists
- Secret-file blocking
- Authentication
- Permission separation between read and write tools

---

## Suggested `.gitignore`

Make sure your `.gitignore` includes:

```gitignore
.env
.venv/
__pycache__/
*.pyc
chroma_obsidian_db/
.DS_Store
```

Do not commit `.env`, `.venv`, or your local ChromaDB database.

---

## Current Status

Completed:

- Local AI note generation
- Obsidian vault integration
- MCP tool server
- LangGraph research agent
- Multi-agent orchestration
- ChromaDB vector search
- RAG-style answering from notes

Next possible upgrades:

- LangSmith observability
- FastAPI deployment
- Dockerization
- Cloud deployment
- Advanced MCP security
- Google ADK version
