from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn
import logging
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our custom utilities
from search_util import search_person_info
from ollama_util import get_ollama_response
from prompt_library import get_ollama_system_prompt, get_ollama_user_prompt

app = FastAPI(title="Startup Bully")

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Models for API requests
class PersonInfo(BaseModel):
    name: str
    company: Optional[str] = None
    github_username: Optional[str] = None
    startup_idea: str
    
class ValidationResponse(BaseModel):
    research: str
    feedback: str

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    # Return the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/validate", response_model=ValidationResponse)
async def validate_startup(
    name: str = Form(...),
    company: Optional[str] = Form(None),
    github_username: Optional[str] = Form(None),
    startup_idea: str = Form(...)
):
    try:
        logger.info(f"Received startup validation request for {name}")
        logger.info(f"Startup idea: {startup_idea}")
        logger.info(f"Company: {company}, GitHub: {github_username}")
        
        # Step 1: Research the person using search_util
        logger.info("Starting research on person's background...")
        research_result = search_person_info(
            name=name,
            company=company,
            github_username=github_username,
            startup_idea=startup_idea
        )
        logger.info(f"Research completed, found {len(research_result)} characters of information")
        
        # Step 2: Pass the research to Ollama for validation
        logger.info("Preparing system prompt for Ollama...")
        system_prompt = get_ollama_system_prompt(research_result)
        logger.info("System prompt (first 200 chars): " + system_prompt[:200] + "...")
        
        user_prompt = get_ollama_user_prompt(
            name=name,
            company=company,
            github_username=github_username,
            startup_idea=startup_idea
        )
        logger.info(f"User prompt: {user_prompt}")
        
        # Get model from environment variable or use default
        model = os.getenv('OLLAMA_MODEL', 'huihui_ai/qwen2.5-1m-abliterated:14b')
        logger.info(f"Using Ollama model: {model}")
        
        logger.info("Sending request to Ollama...")
        # Add a timestamp to avoid any caching issues
        user_prompt_with_timestamp = f"{user_prompt} [Request time: {time.time()}]"
        
        feedback = get_ollama_response(
            model=model,
            user_prompt=user_prompt_with_timestamp,
            system_prompt=system_prompt
        )
        logger.info(f"Received feedback from Ollama ({len(feedback)} characters)")
        logger.info("Feedback preview: " + feedback[:100] + "...")
        
        # Create structured log data
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'input_fields': {
                'name': name,
                'company': company,
                'github_username': github_username,
                'startup_idea': startup_idea
            },
            'search_response': research_result,
            'feedback_response': feedback
        }
        
        # Create logs directory if it doesn't exist
        logs_dir = 'logs'
        os.makedirs(logs_dir, exist_ok=True)
        
        # Generate a unique filename based on timestamp and name
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = ''.join(c if c.isalnum() else '_' for c in name).lower()
        log_filename = f"{timestamp_str}_{safe_name}.json"
        log_path = os.path.join(logs_dir, log_filename)
        
        # Save to individual JSON file
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Logged request and response data to {log_path}")
        
        return ValidationResponse(research=research_result, feedback=feedback)
        
    except Exception as e:
        logger.error(f"Error in validate_startup: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
