 # Level 2: The Tool User (ReAct) 🛠️

While the Level 1 agent relied solely on its internal training data, the **Single Tool User** agent can interact with the outside world. It follows the **ReAct** (Reason + Act) pattern to solve tasks it cannot answer alone.

---

## 🧠 The Agentic Loop: ReAct

This agent is programmed to follow a specific "Loop of Thought":
1. **Thought**: The agent analyzes the user prompt to see if external data is needed.
2. **Action**: If needed, it generates a structured **JSON** command to trigger a tool.
3. **Observation**: Our Python "orchestrator" runs the tool and feeds the results back.
4. **Final Answer**: The agent combines its reasoning with the tool's output for the user.

---

## 🎯 Learning Objectives

In this level, we demonstrate:
- **Tool Binding**: Teaching an LLM how to use a Python function.
- **JSON Parsing**: Handling structured outputs from an LLM.
- **Iterative Loops**: Managing multiple "turns" of conversation before giving an answer.
- **Web Interaction**: Using the `duckduckgo-search` library as an agent tool.

---

## 🚀 Running the Agent

### Option 1: Using Python (Without Docker - Use Virtual Environment & Requirements.txt)
From the project **root** directory (where the `compose.yaml` file is located):
```bash
python3 02_single_tool_use/agent.py
```

### Option 2: Using Docker
From the project **root** directory (where the `compose.yaml` file is located):
```bash
docker compose --profile single-tool run single_tool_agent
```

---

## 🛠️ Implementation Details

- **Tooling**: `common/tools.py` (DuckDuckGo Search).
- **Strategy**: Manual ReAct loop (without a framework like LangChain).
- **Prompting**: Role-based system instructions with few-shot JSON examples.

---

**Next Step:** Now that your agent has "hands" but it can only use one tool (or do single external actions), head over to **Level 3: Multi-Tool Use** to learn how to make agents use multiple tools!