"""
Admin Blog API Blueprint
Admin-only endpoints for managing blog posts
"""
from flask import Blueprint, request, jsonify
import os
import re
from config import DEFAULT_PAGE_SIZE, WORDS_PER_MINUTE
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

admin_blog_bp = Blueprint('admin_blog', __name__)


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


@admin_blog_bp.route('/posts', methods=['GET'])
@require_admin
def admin_list_posts():
    """
    GET /admin/blog/posts
    List all posts including drafts (admin only).

    Query params:
        page: int (default 1)
        per_page: int (default 10)
        status: 'published' | 'draft' | None (default None = all)
    """
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


@admin_blog_bp.route('/posts/<slug>', methods=['GET'])
@require_admin
def admin_get_post(slug):
    """
    GET /admin/blog/posts/<slug>
    Get single post regardless of published status (admin only).
    """
    result = supabase.table('blog_posts').select('*').eq('slug', slug).single().execute()

    if not result.data:
        return jsonify(error='Post not found'), 404

    post = result.data
    post['reading_time'] = calculate_reading_time(post['content'])
    post['headings'] = extract_headings(post['content'])
    return jsonify(post)


@admin_blog_bp.route('/posts', methods=['POST'])
@require_admin
def admin_create_post():
    """
    POST /admin/blog/posts
    Create a new blog post (admin only).
    """
    data = request.json
    content = data['content']

    result = supabase.table('blog_posts').insert({
        'slug': data['slug'],
        'title': data['title'],
        'content': content,
        'excerpt': data.get('excerpt', ''),
        'author': data.get('author', 'Richwell Perez'),
        'tags': data.get('tags', []),
        'published': data.get('published', False),
        'published_at': data.get('published_at'),
        'reading_time': calculate_reading_time(content)
    }).execute()

    return jsonify(result.data[0]), 201


@admin_blog_bp.route('/posts/<slug>', methods=['PUT'])
@require_admin
def admin_update_post(slug):
    """
    PUT /admin/blog/posts/<slug>
    Update an existing blog post (admin only).
    """
    data = request.json

    # Recalculate reading_time if content is being updated
    if 'content' in data:
        data['reading_time'] = calculate_reading_time(data['content'])

    result = supabase.table('blog_posts').update(data).eq('slug', slug).execute()

    if not result.data:
        return jsonify(error='Post not found'), 404

    return jsonify(result.data[0])


@admin_blog_bp.route('/posts/<slug>', methods=['DELETE'])
@require_admin
def admin_delete_post(slug):
    """
    DELETE /admin/blog/posts/<slug>
    Delete a blog post (admin only).
    """
    supabase.table('blog_posts').delete().eq('slug', slug).execute()
    return '', 204
