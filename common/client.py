# common/client.py

# Import necessary libraries
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

def get_groq_client():
    """Get the Groq client with robust path handling"""

    # 1. Check if the key is ALREADY in the environment (e.g., from Docker Compose)
    api_key = os.getenv("GROQ_API_KEY")

    # 2. If not found, try loading from the .env file (for local development)
    if not api_key:
        # 2.1. Get the absolute path of this file (common/client.py)
        # 2.2. Go up one level to the root of the project
        base_dir = Path(__file__).resolve().parent.parent
        env_path = base_dir / ".env"

        # 2.3. Explicitly load the .env from the calculated path
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

            # 2.4. Get the API key from the environment
            api_key = os.getenv("GROQ_API_KEY")

    # 3. If the API key is still not found, raise an error
    if not api_key:
        raise ValueError("API Key not found! Make sure .env is in the root.")
    
    # 4. Print API Key initialization status
    print("API Key initialized successfully!")

    # Return the Groq client
    return Groq(api_key=api_key)
