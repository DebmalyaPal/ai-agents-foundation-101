# common/database.py

"""
Database Module

This module handles all interactions with the SQLite database.
It provides functions to initialize the database, save messages, retrieve chat history, and clear history.
"""

# Import required libraries
import sqlite3
import os

# Ensure there is a 'data' directory at the project root - if not, create it
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "agents.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name (e.g. row['role'])
    conn.row_factory = sqlite3.Row
    return conn

"""
Schema Structure
Table: chat_history
  id          : INTEGER PRIMARY KEY AUTOINCREMENT : Auto-incrementing primary key
  source_agent: TEXT NOT NULL                     : Source agent name (e.g. 04_memory_agent, etc.)
  session_id  : TEXT NOT NULL                     : Session ID
  role        : TEXT NOT NULL                     : Role (e.g. user, assistant, system)
  content     : TEXT NOT NULL                     : Content of the message
  timestamp   : DATETIME DEFAULT CURRENT_TIMESTAMP: Timestamp of the message
"""
def initialize_db() -> None:
    """Creates the necessary tables if they don't exist."""
    # Connect to the database and create a cursor
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create a table for chat history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_agent TEXT NOT NULL,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def save_message(source_agent: str, session_id: str, role: str, content: str) -> None:
    """Saves a single message to the database."""
    # Connect to the database and create a cursor
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert the message into the chat history table
    cursor.execute(
        "INSERT INTO chat_history (source_agent, session_id, role, content) VALUES (?, ?, ?, ?)",
        (source_agent, session_id, role, content)
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_chat_history(session_id: str, limit: int = 10) -> list[dict]:
    """Retrieves the last N messages for a specific session."""
    # Connect to the database and create a cursor
    conn = get_connection()
    cursor = conn.cursor()
    
    # Retrieve the last N messages for the session
    cursor.execute(
        "SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
        (session_id, limit)
    )
    # We reverse the list so it's in chronological order for the LLM
    rows = cursor.fetchall()
    conn.close()
    
    # Convert the rows to a list of dictionaries
    history = [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
    return history

def clear_history(session_id: str) -> None:
    """Wipes the history for a specific session."""
    # Connect to the database and create a cursor
    conn = get_connection()
    cursor = conn.cursor()
    
    # Delete the chat history for the session
    cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("🚀 Initializing Database...")
    initialize_db()
    print(f"✅ Database ready at {DB_PATH}")