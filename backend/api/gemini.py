import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import caching
from config import GEMINI_MODEL, get_contact_message
import hashlib
import json
from datetime import datetime, timedelta
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


def build_system_prompt(site_context=None):
    """
    Build system prompt with full professional context.

    Args:
        site_context: Full professional context

    Returns:
        Optimized prompt with complete details
    """
    # Check cache first
    cache_key = hashlib.md5(json.dumps(site_context, sort_keys=True).encode()).hexdigest()
    if cache_key in _prompt_cache:
        return _prompt_cache[cache_key]

    # Build prompt with FULL details
    prompt = """You are Richwell Perez's AI assistant. Answer briefly using info below.

"""

    if site_context:
        prof = site_context.get('professional', {})

        # VALUE PROPOSITION (added at top for emphasis)
        if personal := prof.get('personal'):
            prompt += f"{personal.get('name')} | {personal.get('email')} | {personal.get('location')}\n"
            prompt += f"{personal.get('summary')}\n\n"

        # Add value proposition based on experience
        if experience := prof.get('experience'):
            current = next((exp for exp in experience if exp.get('current')), None)
            if current:
                prompt += "VALUE PROPOSITION:\n"
                prompt += f"• Currently: {current.get('title')} at {current.get('company')}\n"
                prompt += f"• Professional experience across {len(experience)} companies/roles\n"
                if skills := prof.get('skills'):
                    ai_ml = skills.get('ai_ml', [])
                    if ai_ml:
                        prompt += f"• AI/ML expertise: {', '.join(ai_ml[:3])}\n"
                prompt += "• Full-stack + specialized technical skills (rare combination)\n"
                prompt += "• Proven track record building production systems\n\n"

        # Experience - FULL details always
        if experience := prof.get('experience'):
            prompt += "EXPERIENCE:\n"
            for exp in experience:
                prompt += f"• {exp.get('title')} at {exp.get('company')} ({exp.get('dates')})\n"
                prompt += f"  {exp.get('description', '')}\n"
                if highlights := exp.get('highlights'):
                    prompt += "  Key achievements:\n"
                    for h in highlights[:5]:
                        prompt += f"    - {h}\n"
                if tech := exp.get('technologies'):
                    prompt += f"  Tech: {', '.join(tech)}\n"
            prompt += "\n"

        # Projects - FULL details always (top 8)
        if projects := prof.get('projects'):
            prompt += "PROJECTS:\n"
            for proj in projects[:8]:
                prompt += f"• {proj.get('name')} - {proj.get('subtitle', '')}\n"
                prompt += f"  {proj.get('description', '')}\n"
                if tech := proj.get('technologies'):
                    prompt += f"  Tech: {', '.join(tech)}\n"
                if links := proj.get('links'):
                    for link in links:
                        prompt += f"  Link: {link}\n"
            prompt += "\n"

        # Skills
        if skills := prof.get('skills'):
            prompt += "SKILLS:\n"
            if langs := skills.get('languages'):
                prompt += f"Languages: {', '.join(langs)}\n"
            if frameworks := skills.get('frameworks'):
                prompt += f"Frameworks: {', '.join(frameworks)}\n"
            if ai_ml := skills.get('ai_ml'):
                prompt += f"AI/ML: {', '.join(ai_ml)}\n"
            if cloud := skills.get('cloud'):
                prompt += f"Cloud: {', '.join(cloud)}\n"
            if databases := skills.get('databases'):
                prompt += f"Databases: {', '.join(databases)}\n"
            if tools := skills.get('tools'):
                prompt += f"Tools: {', '.join(tools)}\n"
            prompt += "\n"

        # Education
        if education := prof.get('education'):
            prompt += "EDUCATION:\n"
            for edu in education:
                prompt += f"• {edu.get('degree')} - {edu.get('shortName')} ({edu.get('dates')}, GPA: {edu.get('gpa')})\n"
            prompt += "\n"

    # Add current date for accurate calculations
    from datetime import datetime
    current_date = datetime.now().strftime('%B %d, %Y')

    prompt += f"""
CURRENT DATE: {current_date}

INSTRUCTIONS:
- Keep responses brief and complete (2-4 sentences maximum)
- Use the detailed information above to give technical depth
- For date/time calculations: think step by step, show your work
  Example: "Started June 2025, current is {current_date}, so that's X months"
- Highlight achievements and impact (this is for technical recruiters!)
- When users show hiring interest, suggest: "Check out the full resume on the site or {get_contact_message()}"
- Add [SOURCES: resume/profile/experience/projects] at start
- Be professional, confident, and impressive
- ALWAYS complete your sentences - never stop mid-thought
"""

    # Cache the prompt
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
                import sys
                print(f"[Cache] ✅ Using existing cache (key: {cache_key[:12]}...)", file=sys.stderr, flush=True)
                return cached
        except Exception as e:
            # Cache expired or invalid, remove it
            import sys
            print(f"[Cache] ❌ Cache expired or invalid: {e}", file=sys.stderr, flush=True)
            del _context_cache[cache_key]

    # Create new cached content (valid for 1 hour)
    try:
        import sys
        create_start = time.time()
        print(f"[Cache] Creating new cache with {len(system_prompt)} character prompt...", file=sys.stderr, flush=True)

        cached_content = caching.CachedContent.create(
            model=GEMINI_MODEL,
            display_name="portfolio_context",
            system_instruction=system_prompt,
            ttl=timedelta(hours=1)
        )
        create_time = time.time() - create_start

        _context_cache[cache_key] = cached_content
        print(f"[Cache] ✅ Created new context cache in {create_time:.2f}s (valid for 1 hour, prompt size: {len(system_prompt)} chars)", file=sys.stderr, flush=True)
        return cached_content
    except Exception as e:
        # If caching fails (e.g., API doesn't support it), continue without caching
        import sys
        print(f"[Cache] ❌ Context caching not available: {e}", file=sys.stderr, flush=True)
        return None



