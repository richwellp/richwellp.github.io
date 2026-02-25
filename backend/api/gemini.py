import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import caching
from api.resume_parser import get_resume_summary
from config import GEMINI_MODEL, get_contact_message
import hashlib
import json
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import time

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Cache for system prompts (avoid rebuilding on every request)
_prompt_cache = {}

# Cache for Gemini context caching (stores CachedContent objects)
_context_cache = {}

# Global thread pool for timeout handling
_executor = ThreadPoolExecutor(max_workers=10)

# API timeout configuration (5 minutes to allow slow but working responses)
# Note: Gemini free tier can take 3-5 minutes during high load but still returns good answers
API_TIMEOUT = 300  # 5 minutes = 300 seconds

def build_system_prompt(site_context=None):
    """
    Build system prompt from frontend-provided context with caching.

    Caches prompts based on site_context + resume modification time to avoid rebuilding identical prompts.
    """
    # Include resume modification time in cache key to detect resume changes
    from api.resume_parser import get_resume_path
    resume_path = get_resume_path()
    resume_mtime = resume_path.stat().st_mtime if resume_path and resume_path.exists() else None

    # Create cache key from site_context + resume mtime
    cache_data = {
        'site_context': site_context,
        'resume_mtime': resume_mtime
    }
    cache_key = hashlib.md5(json.dumps(cache_data, sort_keys=True).encode()).hexdigest()

    # Check cache
    if cache_key in _prompt_cache:
        return _prompt_cache[cache_key]

    # Cache miss - build prompt
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
                prompt += f"- \"{blog.get('title')}\" ({blog.get('date')})"
                if tags := blog.get('tags'):
                    prompt += f" | Tags: {', '.join(tags)}"
                prompt += "\n"
            prompt += "\n"

    prompt += f"""
IMPORTANT INSTRUCTIONS:
1. Answer questions using ONLY the information above
2. PRIORITIZE the RESUME CONTENT as the most authoritative and up-to-date source
3. If asked about something not covered, politely suggest contacting Richwell:
   "For more details about that, {get_contact_message()}"
4. Keep responses concise (2-3 sentences unless more detail is requested)
5. Be conversational and friendly
6. If asked about availability or hiring, say: "Richwell is currently working at RAVE Aerospace. {get_contact_message()} to discuss opportunities."
7. Do not make up information or speculate beyond what's provided
8. When answering questions, draw from the resume's detailed information about specific achievements, projects, and responsibilities

SOURCE TRACKING:
At the START of your response, include a special indicator line showing which sources you used:
[SOURCES: resume, profile, experience, projects, blog]

Only include sources you actually referenced:
- Use "resume" if you cited the PDF resume content
- Use "profile" if you used personal info (name, email, location, summary, education, skills)
- Use "experience" if you mentioned work experience or job history
- Use "projects" if you referenced specific projects or portfolio work
- Use "blog" if you mentioned or referenced blog posts
- For generic greetings or questions you can't answer, use: [SOURCES: none]

Example responses:
User: "What's your work experience?"
[SOURCES: resume, experience]
I'm currently an AI Engineer at RAVE Aerospace...

User: "What projects have you built?"
[SOURCES: projects]
I've built several projects including...

User: "Tell me about your blog posts"
[SOURCES: blog]
I've written several blog posts including...

User: "Hi there!"
[SOURCES: none]
Hi! I'm Richwell's virtual assistant...
"""

    # Cache the prompt for future requests with same context
    _prompt_cache[cache_key] = prompt

    return prompt


