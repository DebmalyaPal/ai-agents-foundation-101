# 02_tool_user/agent.py

"""
Single Tool User Agent

This agent is an improvement over the Simple Reflex Agent because it can use tools.
It follows a Condition-Action-Observation loop: "If I need info, I search, then I respond".
It still has no memory of past conversations.
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

# Define the model to be used
MODEL = "llama-3.3-70b-versatile" # https://console.groq.com/models

# Define the tools available to the agent
# In a 'from-scratch' agent, we tell the LLM about tools via the System Prompt
SYSTEM_PROMPT = """
You are a helpful Research Assistant with access to a search tool.
When you receive a question, you should follow this loop:

1. THOUGHT: Do I need to search the web to answer this?
2. ACTION: If yes, output a JSON object in this format: {"action": "search", "query": "your search query"}
3. OBSERVATION: You will receive the search results.
4. FINAL ANSWER: Once you have enough info, provide a clear response to the user.

Available Tools:
- search_web: Use this for current events or facts you don't know.

IMPORTANT: If you need to search, your entire response MUST be ONLY the JSON object.
"""

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
    messages = [{
        "role": "system", 
        "content": SYSTEM_PROMPT
    }]
    
    print("🛠️ Single Tool User Agent (Type 'exit' to stop)")

    while True:
        user_input = input("\n** User Input: ").strip()
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # --- THE AGENTIC LOOP ---
        # We allow up to 3 turns for the agent to "think and act"
        for _ in range(3):
            # Call the LLM to get the response
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            # Extract the content from the response
            ai_content = response.choices[0].message.content
            
            # Check if the AI wants to use a tool (is the response a JSON?)
            try:
                tool_call = json.loads(ai_content)
                # If the AI wants to use a tool, execute it
                if tool_call.get("action") == "search":
                    query = tool_call.get("query")
                    
                    # Execute the actual Python function from common/tools.py
                    observation = search_web(query)
                    
                    # Feed the result back to the LLM
                    messages.append({"role": "assistant", "content": ai_content})
                    messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})
                    
                    print(f"🤖 Agent is using tool 'search_web' for: '{query}'...")
                    continue # Loop back to let the LLM see the search results
            
            # If it's not JSON, it's the Final Answer
            except json.JSONDecodeError:
                print(f"\n** Agent Final Answer: {ai_content}")
                print("\n---- END OF QUERY ----\n")
                messages.append({"role": "assistant", "content": ai_content})
                break
            # If there is any other error, break the loop
            except Exception as e:
                print(f"\nAgent Error: {str(e)}")
                messages.append({"role": "assistant", "content": ai_content})
                break

if __name__ == "__main__":
    tool_user_agent()