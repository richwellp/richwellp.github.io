from flask import Blueprint, request, jsonify
from functools import wraps
import os
import re
from config import DEFAULT_PAGE_SIZE, WORDS_PER_MINUTE, DEFAULT_READING_TIME_ESTIMATE

# Initialize Supabase client
try:
    from supabase import create_client
    supabase = create_client(
        os.environ.get('SUPABASE_URL', ''),
        os.environ.get('SUPABASE_KEY', '')
    )
except Exception as e:
    print(f"Warning: Supabase client initialization failed: {e}")
    supabase = None

blog_bp = Blueprint('blog', __name__)

# Admin authentication
ADMIN_KEY = os.environ.get('BLOG_ADMIN_KEY', '')


def require_admin(f):
    """Decorator to require admin authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer ') or auth[7:] != ADMIN_KEY:
            return jsonify(error='Unauthorized'), 401
        return f(*args, **kwargs)
    return decorated


def calculate_reading_time(content):
    """Calculate estimated reading time in minutes."""
    words = len(re.findall(r'\w+', content))
    return max(1, round(words / WORDS_PER_MINUTE))


def extract_headings(content):
    """Extract ## and ### headings from markdown content."""
    headings = []
    for match in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2)
        # Create ID: lowercase, remove special chars, replace spaces with hyphens
        id = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
        headings.append({'level': level, 'text': text, 'id': id})
    return headings


@blog_bp.route('/posts', methods=['GET'])
def list_posts():
    """List published blog posts with pagination and filtering."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', DEFAULT_PAGE_SIZE))
    tag = request.args.get('tag')

    # Build query
    query = supabase.table('blog_posts').select(
        'slug,title,excerpt,author,tags,published_at,created_at'
    )
    query = query.eq('published', True).order('published_at', desc=True)

    # Filter by tag if provided
    if tag:
        query = query.contains('tags', [tag])

    # Apply pagination
    start = (page - 1) * per_page
    end = page * per_page - 1
    result = query.range(start, end).execute()

    # Add reading_time estimate to each post
    posts = [{
        **post,
        'reading_time': DEFAULT_READING_TIME_ESTIMATE  # Estimated (actual calculation requires full content)
    } for post in result.data]

    return jsonify(posts=posts, page=page, per_page=per_page)


@blog_bp.route('/posts/<slug>', methods=['GET'])
def get_post(slug):
    """Get a single blog post by slug."""
    result = supabase.table('blog_posts').select('*').eq('slug', slug).eq(
        'published', True
    ).single().execute()

    if not result.data:
        return jsonify(error='Post not found'), 404

    post = result.data
    post['reading_time'] = calculate_reading_time(post['content'])
    post['headings'] = extract_headings(post['content'])

    return jsonify(post)


@blog_bp.route('/search', methods=['GET'])
def search_posts():
    """Search blog posts by query string."""
    q = request.args.get('q', '')
    if not q:
        return jsonify(posts=[], total=0)

    # Search in title, content, and excerpt
    result = supabase.table('blog_posts').select(
        'slug,title,excerpt,tags,published_at'
    ).eq('published', True).or_(
        f'title.ilike.%{q}%,content.ilike.%{q}%,excerpt.ilike.%{q}%'
    ).execute()

    return jsonify(posts=result.data, total=len(result.data))


@blog_bp.route('/posts', methods=['POST'])
@require_admin
def create_post():
    """Create a new blog post (admin only)."""
    data = request.json

    result = supabase.table('blog_posts').insert({
        'slug': data['slug'],
        'title': data['title'],
        'content': data['content'],
        'excerpt': data.get('excerpt', ''),
        'author': data.get('author', 'Richwell Perez'),
        'tags': data.get('tags', []),
        'published': data.get('published', False),
        'published_at': data.get('published_at')
    }).execute()

    return jsonify(result.data[0]), 201


@blog_bp.route('/posts/<slug>', methods=['PUT'])
@require_admin
def update_post(slug):
    """Update an existing blog post (admin only)."""
    data = request.json

    result = supabase.table('blog_posts').update(data).eq('slug', slug).execute()

    if not result.data:
        return jsonify(error='Post not found'), 404

    return jsonify(result.data[0])


@blog_bp.route('/posts/<slug>', methods=['DELETE'])
@require_admin
def delete_post(slug):
    """Delete a blog post (admin only)."""
    supabase.table('blog_posts').delete().eq('slug', slug).execute()
    return '', 204


@blog_bp.route('/admin/posts', methods=['GET'])
@require_admin
def admin_list_posts():
    """List all posts including drafts (admin only)."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', DEFAULT_PAGE_SIZE))
    status = request.args.get('status')  # 'published', 'draft', or None

    query = supabase.table('blog_posts').select('*')

    if status == 'published':
        query = query.eq('published', True)
    elif status == 'draft':
        query = query.eq('published', False)

    query = query.order('created_at', desc=True)
    start = (page - 1) * per_page
    result = query.range(start, start + per_page - 1).execute()

    return jsonify(posts=result.data, page=page, per_page=per_page, total=len(result.data))


@blog_bp.route('/admin/posts/<slug>', methods=['GET'])
@require_admin
def admin_get_post(slug):
    """Get single post regardless of published status (admin only)."""
    result = supabase.table('blog_posts').select('*').eq('slug', slug).single().execute()

    if not result.data:
        return jsonify(error='Post not found'), 404

    post = result.data
    post['reading_time'] = calculate_reading_time(post['content'])
    post['headings'] = extract_headings(post['content'])
    return jsonify(post)
