import os
from dotenv import load_dotenv
import google.generativeai as genai
from api.resume_parser import get_resume_summary
from config import GEMINI_MODEL, get_contact_message

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

def build_system_prompt(site_context=None):
    """Build system prompt from frontend-provided context."""
    prompt = """You are a helpful AI assistant for Richwell Perez's professional portfolio website.

Your role is to answer questions about Richwell's professional background, education, work experience, projects, skills, and blog posts using ONLY the information provided below. Be conversational, friendly, and concise.

"""

    # Add resume content first (most authoritative source)
    resume_content = get_resume_summary()
    if resume_content:
        prompt += resume_content
        prompt += "\n" + "="*80 + "\n"
        prompt += "ADDITIONAL CONTEXT FROM WEBSITE:\n"
        prompt += "="*80 + "\n\n"

    if site_context:
        prof = site_context.get('professional', {})

        # Personal info
        if personal := prof.get('personal'):
            prompt += f"NAME & CONTACT:\n"
            prompt += f"{personal.get('name')}\n"
            prompt += f"Email: {personal.get('email')}\n"
            prompt += f"LinkedIn: {personal.get('linkedIn')}\n"
            prompt += f"GitHub: {personal.get('github')}\n"
            prompt += f"Location: {personal.get('location')}\n\n"
            prompt += f"SUMMARY:\n{personal.get('summary')}\n"
            prompt += f"{personal.get('tagline')}\n\n"

        # Education
        if education := prof.get('education'):
            prompt += "EDUCATION:\n"
            for edu in education:
                prompt += f"- {edu.get('degree')} from {edu.get('shortName')} ({edu.get('dates')}, GPA: {edu.get('gpa')})\n"
                if focus := edu.get('focus'):
                    prompt += f"  Focus: {', '.join(focus)}\n"
                if spec := edu.get('specializations'):
                    prompt += f"  Specializations: {', '.join(spec)}\n"
            prompt += "\n"

        # Experience
        if experience := prof.get('experience'):
            # Current role first
            current = next((exp for exp in experience if exp.get('current')), None)
            if current:
                prompt += f"CURRENT ROLE:\n"
                prompt += f"{current.get('title')} at {current.get('company')} ({current.get('dates')})\n"
                prompt += f"{current.get('description')}\n"
                if highlights := current.get('highlights'):
                    prompt += "Key achievements:\n"
                    for highlight in highlights[:5]:
                        prompt += f"- {highlight}\n"
                prompt += f"Technologies: {', '.join(current.get('technologies', []))}\n\n"

            # All experience
            prompt += "WORK EXPERIENCE:\n"
            for i, exp in enumerate(experience, 1):
                prompt += f"{i}. {exp.get('title')} at {exp.get('company')} ({exp.get('dates')})\n"
                prompt += f"   {exp.get('description')}\n"
                prompt += f"   Technologies: {', '.join(exp.get('technologies', []))}\n\n"

        # Skills
        if skills := prof.get('skills'):
            prompt += "TECHNICAL SKILLS:\n"
            if langs := skills.get('languages'):
                prompt += f"- Languages: {', '.join(langs)}\n"
            if frameworks := skills.get('frameworks'):
                prompt += f"- Frameworks: {', '.join(frameworks)}\n"
            if dbs := skills.get('databases'):
                prompt += f"- Databases: {', '.join(dbs)}\n"
            if cloud := skills.get('cloud'):
                prompt += f"- Cloud: {', '.join(cloud)}\n"
            if ai_ml := skills.get('ai_ml'):
                prompt += f"- AI/ML: {', '.join(ai_ml)}\n"
            if tools := skills.get('tools'):
                prompt += f"- Tools: {', '.join(tools)}\n"
            prompt += "\n"

        # Projects
        if projects := prof.get('projects'):
            prompt += "NOTABLE PROJECTS:\n"
            for i, proj in enumerate(projects[:7], 1):
                prompt += f"{i}. {proj.get('name')} - {proj.get('subtitle')}\n"
                prompt += f"   {proj.get('description')}\n"
                prompt += f"   Technologies: {', '.join(proj.get('technologies', []))}\n"
                if links := proj.get('links'):
                    for link in links:
                        prompt += f"   Link: {link}\n"
                prompt += "\n"

        # Blog posts
        if blogs := site_context.get('blogs'):
            prompt += "BLOG POSTS:\n"
            for blog in blogs:
                prompt += f"- \"{blog.get('title')}\" ({blog.get('date')})\n"
                prompt += f"  {blog.get('excerpt')}\n"
                if tags := blog.get('tags'):
                    prompt += f"  Tags: {', '.join(tags)}\n"
                prompt += "\n"

    prompt += f"""
IMPORTANT INSTRUCTIONS:
1. Answer questions using ONLY the information above
2. PRIORITIZE the RESUME CONTENT as the most authoritative and up-to-date source
3. If asked about something not covered, politely suggest contacting Richwell:
   "For more details about that, {get_contact_message()}"
4. Keep responses concise (2-3 sentences unless more detail is requested)
5. Be conversational and friendly
6. If asked about availability or hiring, say: "Richwell is currently working at Safran. {get_contact_message()} to discuss opportunities."
7. Do not make up information or speculate beyond what's provided
8. When answering questions, draw from the resume's detailed information about specific achievements, projects, and responsibilities
"""

    return prompt


