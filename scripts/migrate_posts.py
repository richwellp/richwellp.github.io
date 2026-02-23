#!/usr/bin/env python3
"""
Migrate blog posts from Markdown files to Supabase database.
Usage:
  python migrate_posts.py --dry-run  # Show what would be migrated
  python migrate_posts.py            # Actually migrate
"""

import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
import urllib3
import warnings

# Disable SSL warnings for Windows environment
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Add backend to path for imports
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Load environment variables from backend/.env
env_path = backend_path / '.env'
load_dotenv(env_path)

from supabase import create_client


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text, body = match.groups()
    data = {}

    for line in frontmatter_text.split('\n'):
        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip('"\'')

        # Parse tags array
        if key == 'tags' and value.startswith('[') and value.endswith(']'):
            # Extract items between brackets and quotes
            tags = re.findall(r'"([^"]+)"', value)
            data[key] = tags
        else:
            data[key] = value

    return data, body


def migrate_post(supabase, filepath, dry_run=False):
    """Migrate a single blog post."""
    filename = os.path.basename(filepath)

    # Skip README
    if filename == 'README.md':
        return None

    # Parse filename: YYYY-MM-DD-slug.md
    match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', filename)
    if not match:
        print(f'[SKIP]  Skipping {filename}: Invalid format (expected YYYY-MM-DD-slug.md)')
        return None

    date, slug = match.groups()

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    post_data = {
        'slug': slug,
        'title': frontmatter.get('title', slug.replace('-', ' ').title()),
        'content': body.strip(),
        'excerpt': frontmatter.get('excerpt', ''),
        'author': frontmatter.get('author', 'Richwell Perez'),
        'tags': frontmatter.get('tags', []),
        'published': True,
        'published_at': f'{date}T00:00:00Z'
    }

    if dry_run:
        print(f'\n[FILE] Would migrate: {filename}')
        print(f'   Slug: {post_data["slug"]}')
        print(f'   Title: {post_data["title"]}')
        print(f'   Date: {post_data["published_at"]}')
        print(f'   Tags: {post_data["tags"]}')
        print(f'   Content length: {len(post_data["content"])} characters')
        return post_data

    # Actually insert to database
    try:
        result = supabase.table('blog_posts').insert(post_data).execute()
        print(f'[OK] Migrated: {filename} -> {slug}')
        return result.data[0] if result.data else None
    except Exception as e:
        print(f'[ERROR] Failed to migrate {filename}: {e}')
        return None


def main():
    dry_run = '--dry-run' in sys.argv

    print('=' * 60)
    print('Blog Post Migration Script')
    print('=' * 60)
    print(f'Mode: {"DRY RUN (no changes will be made)" if dry_run else "LIVE (will insert to database)"}')
    print()

    # Initialize Supabase client
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print('[ERROR] ERROR: SUPABASE_URL and SUPABASE_KEY must be set in backend/.env')
        sys.exit(1)

    print(f'Supabase URL: {supabase_url}')
    print()

    try:
        # Monkey patch to disable SSL verification
        import httpx
        _original_build = httpx.Client.__init__

        def patched_init(self, *args, **kwargs):
            kwargs['verify'] = False
            return _original_build(self, *args, **kwargs)

        httpx.Client.__init__ = patched_init

        supabase = create_client(supabase_url, supabase_key)
        print('[WARNING] SSL verification disabled for migration (Windows environment workaround)')
        print()
    except Exception as e:
        print(f'[ERROR] ERROR: Failed to create Supabase client: {e}')
        sys.exit(1)

    # Find blog directory
    blog_dir = Path(__file__).parent.parent / 'frontend' / 'public' / 'blog'

    if not blog_dir.exists():
        print(f'[ERROR] ERROR: Blog directory not found: {blog_dir}')
        sys.exit(1)

    print(f'Blog directory: {blog_dir}')
    print()

    # Find all markdown files
    md_files = sorted(blog_dir.glob('*.md'))

    print(f'Found {len(md_files)} markdown files')
    print('-' * 60)

    migrated = []
    for filepath in md_files:
        result = migrate_post(supabase, filepath, dry_run)
        if result:
            migrated.append(result)

    print()
    print('=' * 60)
    print(f'Summary: {len(migrated)} posts {"would be" if dry_run else ""} migrated')
    print('=' * 60)

    if dry_run:
        print()
        print('To actually migrate, run without --dry-run flag:')
        print('  python migrate_posts.py')


if __name__ == '__main__':
    main()
