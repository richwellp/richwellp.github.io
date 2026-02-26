"""
Centralized configuration for backend API
"""
import os

# Contact Information
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'richwell.perez@gmail.com')
CONTACT_LINKEDIN = os.environ.get('CONTACT_LINKEDIN', 'linkedin.com/in/richwell-perez')

# Rate Limiting
RATE_LIMIT_REQUESTS = 10  # requests
RATE_LIMIT_WINDOW = 60    # seconds

# Message Constraints
MESSAGE_LENGTH_LIMIT = 2000  # characters
HISTORY_LIMIT = 20  # maximum conversation history to send

# Gemini Configuration
# gemini-2.5-flash - Latest free model (has truncation issues, but we handle them)
GEMINI_MODEL = 'gemini-2.5-flash'


# Blog Configuration
DEFAULT_PAGE_SIZE = 10
WORDS_PER_MINUTE = 200  # Average reading speed
DEFAULT_READING_TIME_ESTIMATE = 5  # Minutes (when content not available)

def get_contact_message():
    """Get formatted contact message for error responses."""
    return f"Please reach out directly at {CONTACT_EMAIL} or {CONTACT_LINKEDIN}."