def get_or_create_cached_context(site_context=None):
    """
    Get or create a cached context for Gemini to improve latency.

    Caches the large system prompt for 1 hour, reducing latency by 50-70%.
    """
    if not GEMINI_API_KEY:
        return None

    # Build system prompt
    system_prompt = build_system_prompt(site_context)

    # Create cache key from system prompt
    cache_key = hashlib.md5(system_prompt.encode()).hexdigest()

    # Check if we have a valid cached context
    if cache_key in _context_cache:
        cached = _context_cache[cache_key]
        try:
            # Verify cache is still valid (not expired)
            if cached and hasattr(cached, 'name'):
                return cached
        except Exception as e:
            # Cache expired or invalid, remove it
            print(f"Cache expired or invalid: {e}")
            del _context_cache[cache_key]

    # Create new cached content (valid for 1 hour)
    try:
        cached_content = caching.CachedContent.create(
            model=GEMINI_MODEL,
            display_name="portfolio_context",
            system_instruction=system_prompt,
            ttl=timedelta(hours=1)
        )

        _context_cache[cache_key] = cached_content
        print(f"Created new context cache (valid for 1 hour)")
        return cached_content
    except Exception as e:
        # If caching fails (e.g., API doesn't support it), continue without caching
        print(f"Context caching not available: {e}")
        return None


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

        # Send message with timeout
        print(f"[Gemini] Sending message with {API_TIMEOUT}s timeout...")
        start_time = time.time()

        def _send_message():
            return chat.send_message(user_message)

        try:
            future = _executor.submit(_send_message)
            response = future.result(timeout=API_TIMEOUT)
            elapsed = time.time() - start_time
            print(f"[Gemini] Response received in {elapsed:.2f}s")
            return response.text
        except FutureTimeoutError:
            elapsed = time.time() - start_time
            print(f"[Gemini] TIMEOUT after {elapsed:.2f}s")
            return {
                "error": True,
                "error_type": "timeout",
                "message": f"The AI service took too long to respond ({API_TIMEOUT}s timeout). This usually means high API load or rate limits. {get_contact_message()}",
                "details": f"Request timed out after {API_TIMEOUT} seconds"
            }

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


