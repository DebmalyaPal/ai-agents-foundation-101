# 01_simple_reflex/agent.py

"""
Simple Reflex Agent

This is the most basic form of an AI agent. It follows a simple 
Condition-Action rule: "If the user says X, I say Y".
It has no memory of past conversations and cannot use tools.
"""

# Import necessary libraries
import sys
import os

# Ensure the parent directory is in the path so we can import 'common'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the client from the common module
from common.client import get_groq_client

# Define the model to be used
MODEL = "llama-3.3-70b-versatile" # https://console.groq.com/models


def simple_reflex_agent():
    # Define the agent function

    # Step 1: Initialize the "Brain"
    client = get_groq_client()
    
    print("🤖 Simple Reflex Agent is online. (Type 'exit' to stop)")
    
    while True:
        # Step 2: Perception: Get input from the environment (the user)
        user_msg = input("User: ")
        
        if user_msg.lower() in ["exit", "quit"]:
            break
            
        # Step 3: Action: Send to LLM and get a response
        # The "Condition-Action" rule is: "If user speaks, respond helpfully"
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a simple reflex agent. Your goal is to respond clearly and concisely."
                },
                {
                    "role": "user", 
                    "content": user_msg
                }
            ]
        )
        
        # Step 4: Actuation: Output the result to the environment
        print(f"Agent: {completion.choices[0].message.content}\n")

if __name__ == "__main__":
    simple_reflex_agent()