# 03_multi_tool_use/agent.py

"""
Multi-Tool User Agent

This agent implements the ReAct (Reason + Act) pattern using multiple tools.
It can chain actions together (e.g., search for a price, then calculate tax).
It maintains a temporary session context but still lacks persistent memory.
"""

# Import necessary libraries
import sys
import os
import json

# Ensure the parent directory is in the path so we can import 'common'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Groq client and the expanded toolset from the common package
from common.client import get_groq_client
from common.tools import search_web, calculator

# Define the model to be used
MODEL = "llama-3.3-70b-versatile"

# Enhanced System Prompt to handle tool discrimination
SYSTEM_PROMPT = """
You are a Multi-Tool Assistant. You have access to:
1. search_web: Use this for current events, facts, or information you don't know.
2. calculator: Use this for ANY math calculations, even simple ones, to ensure accuracy.

When you receive a question, follow this loop:
1. THOUGHT: Reason about what information is missing.
2. ACTION: If you need a tool, output ONLY a JSON: {"tool": "search_web" or "calculator", "input": "your_query"}
3. OBSERVATION: You will receive the result from the tool.
4. FINAL ANSWER: Once you have all data, provide a clear response to the user.

IMPORTANT: If you need a tool, your entire response MUST be ONLY the JSON object.
"""

def multi_tool_agent():
    """
    Orchestrates the ReAct loop for multiple tools.
    Allows up to 5 iterations to support multi-step problem solving.
    """
    # Initialize the Groq client
    client = get_groq_client()
    
    # Initialize the messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    print("🛠️ Multi-Tool Agent Online (Type 'exit' to stop)")

    while True:
        # Step 1. Get User Input
        user_input = input("\n** User Input: ").strip()

        # Exit if user types 'exit'
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        # Step 2. Add user input to the messages list
        messages.append({"role": "user", "content": user_input})
        
        # --- THE MULTI-STEP AGENTIC LOOP ---
        # Increased to 5 turns to allow for complex 'Search -> Calculate' chains
        for step in range(5):
            try:
                # Step 3. Get the response from the LLM
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages
                )
                
                # Get the content from the response
                ai_content = response.choices[0].message.content
                
                # Step 4. Try to parse tool call
                tool_call = extract_json(ai_content)

                # If tool_call is not None, then it is a tool call
                if tool_call:
                    tool_name = tool_call.get("tool")
                    tool_input = tool_call.get("input")
                    
                    print(f"🤖 Step {step+1}: Using {tool_name} for '{tool_input}'...")

                    if tool_name == "search_web":
                        observation = search_web(tool_input)
                    elif tool_name == "calculator":
                        observation = calculator(tool_input)
                    else:
                        observation = f"Error: Tool '{tool_name}' not found."
                    
                    # Feedback loop
                    messages.append({"role": "assistant", "content": ai_content})
                    messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})
                    continue # Loop back to let the LLM see the result

                # If no JSON was found, assume it's the Final Answer
                else:
                    print(f"\n** Agent Final Answer: {ai_content}")
                    print("\n---- END OF QUERY ----\n")
                    messages.append({"role": "assistant", "content": ai_content})
                    break
                
            except Exception as e:
                # Step 6. If there is any other error, break the loop
                print(f"\nAgent Error: {str(e)}")
                break

def extract_json(text):
    """
    Extracts the first valid JSON object from a string, 
    even if it is surrounded by other text.
    """
    try:
        # Try direct parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        # If that fails, look for the first '{' and the last '}'
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end])
            except:
                return None
        return None

if __name__ == "__main__":
    multi_tool_agent()



"""
--- ERROR LOG & FIX ---

ERROR: "Chatty Agent" JSONDecodeError
-------------------------------------
The Agent often failed with a JSONDecodeError because the LLM would output conversational text 
alongside the JSON command (e.g., "Sure, I can calculate that! {"tool": "calculator"...}"). 
The standard json.loads() function expects a string containing *only* valid JSON and crashes 
on the extra text.

SOLUTION: Dynamic JSON Extraction
--------------------------------
We replaced the simple json.loads() with a helper function 'extract_json(text)'.
1. It first tries to parse the text as-is.
2. If that fails, it scans the string for the first '{' and the last '}' characters.
3. It extracts the substring between those indices and attempts to parse it again.

This allows the Agent to be "conversational" (chatty) while still executing tool calls reliably.
"""