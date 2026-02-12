# common/tools.py
# Shared tools for agents

# Import the DDGS class from ddgs (DuckDuckGo Search)
from ddgs import DDGS

# Import numexpr for safe evaluation of mathematical expressions
import numexpr as ne


def search_web(query: str, max_results: int = 3) -> str:
    """
    Search the web using DuckDuckGo and return a concatenated string of snippets.
    """
    try:
        # We initialize without a context manager to manage retries if needed
        with DDGS() as ddgs:
            # use the 'text' method which is current for 2026
            results = list(ddgs.text(query, max_results=max_results))
            
            # If no results are found, return a message
            if not results:
                return f"No results found for '{query}'. Try a broader search term."
            
            # Format the results into a single string for the LLM to read
            formatted_results = []
            for i, r in enumerate(results, 1):
                # Using .get() with defaults is safer for agentic workflows
                title = r.get('title', 'No Title')
                body = r.get('body', 'No Content')
                href = r.get('href', '#')
                
                formatted_results.append(f"[{i}] {title}\nSource: {href}\nContent: {body}")
            
            # Return the formatted results
            return "\n\n".join(formatted_results)
    
    # If an error occurs, return an error message
    except Exception as e:
        # If it's a rate limit error, the agent should know to wait
        if "Ratelimit" in str(e):
            return "Error: Search rate limit hit. Please wait a moment before trying again."
        # If something else goes wrong, return the error message
        return f"Search Error: {str(e)}"


def calculator(expression: str) -> str:
    """Evaluates a mathematical expression safely."""
    try:
        # Using numexpr for safe evaluation
        result = ne.evaluate(expression)
        print(f"Expression: {expression} ------ Result: {result}")
        return str(result)
    except Exception as e:
        # If something else goes wrong, return the error message
        return f"Error: Could not evaluate expression. {str(e)}"