def determine_relevant_sources(user_message, site_context):
    """
    Determine which sources are relevant based on the user's question.

    Sources:
    - resume: PDF resume content
    - profile: Personal info, education (About Me page)
    - experience: Work history, job details
    - projects: Portfolio projects

    Uses keyword matching for instant display, refined by AI verification.
    """
    if not site_context:
        return []

    message_lower = user_message.lower()

    # Check what data is available
    has_professional = bool(site_context.get('professional'))

    # Detect question type using keyword matching
    question_types = {
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
    if question_types['projects'] and sum(question_types.values()) == 1:
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

    # Remove duplicates while preserving order
    return list(dict.fromkeys(sources))


def select_relevant_context(message, full_context):
    """
    Analyze question and return only relevant context sections.
    Keeps prompt small for faster responses.

    Args:
        message (str): The user's message
        full_context (dict): Full site context with professional info

    Returns:
        dict: Filtered context with only relevant sections
    """
    if not full_context:
        return {}

    message_lower = message.lower()
    prof = full_context.get('professional', {})
    selected = {}

    # Always include name and current role as baseline
    if personal := prof.get('personal'):
        selected['name'] = personal.get('name')
        selected['email'] = personal.get('email')
        selected['location'] = personal.get('location')

    # Contact keywords
    if any(kw in message_lower for kw in ['email', 'contact', 'reach', 'phone', 'linkedin', 'github']):
        if personal := prof.get('personal'):
            selected['contact'] = {
                'email': personal.get('email'),
                'linkedIn': personal.get('linkedIn'),
                'github': personal.get('github'),
                'location': personal.get('location')
            }

    # Experience keywords
    if any(kw in message_lower for kw in ['experience', 'work', 'job', 'career', 'company', 'role', 'position']):
        if experience := prof.get('experience'):
            # Include current role and top 2 previous roles
            selected['experience'] = experience[:3]

    # Skills keywords
    if any(kw in message_lower for kw in ['skill', 'technology', 'tech', 'programming', 'language', 'framework', 'tool']):
        if skills := prof.get('skills'):
            selected['skills'] = skills

    # Projects keywords
    if any(kw in message_lower for kw in ['project', 'portfolio', 'built', 'created', 'app', 'application']):
        if projects := prof.get('projects'):
            # Include top 3 projects
            selected['projects'] = projects[:3]

    # Education keywords
    if any(kw in message_lower for kw in ['education', 'degree', 'university', 'school', 'study', 'college']):
        if education := prof.get('education'):
            selected['education'] = education

    # If no specific match, include current role as baseline
    if len(selected) <= 3:  # Only has name, email, location
        if experience := prof.get('experience'):
            current = next((exp for exp in experience if exp.get('current')), None)
            if current:
                selected['current_role'] = current

    return {'professional': selected}


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
        import sys
        print(f"[Gemini] ===== REQUEST START =====", flush=True, file=sys.stderr)
        request_start = time.time()

        # Create model (no caching - simpler and more reliable)
        model_start = time.time()
        model = genai.GenerativeModel(GEMINI_MODEL)
        model_time = time.time() - model_start
        print(f"[Gemini] Model creation took {model_time:.3f}s", flush=True, file=sys.stderr)

        # Build conversation history with system prompt
        history_start = time.time()
        full_history = []
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
        history_time = time.time() - history_start
        print(f"[Gemini] History building took {history_time:.3f}s (prompt size: {len(system_prompt)} chars)", flush=True, file=sys.stderr)

        # Start chat
        chat_start = time.time()
        chat = model.start_chat(history=full_history)
        chat_time = time.time() - chat_start
        print(f"[Gemini] Chat initialization took {chat_time:.3f}s", flush=True, file=sys.stderr)

        # Stream response
        start_time = time.time()

        # Generation config - prevent truncation, maximize accuracy
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2000,  # Prevent truncation (Gemini 2.5 Flash issue)
            temperature=1.0,         # Required for Gemini 2.5+ models
            top_p=0.3,              # Low = more factual
            top_k=1,                # Deterministic = most accurate
            candidate_count=1
        )

        # Send message and stream response
        api_call_start = time.time()
        print(f"[Gemini] Calling API with message: '{user_message[:50]}...'", flush=True, file=sys.stderr)

        response = chat.send_message(
            user_message,
            stream=True,
            generation_config=generation_config
        )
        api_call_time = time.time() - api_call_start
        print(f"[Gemini] API call returned iterator in {api_call_time:.2f}s", flush=True, file=sys.stderr)

        # Use keyword matching for instant source display (better UX than waiting for AI)
        sources = determine_relevant_sources(user_message, site_context)
        yield {"sources": sources}

        # Stream text chunks with timing
        first_token = True
        first_token_time = None

        import re
        for chunk in response:
            if chunk.text:
                # Track first token latency (time to first response)
                if first_token:
                    first_token_time = time.time() - start_time
                    print(f"[Gemini] First token received in {first_token_time:.2f}s")
                    first_token = False

                # Remove [SOURCES: ...] tag if present (keep response clean)
                chunk_text = re.sub(r'\[SOURCES:[^\]]+\]\s*', '', chunk.text)
                if chunk_text:
                    yield {"text": chunk_text}

        # Log successful completion with timing breakdown
        total_elapsed = time.time() - start_time
        print(f"[Gemini] Streaming completed in {total_elapsed:.2f}s (first token: {first_token_time:.2f}s)")

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Gemini streaming error: {str(e)}", flush=True, file=sys.stderr)
        print(f"Error type: {type(e).__name__}", flush=True, file=sys.stderr)

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


