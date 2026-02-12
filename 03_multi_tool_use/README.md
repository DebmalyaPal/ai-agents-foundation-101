# Level 3: Multi-Tool Agent 🧰

The **Multi-Tool Agent** represents a significant leap in complexity. While Level 2 could use a single tool, Level 3 introduces the concept of **Routing** and **Chaining**. The agent must now evaluate a "menu" of available tools and decide which one (if any) is appropriate for the current step of the problem.

---

## 🧠 How it Works: The Router Pattern

The agent operates on an expanded **ReAct** loop. In the **Thought** phase, it doesn't just ask "Do I need a tool?", but "Which tool do I need?".

1. **User Input**: "How much is 500 USD in INR?"
2. **Router (LLM)**: Analyzes the request.
   - *Is it a general fact?* -> Answer directly.
   - *Is it a live event?* -> Use `search_web` tool.
   - *Is it a math problem?* -> Use `calculator` tool.
3. **Action**: The agent selects a tool and generates the specific input for it.
4. **Observation**: The Python script executes the tool and returns the result.
5. **Loop**: The agent can repeat this process (Chain of Thought) until the task is done.


## 🎯 Learning Objectives

In this level, we demonstrate:
- **Tool Discrimination**: Teaching the LLM to choose the right tool for the job.
- **Multi-Step Reasoning**: Handling tasks that require a sequence of actions (e.g., Search -> Calculate).
- **Safe Execution**: Using libraries like `numexpr` for safe mathematical evaluation.
- **Error Handling**: What happens when a tool fails or the LLM asks for a non-existent tool.

## 🧪 Example Test Cases

### Case 1: No Tool Use (Direct Answer)
**User**: "Who wrote 'Hamlet'?"  
**Agent (Thought)**: *Recognizes this is general knowledge.*  
**Agent (Final Answer)**: Returns "William Shakespeare" immediately without calling any tool.

### Case 2: Single Tool Use
**User**: "What is 12,345 divided by 67?"  
**Agent (Thought)**: *Recognizes a math problem.*  
**Action**: Calls `calculator("12345 / 67")`.  
**Observation**: Returns the precise number.  
**Agent (Final Answer)**: "12,345 divided by 67 is 182."

### Case 3: Multi-Tool Chaining (The "Power" Move)
**User**: "Tell me how much does 5 Bitcoins cost today?"  
**Agent (Step 1)**: Agent calls `search_web("current bitcoin price")`.  
**Observation**: "Bitcoin is $95,000."  
**Agent (Step 2)**: Agent calls `calculator("95000 * 5")`.  
**Observation**: "475000".  
**Agent (Final Answer)**: "5 Bitcoins would cost $475,000."



## 🚀 Running the Agent

### Option 1: Using Python
From the project **root** directory:
```bash
python3 03_multi_tool_use/agent.py
```

### Option 2: Using Docker
First, ensure you have built the image (or use the --build flag):
```bash
docker compose --profile multi-tool run multi_tool_agent
```

## 🛠️ Implementation Details

- **Tools**:
    - @search_web@: Uses `duckduckgo-search` (ddgs) for live web data.
    - @calculator@: Uses `numexpr` for safe string-based math evaluation.
- **Max Loop Depth**: 5 iterations (allows for complex chains).
- **System Prompt**: Explicitly lists available tools and their specific use cases to guide the LLM's decision-making.

---

**Next Step:** The agent is smart, but it has **Short-Term Memory Loss**. If you restart the script, it forgets everything. Head over to **Level 4: Memory & Database** to give the agent a long-term brain!