"""
Resume parser to extract text from PDF resume file.
"""

import os
from PyPDF2 import PdfReader
from pathlib import Path

# Cache for resume content to avoid re-parsing
_resume_cache = None
_resume_cache_timestamp = None

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
    Extract text content from resume PDF file.
    Auto-reloads if file has been modified since last cache.

    Returns:
        str: Extracted text from resume, or None if resume not found
    """
    global _resume_cache, _resume_cache_timestamp

    resume_path = get_resume_path()

    if not resume_path:
        print("Warning: Resume.pdf not found in expected locations")
        return None

    try:
        # Get file modification time
        current_mtime = resume_path.stat().st_mtime

        # Check if cache is still valid
        if _resume_cache is not None and _resume_cache_timestamp == current_mtime:
            # Cache is valid, return it
            return _resume_cache

        # Cache is invalid or empty, reload the file
        print(f"{'Reloading' if _resume_cache else 'Loading'} resume from: {resume_path}")

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

        # Cache the result with timestamp
        _resume_cache = full_text
        _resume_cache_timestamp = current_mtime

        print(f"Resume loaded successfully: {len(full_text)} characters")

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
