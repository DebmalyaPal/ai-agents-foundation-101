# Level 1: Simple Reflex Agent 🤖

The **Simple Reflex Agent** is the most foundational type of AI agent. It operates on a **condition-action** basis: it perceives its environment (user input) and reacts immediately based on current reasoning, without relying on past history or future planning.

---

## 🧠 How it Works

A Simple Reflex Agent follows a straightforward loop:
1. **Perception**: It receives a message from the user.
2. **Reasoning**: It passes the message to the LLM with a specific system prompt.
3. **Action**: It returns the generated response to the user.


## 🎯 Learning Objectives

In this level, we demonstrate:
- Basic project structure and `common/` utility imports.
- Secure API key handling via `.env`.
- The "Infinite Loop" pattern for agentic interaction.
- Containerization of a single-file agent.

## 🚀 Running the Agent

### Option 1: Using Python
From the project **root** directory:
```bash
python3 01_simple_reflex/agent.py
```

### Option 2: Using Docker
From the project **root** directory:
```bash
docker compose --profile reflex up
```

## 🛠️ Implementation Details

- **Model**: `llama-3.3-70b-versatile` (via Groq)
- **Shared Logic**: Uses `common/client.py` for unified LLM configuration.
- **Interactivity**: Uses Python's `input()` function to simulate an environment.

---

**Next Step:** Once we understand how this agent communicates, we head over to **Level 2: Tool User** to see how we give the agent "hands" to interact with the tools (eg. web, calculator, etc)!
