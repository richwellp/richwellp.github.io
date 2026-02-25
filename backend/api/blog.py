from flask import Blueprint, request, jsonify
import os
import re
from config import DEFAULT_PAGE_SIZE, WORDS_PER_MINUTE, DEFAULT_READING_TIME_ESTIMATE
from auth import require_admin

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
        'slug,title,excerpt,author,tags,published_at,created_at,reading_time'
    )
    query = query.eq('published', True).order('created_at', desc=True)

    # Filter by tag if provided
    if tag:
        query = query.contains('tags', [tag])

    # Apply pagination
    start = (page - 1) * per_page
    end = page * per_page - 1
    result = query.range(start, end).execute()

    return jsonify(posts=result.data, page=page, per_page=per_page)


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


# Admin routes moved to api/admin_blog.py
