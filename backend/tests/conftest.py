import pytest
from unittest.mock import Mock, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Create Flask app for testing."""
    from api.index import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_supabase():
    """Create mocked Supabase client."""
    mock_client = Mock()

    # Mock table() method chain
    mock_table = Mock()
    mock_client.table.return_value = mock_table

    # Mock query chain methods
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.contains.return_value = mock_table
    mock_table.order.return_value = mock_table
    mock_table.range.return_value = mock_table
    mock_table.or_.return_value = mock_table
    mock_table.ilike.return_value = mock_table

    # Mock execute() returns mock result
    mock_result = Mock()
    mock_result.data = []
    mock_table.execute.return_value = mock_result
    mock_table.single.return_value = mock_table

    return mock_client


@pytest.fixture
def sample_blog_post():
    """Sample blog post data for testing."""
    return {
        'slug': 'test-post',
        'title': 'Test Post',
        'content': '# Test Post\n\nThis is a test.\n\n## Heading 2\n\nMore content.',
        'excerpt': 'This is a test post',
        'author': 'Richwell Perez',
        'tags': ['test', 'python'],
        'published': True,
        'published_at': '2024-01-01T00:00:00Z'
    }


@pytest.fixture
def admin_headers():
    """Headers with admin authentication."""
    return {
        'Authorization': 'Bearer test-admin-key',
        'Content-Type': 'application/json'
    }
