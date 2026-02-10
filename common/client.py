# common/client.py

# Import necessary libraries
import os
from dotenv import load_dotenv
from groq import Groq

# Load the .env file from the root directory
# This looks for .env in the current folder OR any parent folder
load_dotenv()

def get_groq_client():
    """Get the Groq client"""

    # Get the API key from the environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Raise an error if the API key is not found
        raise ValueError("API Key not found! Make sure .env is in the root.")
    
    # Return the Groq client
    return Groq(api_key=api_key)
