import os
from dotenv import load_dotenv
import google.generativeai as genai

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

    prompt += """
IMPORTANT INSTRUCTIONS:
1. Answer questions using ONLY the information above
2. If asked about something not covered, politely suggest contacting Richwell:
   "For more details about that, I'd recommend reaching out to Richwell directly at richwell.perez@gmail.com or connecting on LinkedIn at linkedin.com/in/richwell-perez"
3. Keep responses concise (2-3 sentences unless more detail is requested)
4. Be conversational and friendly
5. If asked about availability or hiring, say: "Richwell is currently working at Safran, but you can reach out to discuss opportunities at richwell.perez@gmail.com"
6. Do not make up information or speculate beyond what's provided
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
        return "Sorry, the chat service is not configured. Please contact richwell.perez@gmail.com directly."

    try:
        # Initialize model (gemini-2.5-flash is the latest free tier model)
        model = genai.GenerativeModel('gemini-2.5-flash')

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
                "message": "I'm currently experiencing high demand and have reached my request limit. I am using a free model (resets at midnight Pacific time). Please reach out directly at richwell.perez@gmail.com or linkedin.com/in/richwell-perez.",
                "details": str(e)
            }

        # Generic error
        return {
            "error": True,
            "error_type": "api_error",
            "message": "I'm having trouble processing your request. You can reach Richwell directly at richwell.perez@gmail.com or linkedin.com/in/richwell-perez.",
            "details": str(e)
        }
