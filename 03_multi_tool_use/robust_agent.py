# 03_multi_tool_use/robust_agent.py

"""
Robust Multi-Tool User Agent

This agent implements the ReAct (Reason + Act) pattern using multiple tools.
It can chain actions together (e.g., search for a price, then calculate tax).
It maintains a temporary session context but still lacks persistent memory.

This agent improves upon the manual JSON parsing by using Groq's native 'tool use' API.
It defines a schema for both 'search_web' and 'calculator', allowing the LLM to 
intelligently select and execute the correct tool with strict parameter adherence.
"""

# Import necessary libraries
import sys
import os
import json

# Ensure the parent directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Groq client and the expanded toolset from the common package
from common.client import get_groq_client
from common.tools import search_web, calculator

# Define the model to be used
MODEL = "llama-3.3-70b-versatile"

# 1. Define the Native Tool Schema
# We describe BOTH tools here so the LLM knows its full capability.
tools_schema = [
    # Define the search_web tool
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current events, news, or unknown facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    # Define the calculator tool
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression. Use this for ANY math calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate (e.g., '2 * 3', 'sqrt(16)')."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 2. Simplified System Prompt
# We don't need to explain JSON formatting anymore; the API handles it.
SYSTEM_PROMPT = """
You are a Multi-Tool Research Assistant. 
You have access to a search engine and a calculator.
- Use 'search_web' for current events, facts, or information you don't know.
- Use 'calculator' for any math calculations, even simple ones, to ensure accuracy.
If you need to perform a sequence of actions (like search then calculate), do them one by one.
"""

def robust_multi_tool_agent():
    """
    Orchestrates the ReAct loop for multiple tools.
    Allows up to 5 iterations to support multi-step problem solving.
    Uses the 'tools' parameter in Groq API for reliable function calling.
    """
    # Initialize the Groq client
    client = get_groq_client()
    
    # Initialize the conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("🛠️ Robust Multi-Tool Agent (Native Groq API) (Type 'exit' to stop)")

    while True:
        # Step 1: Get user input
        user_input = input("\n** User Input: ").strip()
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        # Step 2: Add user input to the messages list
        messages.append({"role": "user", "content": user_input})
        
        # --- THE MULTI-STEP AGENTIC LOOP ---
        # Increased to 5 turns to allow for complex 'Search -> Calculate' chains
        for step in range(5):
            try:
                # Step 3: Call the API with the tools definition
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools_schema,
                    tool_choice="auto", # Let the model decide
                    max_tokens=4096
                )
                
                # Get the response message and tool calls
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                # Step 4. Check if the model wants to call a tool (if so, it will be in tool_calls)
                if tool_calls:
                    # Append the model's "intent" message to history (required by API)
                    messages.append(response_message)

                    # Iterate over all tool calls (the model might want to call multiple at once)
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"🤖 Step {step+1}: Calling '{function_name}' with {function_args}...")
                        
                        # --- THE ROUTER ---
                        # Step 5: Call the tool if it exists
                        tool_result = ""
                        if function_name == "search_web":
                            tool_result = search_web(function_args.get("query"))
                        elif function_name == "calculator":
                            tool_result = calculator(function_args.get("expression"))
                        else:
                            tool_result = f"Error: Tool {function_name} not found."

                        # Step 6: Append the Tool Output (Observation)
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": tool_result,
                        })
                    
                    # Continue the loop to let the LLM process the result
                    continue
                
                # Step 7: If no tool calls, this is the final answer
                else:
                    final_answer = response_message.content
                    print(f"\n** Agent Final Answer: {final_answer}")
                    print("\n---- END OF QUERY ----\n")

                    messages.append({"role": "assistant", "content": final_answer})
                    break
            
            except Exception as e:
                # Step 8: If there is any other error, break the loop
                print(f"Error during agent execution: {e}")
                messages.pop()
                break

if __name__ == "__main__":
    robust_multi_tool_agent()