import pytest
import json
from unittest.mock import patch, Mock
import os


# Mock environment variables before importing blog module
@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for all tests."""
    with patch.dict(os.environ, {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_KEY': 'test-key',
        'BLOG_ADMIN_KEY': 'test-admin-key'
    }):
        yield


@pytest.fixture
def blog_app():
    """Create Flask app with blog blueprint registered."""
    from api.index import app
    from api.blog import blog_bp

    # Register blog blueprint if not already registered
    if not any(bp.name == 'blog' for bp in app.blueprints.values()):
        app.register_blueprint(blog_bp, url_prefix='/blog')

    app.config['TESTING'] = True
    return app


@pytest.fixture
def blog_client(blog_app):
    """Create test client with blog routes."""
    return blog_app.test_client()


# Test 1: List posts returns published posts only
def test_list_posts_returns_published_posts_only(blog_client, mock_supabase):
    """GET /blog/posts should return only published posts."""
    # Mock Supabase response
    mock_posts = [
        {
            'slug': 'post-1',
            'title': 'Post 1',
            'excerpt': 'Excerpt 1',
            'author': 'Richwell Perez',
            'tags': ['python'],
            'published_at': '2024-01-01T00:00:00Z'
        },
        {
            'slug': 'post-2',
            'title': 'Post 2',
            'excerpt': 'Excerpt 2',
            'author': 'Richwell Perez',
            'tags': ['javascript'],
            'published_at': '2024-01-02T00:00:00Z'
        }
    ]

    with patch('api.blog.supabase') as mock_sb:
        mock_result = Mock()
        mock_result.data = mock_posts

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.range.return_value = mock_chain
        mock_chain.order.return_value = mock_chain
        mock_chain.eq.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/posts')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'posts' in data
        assert len(data['posts']) == 2
        assert data['posts'][0]['slug'] == 'post-1'

        # Verify it filtered for published=True
        mock_chain.eq.assert_any_call('published', True)


# Test 2: List posts filters by tag
def test_list_posts_filters_by_tag(blog_client):
    """GET /blog/posts?tag=python should filter by tag."""
    with patch('api.blog.supabase') as mock_sb:
        mock_result = Mock()
        mock_result.data = [{'slug': 'python-post', 'tags': ['python']}]

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.range.return_value = mock_chain
        mock_chain.order.return_value = mock_chain
        mock_chain.eq.return_value = mock_chain
        mock_chain.contains.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/posts?tag=python')

        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify contains was called with the tag
        mock_chain.contains.assert_called_with('tags', ['python'])


# Test 3: List posts pagination
def test_list_posts_pagination(blog_client):
    """GET /blog/posts?page=2&per_page=5 should paginate correctly."""
    with patch('api.blog.supabase') as mock_sb:
        mock_result = Mock()
        mock_result.data = []

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.range.return_value = mock_chain
        mock_chain.order.return_value = mock_chain
        mock_chain.eq.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/posts?page=2&per_page=5')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['page'] == 2
        assert data['per_page'] == 5

        # Verify correct range (page 2 with per_page 5 = items 5-9)
        mock_chain.range.assert_called_with(5, 9)


# Test 4: Get post by slug returns post with metadata
def test_get_post_by_slug_returns_post_with_metadata(blog_client):
    """GET /blog/posts/<slug> should return post with reading_time and headings."""
    with patch('api.blog.supabase') as mock_sb:
        mock_post = {
            'slug': 'test-post',
            'title': 'Test Post',
            'content': '# Test\n\n' + ('word ' * 400) + '\n\n## Section 1\n\nMore content.\n\n### Subsection',
            'excerpt': 'Test excerpt',
            'author': 'Richwell Perez',
            'tags': ['test'],
            'published': True,
            'published_at': '2024-01-01T00:00:00Z'
        }

        mock_result = Mock()
        mock_result.data = mock_post

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.single.return_value = mock_chain
        mock_chain.eq.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/posts/test-post')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['slug'] == 'test-post'
        assert 'reading_time' in data
        assert data['reading_time'] >= 2  # ~400 words = 2 min
        assert 'headings' in data
        assert len(data['headings']) == 2  # ## and ### headings


# Test 5: Get post not found returns 404
def test_get_post_not_found_returns_404(blog_client):
    """GET /blog/posts/nonexistent should return 404."""
    with patch('api.blog.supabase') as mock_sb:
        mock_result = Mock()
        mock_result.data = None

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.single.return_value = mock_chain
        mock_chain.eq.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/posts/nonexistent')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


# Test 6: Search posts finds by title and content
def test_search_posts_finds_by_title_and_content(blog_client):
    """GET /blog/search?q=keyword should search title, content, and excerpt."""
    with patch('api.blog.supabase') as mock_sb:
        mock_results = [
            {'slug': 'post-1', 'title': 'Python Tutorial'},
            {'slug': 'post-2', 'title': 'Advanced Python'}
        ]

        mock_result = Mock()
        mock_result.data = mock_results

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result
        mock_chain.eq.return_value = mock_chain
        mock_chain.or_.return_value = mock_chain

        mock_table = Mock()
        mock_table.select.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.get('/blog/search?q=python')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'posts' in data
        assert len(data['posts']) == 2
        assert data['total'] == 2


# Test 7: Create post requires admin auth
def test_create_post_requires_admin_auth(blog_client):
    """POST /blog/posts without auth should return 401."""
    post_data = {
        'slug': 'new-post',
        'title': 'New Post',
        'content': '# Content'
    }

    response = blog_client.post(
        '/blog/posts',
        data=json.dumps(post_data),
        content_type='application/json'
    )

    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data


# Test 8: Create post with valid auth succeeds
def test_create_post_with_valid_auth_succeeds(blog_client):
    """POST /blog/posts with valid auth should create post."""
    with patch('api.blog.supabase') as mock_sb:
        post_data = {
            'slug': 'new-post',
            'title': 'New Post',
            'content': '# Content',
            'excerpt': 'Excerpt',
            'tags': ['test']
        }

        mock_result = Mock()
        mock_result.data = [{**post_data, 'id': '123'}]

        mock_chain = Mock()
        mock_chain.execute.return_value = mock_result

        mock_table = Mock()
        mock_table.insert.return_value = mock_chain
        mock_sb.table.return_value = mock_table

        response = blog_client.post(
            '/blog/posts',
            data=json.dumps(post_data),
            headers={
                'Authorization': 'Bearer test-admin-key',
                'Content-Type': 'application/json'
            }
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['slug'] == 'new-post'


# Test 9: Update post requires admin auth
def test_update_post_requires_admin_auth(blog_client):
    """PUT /blog/posts/<slug> without auth should return 401."""
    update_data = {'title': 'Updated Title'}

    response = blog_client.put(
        '/blog/posts/test-post',
        data=json.dumps(update_data),
        content_type='application/json'
    )

    assert response.status_code == 401


# Test 10: Delete post requires admin auth
def test_delete_post_requires_admin_auth(blog_client):
    """DELETE /blog/posts/<slug> without auth should return 401."""
    response = blog_client.delete('/blog/posts/test-post')

    assert response.status_code == 401


# Test 11: Calculate reading time
def test_calculate_reading_time():
    """calculate_reading_time should estimate reading time correctly."""
    from api.blog import calculate_reading_time

    # 200 words = 1 minute
    content_200_words = ' '.join(['word'] * 200)
    assert calculate_reading_time(content_200_words) == 1

    # 400 words = 2 minutes
    content_400_words = ' '.join(['word'] * 400)
    assert calculate_reading_time(content_400_words) == 2

    # 50 words = should round to 1 minute minimum
    content_50_words = ' '.join(['word'] * 50)
    assert calculate_reading_time(content_50_words) == 1


# Test 12: Extract headings from markdown
def test_extract_headings_from_markdown():
    """extract_headings should parse ## and ### headings."""
    from api.blog import extract_headings

    markdown = """
# Title (should be ignored)

## Section 1
Some content

### Subsection 1.1
More content

## Section 2
Final content
"""

    headings = extract_headings(markdown)

    assert len(headings) == 3
    assert headings[0]['level'] == 2
    assert headings[0]['text'] == 'Section 1'
    assert headings[0]['id'] == 'section-1'

    assert headings[1]['level'] == 3
    assert headings[1]['text'] == 'Subsection 1.1'
    assert headings[1]['id'] == 'subsection-11'

    assert headings[2]['level'] == 2
    assert headings[2]['text'] == 'Section 2'
