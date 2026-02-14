# Level 4: The Persistent Agent (Memory) 🧠

Until now, our agents have suffered from **Total Amnesia**. Every time the script restarted, the context was wiped clean. Level 4 introduces **Long-Term Persistence** using an SQLite backend.

---

## 🛠️ The Memory Architecture

We have moved beyond simple lists and implemented a **Data Access Object (DAO)** pattern in `common/database.py`. 

1. **Short-Term (Episodic)**: Managed via the LLM context window (the `messages` list).
2. **Long-Term (Persistent)**: Managed via SQLite. 

### Database Schema
We track every interaction with a `source_agent` tag to ensure **Provenance** across our monorepo levels.

## 🎯 Learning Objectives
- **Database Integration**: Connecting an LLM to a relational database.
- **Session Management**: Loading and saving history based on a `session_id`.
- **Context Management**: Fetching a specific "window" of history (e.g., the last 10 messages) to balance memory with token costs.
- **Provenance**: Tracking which agent generated which piece of data using the `source_agent` column.

## 🚀 Running the Agent

### Option 1: Local Setup
```bash
python3 04_memory_aware_agent/agent.py
```

### Option 2: Docker with Persistence
To keep your memory alive in Docker, we use a **Volume** to map the `data/` folder.
```bash
docker compose --profile memory_aware_agent run memory_aware_agent
```

---

## More about Agentic Memory

The flow of information typically follows this sequence to ensure the agent stays "grounded" in facts and context:
1. **Ingestion**: The user's query enters the system.  
2. **Contextual Retrieval**: The orchestrator queries Persistent Memory (Databases) to fetch External Semantic (facts) and Episodic (history) data.  
3. **Synthesis (Working Memory)**: The orchestrator assembles the System Prompt (Procedural) + Retrieved Data + History into the Context Window.  
4. **Generation**: The LLM processes the assembly using its Internal Parametric Semantic memory to produce a response.  
5. **Commitment**: The new interaction is saved back to Episodic/Persistent storage for future turns.  

### The Unified Memory Table
| Memory Category | Specific Type | Duration | Technical Implementation | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| Short-term | Working Memory | Minutes (Transient) | Context Window / RAM | Acts as the "scratchpad" for the current reasoning task. |
| Semantic | Internal (Parametric) | Permanent (Static) | Model Weights | General world knowledge and language skills learned during training. |
| Semantic | External (Non-Parametric) | Long-term (Dynamic) | Vector Database / RAG | Specific, private, or up-to-date facts stored outside the model. |
| Episodic | Session History | Variable | NoSQL / SQL Databases | Records specific past interactions or "episodes" with the user. |
| Procedural | Implicit / Explicit Skills | Permanent | System Prompts / Tool Registry | The "How-To" knowledge; rules, instructions, and API capabilities. |
| Persistent | Long-term Storage | Indefinite | Disk / Cloud Databases | The infrastructure that allows Episodic and External Semantic data to survive restarts. |


---
**Next Step:** Now that your agent has a memory, it's time to give it **Intelligence over Data**. Head to **Level 5: RAG (Retrieval-Augmented Generation)** to learn how to make the agent read your PDFs and text files!