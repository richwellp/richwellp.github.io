"""
Tests for Gemini API chatbot functionality
"""
import pytest
from api.gemini import determine_relevant_sources


# Test data
FULL_CONTEXT = {
    'professional': {'name': 'Test User'}
}

PROFESSIONAL_ONLY = {
    'professional': {'name': 'Test User'}
}


class TestSingleTopicQuestions:
    """Test single-topic questions return specific sources."""

    def test_projects_questions_only(self):
        """Project-only questions should show only projects source."""
        questions = [
            "What projects have you built?",
            "Show me your portfolio",
            "What have you created?",
            "Tell me about your projects"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert sources == ['projects'], f"Failed for: {question}"

    def test_experience_questions_only(self):
        """Work experience questions should show resume and experience."""
        questions = [
            "What's your work experience?",
            "Where did you work?",
            "Tell me about your job history",
            "What companies have you worked for?"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert 'resume' in sources, f"Resume missing for: {question}"
            assert 'experience' in sources, f"Experience missing for: {question}"

    def test_education_questions_only(self):
        """Education questions should show only profile."""
        questions = [
            "Where did you study?",
            "What's your degree?",
            "Tell me about your education"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert sources == ['profile'], f"Failed for: {question}"

    def test_resume_questions_only(self):
        """Resume questions should show only resume."""
        questions = [
            "Can I see your resume?",
            "Show me your CV",
            "What are your qualifications?"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert sources == ['resume'], f"Failed for: {question}"

    def test_skills_questions_only(self):
        """Skills questions should show profile."""
        questions = [
            "What are your skills?",
            "What technologies do you know?",
            "Tell me your tech stack",
            "What programming languages do you use?"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert sources == ['profile'], f"Failed for: {question}"


class TestMixedTopicQuestions:
    """Test multi-topic and generic questions."""

    def test_work_and_projects_mixed(self):
        """Questions about both work and projects should show multiple sources."""
        question = "What projects have you worked on at your job?"
        sources = determine_relevant_sources(question, FULL_CONTEXT)

        assert 'resume' in sources
        assert 'experience' in sources
        assert 'projects' in sources

    def test_generic_questions_show_all(self):
        """Generic questions should show all available sources."""
        questions = [
            "Tell me about yourself",
            "Who are you?",
            "What can you help me with?"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)

            # Should include professional sources and projects
            assert 'resume' in sources
            assert 'profile' in sources
            assert 'projects' in sources

    def test_greeting_shows_all(self):
        """Greetings show all sources (AI will refine to none)."""
        questions = ["Hi!", "Hello", "Hey there"]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            # Keyword matching shows all, AI will refine to none
            assert len(sources) >= 2


class TestPartialContext:
    """Test when only some data is available."""

    def test_professional_data_available(self):
        """When professional data exists, show professional sources."""
        question = "Tell me about yourself"
        sources = determine_relevant_sources(question, PROFESSIONAL_ONLY)

        assert 'resume' in sources
        assert 'profile' in sources
        assert 'projects' in sources

    def test_no_context_returns_empty(self):
        """When no context provided, return empty list."""
        sources = determine_relevant_sources("What's your experience?", None)
        assert sources == []

        sources = determine_relevant_sources("What's your experience?", {})
        assert sources == []


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_removes_duplicate_sources(self):
        """Source list should not contain duplicates."""
        question = "Tell me about your work experience and job history"
        sources = determine_relevant_sources(question, FULL_CONTEXT)

        # Should not have duplicate 'experience' or 'resume'
        assert len(sources) == len(set(sources))

    def test_case_insensitive_matching(self):
        """Keyword matching should be case-insensitive."""
        questions = [
            "What PROJECTS have you built?",
            "What's your WORK experience?",
            "Tell me about your SKILLS"
        ]

        for question in questions:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert len(sources) > 0, f"No sources for: {question}"

    def test_keyword_variations(self):
        """Should match various keyword forms."""
        test_cases = [
            ("What have you developed?", 'projects'),  # 'developed' -> projects
            ("Tell me about your employer", 'experience'),  # 'employer' -> experience
        ]

        for question, expected_source in test_cases:
            sources = determine_relevant_sources(question, FULL_CONTEXT)
            assert expected_source in sources, f"Expected {expected_source} for: {question}"


class TestSourceAvailability:
    """Test that sources are only shown when data exists."""

    def test_professional_sources_require_data(self):
        """Professional sources only appear when data exists."""
        no_prof_context = {'professional': None}

        question = "What's your work experience?"
        sources = determine_relevant_sources(question, no_prof_context)

        assert 'resume' not in sources
        assert 'profile' not in sources
        assert 'experience' not in sources
        assert 'projects' not in sources
