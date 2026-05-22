from pathlib import Path
from typing import TypedDict, List
from datetime import datetime
import os
import re

from dotenv import load_dotenv
import ollama
from langgraph.graph import StateGraph, START, END


# Load .env
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    load_dotenv()


MODEL = "llama3.2:3b"


class MultiAgentState(TypedDict):
    task: str
    plan: List[str]
    completed_agents: List[str]

    notes_context: str
    research_output: str
    quiz_output: str
    coding_output: str
    reflection_output: str

    final_note: str
    saved_path: str


def get_vault_path() -> Path:
    vault = os.environ.get("OBSIDIAN_VAULT")

    if not vault:
        raise EnvironmentError(
            "OBSIDIAN_VAULT is not set. Add this to .env:\n"
            "OBSIDIAN_VAULT=C:\\Path\\To\\AI-Second-Brain"
        )

    path = Path(vault)

    if not path.exists():
        raise FileNotFoundError(f"Vault path does not exist: {path}")

    return path


def safe_filename(title: str) -> str:
    title = re.sub(r'[<>:"/\\\\|?*]', "", title)
    title = title.strip()
    return title[:80] if title else "Untitled"


def ask_ollama(prompt: str, system_message: str = "") -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_message or "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]


def search_obsidian_notes(query: str, max_results: int = 5) -> str:
    vault = get_vault_path()
    query_lower = query.lower()

    matches = []

    for path in vault.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        score = 0

        if query_lower in path.name.lower():
            score += 3

        if query_lower in text.lower():
            score += 2

        for word in query_lower.split():
            if word in text.lower():
                score += 1

        if score > 0:
            matches.append((score, path, text[:1200]))

    matches.sort(key=lambda x: x[0], reverse=True)

    if not matches:
        return "No directly matching Obsidian notes found."

    context_parts = []

    for score, path, snippet in matches[:max_results]:
        relative_path = path.relative_to(vault)
        context_parts.append(
            f"## Source: {relative_path}\n"
            f"Score: {score}\n"
            f"Snippet:\n{snippet}\n"
        )

    return "\n---\n".join(context_parts)


def supervisor_agent(state: MultiAgentState) -> MultiAgentState:
    print("Supervisor Agent: Creating plan...")

    task = state["task"].lower()

    plan = []

    # Notes are useful for most learning tasks
    plan.append("notes")

    if any(word in task for word in ["quiz", "mcq", "test", "questions"]):
        plan.append("quiz")

    elif any(word in task for word in ["code", "python", "script", "program", "implementation"]):
        plan.append("coding")

    elif any(word in task for word in ["complete", "full", "deep", "learn", "roadmap", "project"]):
        plan.extend(["research", "quiz", "coding"])

    else:
        plan.append("research")

    # Remove duplicates while preserving order
    final_plan = []
    for item in plan:
        if item not in final_plan:
            final_plan.append(item)

    state["plan"] = final_plan
    state["completed_agents"] = []

    print(f"Supervisor Plan: {state['plan']}")

    return state


def dispatcher(state: MultiAgentState) -> MultiAgentState:
    print("Dispatcher: Checking next agent...")
    return state


def route_next_agent(state: MultiAgentState) -> str:
    plan = state["plan"]
    completed = state["completed_agents"]

    for agent in plan:
        if agent not in completed:
            if agent == "notes":
                return "notes_agent"
            if agent == "research":
                return "research_agent"
            if agent == "quiz":
                return "quiz_agent"
            if agent == "coding":
                return "coding_agent"

    return "reflection_agent"


def notes_agent(state: MultiAgentState) -> MultiAgentState:
    print("Notes Agent: Searching Obsidian notes...")

    task = state["task"]
    context = search_obsidian_notes(task)

    state["notes_context"] = context
    state["completed_agents"].append("notes")

    return state


def research_agent(state: MultiAgentState) -> MultiAgentState:
    print("Research Agent: Generating explanation...")

    prompt = f"""
You are the Research Agent in a multi-agent AI second-brain system.

User task:
{state["task"]}

Relevant Obsidian note context:
{state["notes_context"]}

Create a useful explanation with:

## Simple Meaning
## Why It Matters
## Key Concepts
## Architecture / Flow
## Practical Use Cases
## Common Mistakes
## Related Obsidian Links

Use Obsidian backlinks like [[AI Agents]], [[MCP]], [[LangGraph]], [[LangSmith Observability]] where relevant.
"""

    state["research_output"] = ask_ollama(
        prompt,
        "You are a research specialist agent. Explain clearly and practically in Markdown.",
    )

    state["completed_agents"].append("research")
    return state


def quiz_agent(state: MultiAgentState) -> MultiAgentState:
    print("Quiz Agent: Creating quiz...")

    prompt = f"""
You are the Quiz Agent in a multi-agent AI second-brain system.

User task:
{state["task"]}

Existing research output:
{state["research_output"]}

Relevant Obsidian context:
{state["notes_context"]}

Create:

## 5 Multiple Choice Questions
Each with 4 options.

## 5 Short Answer Questions

## Answer Key

Make questions useful for learning and revision.
"""

    state["quiz_output"] = ask_ollama(
        prompt,
        "You are a quiz generation specialist. Create clear educational questions.",
    )

    state["completed_agents"].append("quiz")
    return state


