# 02_single_tool_use/robust_agent.py

"""
Robust Tool User Agent

This agent is an improvement over the Single Tool User Agent because it uses the Groq API's native tool calling feature instead of manual JSON parsing.
"""

# Import necessary libraries
import sys
import os
import json

# Ensure the parent directory is in the path so we can import 'common'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Groq client and tools from the common package
from common.client import get_groq_client
from common.tools import search_web

# Use the latest Llama model optimized for tool use
MODEL = "llama-3.3-70b-versatile"

# 1. Define the tool schema (This replaces the manual JSON instructions)
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current events or unknown facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific search query to look up."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 2. Simplified System Prompt
SYSTEM_PROMPT = "You are a helpful Research Assistant. Use the search tool for facts you do not know."

def tool_user_agent():
    """
    This function is the main entry point for the tool user agent.
    It initializes the Groq client and the messages list.
    It follows a Condition-Action-Observation loop: "If I need info, I search, then I respond".
    It allows the agent to use tools to gather information and then respond to the user.
    """
    # Initialize the Groq client
    client = get_groq_client()
    # Initialize the messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("🛠️ Native Tool User Agent (Groq + Llama 3.3)")

    while True:
        # Get user input
        user_input = input("\n** User Input: ").strip()
        # Check if the user wants to exit
        if user_input.lower() in ["exit", "quit"]: break
        
        # Add user input to messages
        messages.append({"role": "user", "content": user_input})
        
        # Loop for the agent to think and act
        for _ in range(3):
            # 3. Pass the 'tools' parameter to the API
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto" # Model decides if it needs the tool
            )
            
            response_message = response.choices[0].message
            
            # 4. Check if the model wants to call a tool
            if response_message.tool_calls:
                # Loop through the tool calls
                for tool_call in response_message.tool_calls:
                    # Get the function name and arguments
                    function_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    print(f"🤖 Agent is calling '{function_name}' with: {args}...")
                    
                    # Execute the actual tool
                    if function_name == "search_web":
                        result = search_web(args['query'])
                        
                        # Add the assistant's call and the tool's response to history
                        messages.append(response_message)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": result
                        })
                continue # Let the LLM process the search result
            
            # 5. Final Answer
            else:
                final_answer = response_message.content
                print(f"\n** Agent Final Answer: {final_answer}")
                # Add the final answer to messages
                messages.append({"role": "assistant", "content": final_answer})
                break

if __name__ == "__main__":
    tool_user_agent()