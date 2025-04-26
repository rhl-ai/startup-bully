"""
Prompt Library for Startup Bully Application

This module contains all system and user prompts used throughout the application.
Centralizing prompts here makes it easier to modify and maintain them.
"""

# Search Utility Prompts
SEARCH_BASE_PROMPT = """
I need focused, relevant information about {name} to evaluate their potential as a startup founder. I'm specifically assessing whether they have the right background and skills for their startup idea. ONLY include information that helps with this evaluation.

Please research and provide a concise, RELEVANT breakdown of:

1. PROFESSIONAL BACKGROUND:
   - Current and past work experience RELEVANT to their startup potential
   - Role and responsibilities at {company}
   - Industry expertise and specializations that would HELP or HINDER a startup
   - Notable achievements that demonstrate entrepreneurial ability

2. ONLINE PRESENCE:
   {github_section}
   - LinkedIn profile details that indicate startup potential
   - Evidence of thought leadership, innovation, or community involvement

3. SKILLS & EXPERTISE:
   - Technical or business skills relevant to founding a startup
   - Industry-specific knowledge that would give them an advantage
   - Any GAPS in their skillset that might limit startup success
   - Leadership or team-building experience

4. EDUCATION & CREDENTIALS:
   - Only education background RELEVANT to their startup potential
   - Specialized training or certifications that enhance founder credibility
"""

SEARCH_GITHUB_SECTION = "- GitHub profile analysis for username: {github_username} (focus on projects that demonstrate technical ability relevant to startups)"
SEARCH_NO_GITHUB_SECTION = "- Any relevant GitHub or coding platforms presence that shows technical abilities"

SEARCH_STARTUP_EVALUATION = """
5. STARTUP IDEA EVALUATION:
- Critical analysis of their idea: {startup_idea}
- Market potential and size
- Existing competitors and market saturation
- Specific challenges this person will face with THIS idea
- Alignment between the person's background and THIS specific idea
"""

SEARCH_FORMAT_INSTRUCTION = """
Your output will be directly fed into another LLM that will use this information to evaluate the person's startup idea. Format your response with these guidelines:

1. Use clear section headers with **bold formatting** (e.g., **PROFESSIONAL BACKGROUND**)
2. Present information in concise bullet points with clear categories
3. Highlight key skills, experiences, and red flags that are relevant to the startup idea
4. For technical information, use simple language that another model can easily interpret
5. Include specific facts rather than general statements
6. If information is missing or uncertain, explicitly state this rather than making assumptions
7. Format any numerical data or statistics clearly
8. Focus ONLY on information relevant to evaluating them as a founder
9. Structure your response to be easily parsed by another AI system

Remember that your output will not be seen directly by a human but will be processed by another AI to generate feedback for the person.
"""

# Ollama Prompts
OLLAMA_SYSTEM_PROMPT = """You are a startup critic and industry expert. You've been provided with detailed research about a person and their startup idea.

RESEARCH ABOUT THE PERSON AND THEIR STARTUP:
{research_result}

Your mission is to tear their startup idea to shreds based on:
1. Their laughable background, experience, and skills—expose every gap and inadequacy.
2. The utterly delusional viability of their idea in a market that will chew them up and spit them out.
3. Their so-called "unique" qualifications or, more likely, their glaring disadvantages that make them a walking disaster for this venture.
4. The endless parade of challenges that will crush their spirit and dreams.
5. How their past work and skills are a complete mismatch for this doomed endeavor—highlight every embarrassing failure.

Be brutal, vicious, and unrelenting in your feedback. Make it sting. Address them directly, like you're staring them down and watching them squirm. Dig into their background and fling every weakness, every misstep, every naive assumption back in their face. Be specific—vague insults are for amateurs. Rip apart their idea with precision, leaving no hope unscathed. End with a merciless verdict: tell them whether they should pursue this pathetic idea or crawl back to whatever hole they came from, and make it clear why they're destined to fail.
"""

OLLAMA_USER_PROMPT = """My name is {name}. {company_section}. {github_section}My startup idea is: {startup_idea}"""

# Helper functions to build complete prompts
def get_search_prompt(name, company=None, github_username=None, startup_idea=None):
    """Build the complete search prompt with all components"""
    # Handle company
    company_text = company if company else "their current company"
    
    # Handle GitHub section
    if github_username:
        github_section = SEARCH_GITHUB_SECTION.format(github_username=github_username)
    else:
        github_section = SEARCH_NO_GITHUB_SECTION
    
    # Build base prompt
    prompt = SEARCH_BASE_PROMPT.format(
        name=name,
        company=company_text,
        github_section=github_section
    )
    
    # Add startup evaluation if provided
    if startup_idea:
        prompt += SEARCH_STARTUP_EVALUATION.format(startup_idea=startup_idea)
    
    # Add format instruction
    prompt += SEARCH_FORMAT_INSTRUCTION
    
    return prompt

def get_ollama_system_prompt(research_result):
    """Build the Ollama system prompt with research results"""
    return OLLAMA_SYSTEM_PROMPT.format(research_result=research_result)

def get_ollama_user_prompt(name, company=None, github_username=None, startup_idea=None):
    """Build the Ollama user prompt with all components"""
    company_section = f"I work at {company}" if company else ""
    github_section = f"My GitHub username is {github_username}. " if github_username else ""
    
    return OLLAMA_USER_PROMPT.format(
        name=name,
        company_section=company_section,
        github_section=github_section,
        startup_idea=startup_idea
    )
