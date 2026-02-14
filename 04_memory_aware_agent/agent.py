# 04_memory_aware_agent/agent.py

"""
Memory-Enabled Agent

This agent uses SQLite to persist conversation history across sessions.
It can remember data from past interactions even after a restart.
"""

# Import required libraries
import sys
import os

# Path setup to import from 'common'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Groq client and the database functions
from common.client import get_groq_client
from common.database import initialize_db, save_message, get_chat_history, clear_history

# Define the model to be used
MODEL = "llama-3.3-70b-versatile"


def memory_aware_agent():
    """
    Orchestrates the memory agent loop.
    """
    # 1. Setup the Database
    initialize_db()

    # Initialize the Groq client
    client = get_groq_client()
    
    print("🧠 Memory Aware Agent (Type 'exit' to stop)")
    
    # 2. Identify the User ('Session Management')
    user_name = input("Enter your name to load your history: ").strip().lower()
    session_id = f"user_{user_name}"
    
    # 3. Fetch past history from SQLite
    # We pull the last 10 messages to keep the context clean
    past_history = get_chat_history(session_id, limit=10)
    
    # Initialize the session with System Prompt + Past History
    messages = [
        {
            "role": "system", 
            "content": f"You are a helpful assistant. The user's name is {user_name}."
        }
    ]
    
    # 4. Greet the user based on history
    if past_history:
        print(f"✨ Welcome back, {user_name}! I remember our last conversation. \n")
        
        # Ask user if they want to continue where they left off
        user_response = input("Do you want to continue where we left off? (yes/no): ").strip().lower()
        
        # If user wants to start a fresh session, delete the previous session
        if user_response == "no":
            clear_history(session_id)
            past_history.clear()
            print(f"👋 Hello {user_name}! Starting a new session.")
        else:
            print(f"\nContinuing our last conversation...")
    else:
        print(f"👋 Hello {user_name}! Nice to meet you.")
    
    messages.extend(past_history)
    
    print("\n" + "="*50)

    # 5. Main Conversation Loop
    while True:
        # Get user input
        user_input = input(f"\n[{user_name}]: ").strip()
        
        # Exit if user types 'exit'
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        # Save User message to DB and add to messages list
        save_message(source_agent='04_memory_agent', session_id=session_id, role="user", content=user_input)
        messages.append({"role": "user", "content": user_input})
        
        # Get response from LLM
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        
        # Get AI response
        ai_reply = response.choices[0].message.content
        print(f"\n[Agent]: {ai_reply}")
        
        # Save AI response to DB and add to messages list
        save_message(source_agent='04_memory_agent', session_id=session_id, role="assistant", content=ai_reply)
        messages.append({"role": "assistant", "content": ai_reply})

if __name__ == "__main__":
    memory_aware_agent()