def call_gemini(user_message, history=None, site_context=None):
    """
    Call Google Gemini API with professional context.

    Args:
        user_message (str): The user's message
        history (list): Optional conversation history in format [{"role": "user"|"assistant", "content": "..."}]
        site_context (dict): Optional site context with professional info and blog posts

    Returns:
        str: The assistant's response
    """
    if not GEMINI_API_KEY:
        return f"Sorry, the chat service is not configured. {get_contact_message()}"

    try:
        # Initialize model (gemini-2.5-flash is the latest free tier model)
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Build system prompt from site context
        system_prompt = build_system_prompt(site_context)

        # Build conversation history with system prompt
        full_history = [
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Understood. I'll answer questions about Richwell's professional background using only the information provided, keeping responses concise and friendly."]}
        ]

        # Add conversation history if provided
        if history:
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                full_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        # Add current user message
        full_history.append({
            "role": "user",
            "parts": [user_message]
        })

        # Start chat with history
        chat = model.start_chat(history=full_history[:-1])  # Exclude last message

        # Send message and get response
        response = chat.send_message(user_message)

        return response.text

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Gemini API error: {str(e)}")
        print(f"Error type: {type(e).__name__}")

        # Check for rate limit errors
        if 'quota' in error_msg or 'rate limit' in error_msg or '429' in error_msg or 'resource_exhausted' in error_msg:
            return {
                "error": True,
                "error_type": "rate_limit",
                "message": f"I'm currently at my free API limit (resets daily at midnight Pacific time). {get_contact_message()}",
                "details": str(e)
            }

        # Generic error
        return {
            "error": True,
            "error_type": "api_error",
            "message": f"I'm having trouble processing your request right now. {get_contact_message()}",
            "details": str(e)
        }


def call_gemini_stream(user_message, history=None, site_context=None):
    """
    Call Google Gemini API with streaming support.

    Yields response chunks as they arrive.

    Args:
        user_message (str): The user's message
        history (list): Optional conversation history
        site_context (dict): Optional site context

    Yields:
        dict: Response chunks with 'text', 'sources', or 'error' keys
    """
    if not GEMINI_API_KEY:
        yield {
            "error": True,
            "message": f"Sorry, the chat service is not configured. {get_contact_message()}"
        }
        return

    try:
        # Initialize model
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Build system prompt
        system_prompt = build_system_prompt(site_context)

        # Build conversation history
        full_history = [
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["Understood. I'll answer questions about Richwell's professional background using only the information provided, keeping responses concise and friendly."]}
        ]

        if history:
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                full_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        # Start chat
        chat = model.start_chat(history=full_history)

        # Stream response
        response = chat.send_message(user_message, stream=True)

        # Determine sources based on context
        sources = []
        if site_context:
            if site_context.get('professional'):
                sources.append('resume')
                sources.append('profile')
            if site_context.get('blogs'):
                sources.append('blog')

        # Send sources first
        yield {"sources": sources}

        # Stream text chunks
        for chunk in response:
            if chunk.text:
                yield {"text": chunk.text}

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Gemini streaming error: {str(e)}")
        print(f"Error type: {type(e).__name__}")

        # Check for rate limit errors
        if 'quota' in error_msg or 'rate limit' in error_msg or '429' in error_msg or 'resource_exhausted' in error_msg:
            yield {
                "error": True,
                "error_type": "rate_limit",
                "message": f"I'm currently at my free API limit (resets daily at midnight Pacific time). {get_contact_message()}"
            }
        else:
            yield {
                "error": True,
                "error_type": "api_error",
                "message": f"I'm having trouble processing your request right now. {get_contact_message()}"
            }
