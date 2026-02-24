"""
Sitemap API endpoint
Generates dynamic XML sitemap including blog posts and albums
"""
from flask import Blueprint, make_response
from datetime import datetime
import os

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

sitemap_bp = Blueprint('sitemap', __name__)

BASE_URL = 'https://richwellp.github.io'

# Static pages with their priorities and change frequencies
STATIC_PAGES = [
    {'path': '/', 'priority': '1.0', 'changefreq': 'weekly'},
    {'path': '/experience', 'priority': '0.9', 'changefreq': 'monthly'},
    {'path': '/projects', 'priority': '0.9', 'changefreq': 'monthly'},
    {'path': '/cv', 'priority': '0.8', 'changefreq': 'monthly'},
    {'path': '/misc', 'priority': '0.7', 'changefreq': 'weekly'},
    {'path': '/misc/blog', 'priority': '0.9', 'changefreq': 'weekly'},
    {'path': '/misc/albums', 'priority': '0.7', 'changefreq': 'monthly'},
    {'path': '/contact', 'priority': '0.6', 'changefreq': 'yearly'},
]


def format_date(date_str):
    """Format date to W3C datetime format (YYYY-MM-DD)."""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')

    try:
        # Parse various date formats
        if 'T' in str(date_str):
            # ISO format
            dt = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        else:
            # Try parsing as date only
            dt = datetime.strptime(str(date_str)[:10], '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')


def generate_sitemap_xml():
    """Generate complete sitemap XML with static and dynamic content."""
    urls = []

    # Add static pages
    for page in STATIC_PAGES:
        urls.append(f'''  <url>
    <loc>{BASE_URL}{page['path']}</loc>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>''')

    # Add blog posts
    if supabase:
        try:
            result = supabase.table('blog_posts')\
                .select('slug, updated_at, published_at, created_at')\
                .eq('published', True)\
                .execute()

            for post in result.data:
                # Use the most recent date available
                lastmod = format_date(
                    post.get('updated_at') or
                    post.get('published_at') or
                    post.get('created_at')
                )

                urls.append(f'''  <url>
    <loc>{BASE_URL}/misc/blog/{post['slug']}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>''')
        except Exception as e:
            print(f"Warning: Failed to fetch blog posts for sitemap: {e}")

    # Add albums
    if supabase:
        try:
            result = supabase.table('albums')\
                .select('slug, updated_at, created_at')\
                .eq('published', True)\
                .execute()

            for album in result.data:
                lastmod = format_date(
                    album.get('updated_at') or
                    album.get('created_at')
                )

                urls.append(f'''  <url>
    <loc>{BASE_URL}/misc/albums/{album['slug']}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>''')
        except Exception as e:
            print(f"Warning: Failed to fetch albums for sitemap: {e}")

    # Build complete XML
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    return xml


@sitemap_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """
    GET /sitemap.xml

    Returns dynamic XML sitemap including:
    - Static pages (home, experience, projects, etc.)
    - Published blog posts
    - Published albums

    Response:
        XML sitemap following sitemaps.org protocol
    """
    xml_content = generate_sitemap_xml()

    response = make_response(xml_content)
    response.headers['Content-Type'] = 'application/xml'
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour

    return response
