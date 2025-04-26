import requests
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ollama_response(
    model: str,
    user_prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    host: Optional[str] = None
) -> str:
    """
    Get a response from Ollama by providing system and user prompts.
    
    Args:
        model: The name of the model to use (e.g., 'llama3.2')
        user_prompt: The user's message content
        system_prompt: Optional system prompt to set context/behavior
        temperature: Optional temperature parameter (0.0 to 1.0)
        host: The host URL for Ollama (default: http://localhost:11434)
        
    Returns:
        The text content of the assistant's response
    """
    # Get host from environment variable if not provided
    if host is None:
        host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    # Create messages array
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    
    # Create request payload
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    # Add temperature if provided
    if temperature is not None:
        if "options" not in payload:
            payload["options"] = {}
        payload["options"]["temperature"] = temperature
        
    # Create API endpoint URL and send request
    url = f"{host}/api/chat"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    response_data = response.json()
    
    # Return the content of the response
    return response_data["message"]["content"]