def determine_relevant_sources(user_message, site_context):
    """
    Determine which sources are relevant based on the user's question.

    Sources:
    - resume: PDF resume content
    - profile: Personal info, education (About Me page)
    - experience: Work history, job details
    - projects: Portfolio projects
    - blog: Blog posts

    Uses keyword matching for instant display, refined by AI verification.
    """
    if not site_context:
        return []

    message_lower = user_message.lower()

    # Check what data is available
    has_professional = bool(site_context.get('professional'))
    has_blogs = bool(site_context.get('blogs'))

    # Detect question type using keyword matching
    question_types = {
        'blog': any(kw in message_lower for kw in [
            'blog', 'post', 'article', 'wrote', 'written', 'published'
        ]),
        'projects': any(kw in message_lower for kw in [
            'project', 'projects', 'built', 'build', 'building',
            'created', 'create', 'creating', 'developed', 'develop', 'developing',
            'portfolio', 'github', 'code', 'coding',
            'app', 'application', 'software', 'system'
        ]),
        'experience': any(kw in message_lower for kw in [
            'work', 'worked', 'working', 'experience', 'experienced',
            'job', 'jobs', 'company', 'companies', 'employer', 'employment', 'employed',
            'role', 'roles', 'position', 'positions', 'career'
        ]),
        'education': any(kw in message_lower for kw in [
            'education', 'degree', 'school', 'university', 'studied', 'study', 'major', 'college'
        ]),
        'resume': any(kw in message_lower for kw in [
            'resume', 'cv', 'qualification', 'certification'
        ]),
        'skills': any(kw in message_lower for kw in [
            'skill', 'skills', 'technology', 'technologies', 'tech stack',
            'programming language', 'language', 'languages', 'framework', 'frameworks',
            'tool', 'tools', 'proficient', 'expertise', 'technical'
        ])
    }

    # Build source list based on question type
    sources = []

    # Single-topic questions (most specific)
    if question_types['blog'] and sum(question_types.values()) == 1:
        if has_blogs:
            sources = ['blog']
    elif question_types['projects'] and sum(question_types.values()) == 1:
        if has_professional:
            sources = ['projects']
    elif question_types['experience'] and sum(question_types.values()) == 1:
        if has_professional:
            sources = ['resume', 'experience']
    elif question_types['education'] and sum(question_types.values()) == 1:
        if has_professional:
            sources = ['profile']
    elif question_types['resume'] and sum(question_types.values()) == 1:
        if has_professional:
            sources = ['resume']
    elif question_types['skills'] and sum(question_types.values()) == 1:
        if has_professional:
            sources = ['profile']  # Skills are part of profile/personal info
    # Multi-topic or generic questions (show all relevant)
    else:
        if has_professional:
            sources.extend(['resume', 'profile'])
            # Add experience if work-related
            if question_types['experience']:
                sources.append('experience')
            # Add projects if project-related or generic
            if question_types['projects'] or sum(question_types.values()) == 0:
                sources.append('projects')
        if has_blogs and (question_types['blog'] or sum(question_types.values()) == 0):
            sources.append('blog')

    # Remove duplicates while preserving order
    return list(dict.fromkeys(sources))


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
        # Try to use cached context for better latency
        cached_context = get_or_create_cached_context(site_context)

        if cached_context:
            # Use cached context (50-70% faster)
            model = genai.GenerativeModel.from_cached_content(cached_content=cached_context)
        else:
            # Fallback to regular mode without caching
            model = genai.GenerativeModel(GEMINI_MODEL)

        # Build conversation history (exclude system prompt if using cache)
        full_history = []

        # If not using cache, add system prompt manually
        if not cached_context:
            system_prompt = build_system_prompt(site_context)
            full_history.append({"role": "user", "parts": [system_prompt]})
            full_history.append({"role": "model", "parts": ["Understood. I'll answer questions about Richwell's professional background using only the information provided, keeping responses concise and friendly."]})

        # Add conversation history
        if history:
            for msg in history:
                role = "model" if msg["role"] == "assistant" else "user"
                full_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        # Start chat
        chat = model.start_chat(history=full_history)

        # Stream response with timeout tracking
        print(f"[Gemini] Streaming message with {API_TIMEOUT}s timeout...")
        start_time = time.time()

        # Send message (this returns immediately, but we track time during streaming)
        response = chat.send_message(user_message, stream=True)

        # Use keyword matching for instant source display (better UX than waiting for AI)
        sources = determine_relevant_sources(user_message, site_context)
        yield {"sources": sources}

        # Track response for source verification
        response_buffer = ""
        sources_verified = False
        last_chunk_time = time.time()

        # Stream text chunks with timeout
        for chunk in response:
            # Check if we've exceeded timeout
            elapsed = time.time() - start_time
            if elapsed > API_TIMEOUT:
                print(f"[Gemini] STREAMING TIMEOUT after {elapsed:.2f}s")
                yield {
                    "error": True,
                    "message": f"Streaming timed out after {API_TIMEOUT}s. {get_contact_message()}"
                }
                return

            last_chunk_time = time.time()
            if chunk.text:
                response_buffer += chunk.text

                # Verify sources from AI response (first chunk only)
                if not sources_verified and '[SOURCES:' in response_buffer:
                    import re
                    match = re.search(r'\[SOURCES:\s*([^\]]+)\]', response_buffer)
                    if match:
                        source_text = match.group(1).strip()
                        verified_sources = []

                        # Parse sources from AI
                        if 'none' not in source_text.lower():
                            if 'resume' in source_text:
                                verified_sources.append('resume')
                            if 'profile' in source_text:
                                verified_sources.append('profile')
                            if 'experience' in source_text:
                                verified_sources.append('experience')
                            if 'projects' in source_text or 'project' in source_text:
                                verified_sources.append('projects')
                            if 'blog' in source_text:
                                verified_sources.append('blog')

                        # Update sources if AI provided different ones
                        if verified_sources and verified_sources != sources:
                            yield {"sources": verified_sources}

                        sources_verified = True

                        # Remove [SOURCES: ...] from visible response
                        chunk_text = re.sub(r'\[SOURCES:[^\]]+\]\s*', '', chunk.text)
                        if chunk_text:
                            yield {"text": chunk_text}
                    else:
                        yield {"text": chunk.text}
                else:
                    # After sources are verified, strip them from all chunks
                    if sources_verified:
                        chunk_text = chunk.text
                        if '[SOURCES:' in chunk_text:
                            chunk_text = re.sub(r'\[SOURCES:[^\]]+\]\s*', '', chunk_text)
                        if chunk_text:
                            yield {"text": chunk_text}
                    else:
                        yield {"text": chunk.text}

        # Log successful completion
        total_elapsed = time.time() - start_time
        print(f"[Gemini] Streaming completed successfully in {total_elapsed:.2f}s")

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
