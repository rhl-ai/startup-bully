from google import genai
from google.genai import types
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv
from prompt_library import get_search_prompt

# Load environment variables
load_dotenv()

def search_person_info(
    name: str,
    company: Optional[str] = None,
    github_username: Optional[str] = None,
    startup_idea: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Search for information about a person using Google's Gemini API.
    
    Args:
        name: The name of the person to search for
        company: Optional company where the person works
        github_username: Optional GitHub username
        startup_idea: Optional startup idea to research further
        api_key: Google Gemini API key
        
    Returns:
        A string with the compiled research about the person and their startup idea
    """
    # Get API key from environment variable if not provided
    if api_key is None:
        api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyANSQsad1NsXNIeUkSYbxwUjzKvF8BuGZk')
    
    client = genai.Client(api_key=api_key)
    # Get model from environment variable or use default
    model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # Get search prompt from the prompt library
    search_text = get_search_prompt(
        name=name,
        company=company,
        github_username=github_username,
        startup_idea=startup_idea
    )
    
    # Set up the search request
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=search_text),
            ],
        ),
    ]
    
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
    )
    
    # Make the API call and get the response
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    return response.text

if __name__ == "__main__":
    # Example usage
    result = search_person_info(
        name="John Doe",
        company="Example Corp",
        github_username="johndoe",
        startup_idea="AI-powered coffee delivery service"
    )
    print(result)
