"""
Resume parser to extract text from PDF resume file.
"""

import os
from PyPDF2 import PdfReader
from pathlib import Path

# Cache for resume content (avoid re-parsing on every request)
_resume_cache = {
    'text': None,
    'timestamp': None,
    'path': None
}


def get_resume_path():
    """
    Get the path to the resume PDF file.
    Resume is always located at: frontend/public/assets/Resume.pdf
    """
    # Current backend directory
    backend_dir = Path(__file__).parent.parent

    # Resume path (fixed location)
    resume_path = backend_dir.parent / "frontend" / "public" / "assets" / "Resume.pdf"

    return resume_path if resume_path.exists() else None


def extract_resume_text():
    """
    Extract text content from resume PDF file with caching.

    Caches the parsed resume text in memory to avoid re-parsing on every request.
    Cache is invalidated if the resume file changes.

    Returns:
        str: Extracted text from resume, or None if resume not found
    """
    resume_path = get_resume_path()

    if not resume_path:
        print("Warning: Resume.pdf not found in expected locations")
        return None

    try:
        # Check cache validity
        current_mtime = resume_path.stat().st_mtime

        if (_resume_cache['text'] is not None and
            _resume_cache['path'] == resume_path and
            _resume_cache['timestamp'] == current_mtime):
            # Return cached content
            return _resume_cache['text']

        # Cache miss or stale - parse the PDF
        print(f"Loading resume from: {resume_path}")

        # Read PDF file
        reader = PdfReader(resume_path)

        # Extract text from all pages
        text_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)

        # Join all pages with newlines
        full_text = "\n\n".join(text_content)

        # Update cache
        _resume_cache['text'] = full_text
        _resume_cache['timestamp'] = current_mtime
        _resume_cache['path'] = resume_path

        print(f"Resume loaded and cached: {len(full_text)} characters")

        return full_text

    except Exception as e:
        print(f"Error reading resume PDF: {str(e)}")
        return None


def get_resume_summary():
    """
    Get a formatted summary of the resume content.

    Returns:
        str: Formatted resume content for inclusion in system prompt
    """
    resume_text = extract_resume_text()

    if not resume_text:
        return ""

    # Format for system prompt
    formatted = f"""
RESUME CONTENT:
{resume_text}

Use the resume content above to provide detailed, accurate answers about:
- Work experience and specific achievements
- Technical skills and proficiencies
- Education and certifications
- Projects and their impact
- Leadership and responsibilities
- Any other information present in the resume

If the resume contains information not in other sources, prioritize the resume as the most up-to-date source.
"""

    return formatted