def coding_agent(state: MultiAgentState) -> MultiAgentState:
    print("Coding Agent: Creating implementation guidance...")

    prompt = f"""
You are the Coding Agent in a multi-agent AI second-brain system.

User task:
{state["task"]}

Relevant Obsidian context:
{state["notes_context"]}

Research output if available:
{state["research_output"]}

Create:

## Implementation Goal
## Folder Structure
## Python Code / Pseudocode
## How to Run
## Expected Output
## Next Improvements

Keep it practical for a beginner using Python, Ollama, Obsidian, MCP, and LangGraph.
"""

    state["coding_output"] = ask_ollama(
        prompt,
        "You are a coding mentor. Give practical beginner-friendly implementation guidance.",
    )

    state["completed_agents"].append("coding")
    return state


def reflection_agent(state: MultiAgentState) -> MultiAgentState:
    print("Reflection Agent: Reviewing output quality...")

    combined_output = f"""
Research Output:
{state["research_output"]}

Quiz Output:
{state["quiz_output"]}

Coding Output:
{state["coding_output"]}
"""

    prompt = f"""
You are the Reflection Agent.

Review the following multi-agent output for the task:

{state["task"]}

Output:
{combined_output}

Give:

## Quality Check
- Is the answer complete?
- Is it beginner-friendly?
- Is it practical?
- What is missing?

## Suggested Improvements
Give 3 improvements.

## Final Verdict
Say whether this is good enough to save into Obsidian.
"""

    state["reflection_output"] = ask_ollama(
        prompt,
        "You are a strict but helpful reviewer agent.",
    )

    return state


def assemble_final_note(state: MultiAgentState) -> MultiAgentState:
    print("Save Agent: Assembling final note...")

    task = state["task"]
    plan_text = " → ".join(state["plan"])

    state["final_note"] = f"""---
created: {datetime.now().strftime("%Y-%m-%d %H:%M")}
source: Multi-Agent Second Brain Orchestrator
status: draft
tags:
  - ai
  - multi-agent
  - langgraph
  - second-brain
---

# {task}

#ai #multi-agent #langgraph #second-brain

## Multi-Agent Plan

{plan_text}

## Completed Agents

{", ".join(state["completed_agents"])}

---

## Notes Agent Output

{state["notes_context"]}

---

## Research Agent Output

{state["research_output"]}

---

## Quiz Agent Output

{state["quiz_output"]}

---

## Coding Agent Output

{state["coding_output"]}

---

## Reflection Agent Output

{state["reflection_output"]}

---

## Related Notes

- [[AI Agents]]
- [[MCP]]
- [[LangGraph]]
- [[Multi-Agent Orchestration]]
- [[Project 4 - AI Second Brain Agent Platform]]
"""

    return state


def save_to_obsidian(state: MultiAgentState) -> MultiAgentState:
    print("Save Agent: Saving to Obsidian...")

    vault = get_vault_path()

    target_folder = vault / "06-Advanced-Agent-Engineering" / "Multi-Agent Runs"
    target_folder.mkdir(parents=True, exist_ok=True)

    filename = safe_filename(state["task"]) + " - Multi Agent.md"
    note_path = target_folder / filename

    if note_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        note_path = target_folder / f"{safe_filename(state['task'])} - Multi Agent {timestamp}.md"

    note_path.write_text(state["final_note"], encoding="utf-8")

    state["saved_path"] = str(note_path)

    return state


def build_graph():
    graph = StateGraph(MultiAgentState)

    graph.add_node("supervisor_agent", supervisor_agent)
    graph.add_node("dispatcher", dispatcher)
    graph.add_node("notes_agent", notes_agent)
    graph.add_node("research_agent", research_agent)
    graph.add_node("quiz_agent", quiz_agent)
    graph.add_node("coding_agent", coding_agent)
    graph.add_node("reflection_agent", reflection_agent)
    graph.add_node("assemble_final_note", assemble_final_note)
    graph.add_node("save_to_obsidian", save_to_obsidian)

    graph.add_edge(START, "supervisor_agent")
    graph.add_edge("supervisor_agent", "dispatcher")

    graph.add_conditional_edges(
        "dispatcher",
        route_next_agent,
        {
            "notes_agent": "notes_agent",
            "research_agent": "research_agent",
            "quiz_agent": "quiz_agent",
            "coding_agent": "coding_agent",
            "reflection_agent": "reflection_agent",
        },
    )

    graph.add_edge("notes_agent", "dispatcher")
    graph.add_edge("research_agent", "dispatcher")
    graph.add_edge("quiz_agent", "dispatcher")
    graph.add_edge("coding_agent", "dispatcher")

    graph.add_edge("reflection_agent", "assemble_final_note")
    graph.add_edge("assemble_final_note", "save_to_obsidian")
    graph.add_edge("save_to_obsidian", END)

    return graph.compile()


def main():
    print("Multi-Agent Second Brain Orchestrator")
    print("-------------------------------------")

    task = input("Enter your task: ").strip()

    if not task:
        print("Task cannot be empty.")
        return

    initial_state: MultiAgentState = {
        "task": task,
        "plan": [],
        "completed_agents": [],

        "notes_context": "",
        "research_output": "",
        "quiz_output": "",
        "coding_output": "",
        "reflection_output": "",

        "final_note": "",
        "saved_path": "",
    }

    app = build_graph()
    result = app.invoke(initial_state)

    print("\nDone!")
    print(f"Saved note at: {result['saved_path']}")
    print("\nOpen Obsidian → 06-Advanced-Agent-Engineering → Multi-Agent Runs")


if __name__ == "__main__":
    main()