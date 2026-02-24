"""
Albums API Blueprint
Endpoints for fetching albums and photos from Supabase
"""
from flask import Blueprint, jsonify, request
from supabase import create_client
from functools import wraps
import os

albums_bp = Blueprint('albums', __name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# Admin authentication (same as blog)
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


@albums_bp.route('/albums', methods=['GET'])
def list_albums():
    """
    GET /albums
    Returns list of all published albums ordered by order_index

    Response:
    {
        "albums": [
            {
                "id": 1,
                "slug": "travel",
                "name": "Travel",
                "subtitle": "Description",
                "order_index": 1,
                "cover_photo": "https://..."
            }
        ]
    }
    """
    try:
        # Query published albums ordered by order_index
        response = supabase.table('albums') \
            .select('id,slug,name,subtitle,order_index,published') \
            .eq('published', True) \
            .order('order_index') \
            .execute()

        albums = response.data

        # For each album, get the first photo as cover photo
        for album in albums:
            photos_response = supabase.table('photos') \
                .select('url') \
                .eq('album_id', album['id']) \
                .order('order_index') \
                .limit(1) \
                .execute()

            if photos_response.data and len(photos_response.data) > 0:
                album['cover_photo'] = photos_response.data[0]['url']
            else:
                album['cover_photo'] = None

        return jsonify({
            'albums': albums
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch albums',
            'details': str(e)
        }), 500


@albums_bp.route('/albums/<slug>', methods=['GET'])
def get_album(slug):
    """
    GET /albums/<slug>
    Returns album details with photos

    For albums with categories (like Travel):
    {
        "album": {...},
        "photos": {
            "usa": [...],
            "japan": [...]
        },
        "categories": ["usa", "japan"]
    }

    For albums without categories (like Me):
    {
        "album": {...},
        "photos": [...],
        "categories": []
    }
    """
    try:
        # Get album
        album_response = supabase.table('albums') \
            .select('*') \
            .eq('slug', slug) \
            .execute()

        if not album_response.data:
            return jsonify({
                'error': 'Album not found'
            }), 404

        album = album_response.data[0]

        # Check if published
        if not album.get('published'):
            return jsonify({
                'error': 'Album not found'
            }), 404

        # Get photos for this album
        photos_response = supabase.table('photos') \
            .select('url,caption,category,order_index,date_taken,location') \
            .eq('album_id', album['id']) \
            .order('order_index') \
            .execute()

        photos_data = photos_response.data

        # Group photos by category if they have categories
        has_categories = any(photo.get('category') for photo in photos_data)

        if has_categories:
            # Group by category
            photos_by_category = {}
            categories = []

            for photo in photos_data:
                category = photo.get('category')
                if category:
                    if category not in photos_by_category:
                        photos_by_category[category] = []
                        categories.append(category)

                    # Remove category from photo object (not needed in frontend)
                    photo_obj = {
                        'src': photo['url'],
                        'caption': photo['caption'],
                        'type': photo.get('type', 'image'),
                        'date_taken': photo.get('date_taken'),
                        'location': photo.get('location'),
                        'order_index': photo['order_index']
                    }
                    photos_by_category[category].append(photo_obj)

            return jsonify({
                'album': {
                    'id': album['id'],
                    'slug': album['slug'],
                    'name': album['name'],
                    'subtitle': album['subtitle']
                },
                'photos': photos_by_category,
                'categories': categories
            }), 200
        else:
            # Flat array of photos (no categories)
            photos_array = []
            for photo in photos_data:
                photos_array.append({
                    'src': photo['url'],
                    'caption': photo['caption'],
                    'type': photo.get('type', 'image'),
                    'date_taken': photo.get('date_taken'),
                    'location': photo.get('location'),
                    'order_index': photo['order_index']
                })

            return jsonify({
                'album': {
                    'id': album['id'],
                    'slug': album['slug'],
                    'name': album['name'],
                    'subtitle': album['subtitle']
                },
                'photos': photos_array,
                'categories': []
            }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch album',
            'details': str(e)
        }), 500


# ============================================
# ADMIN ENDPOINTS (require authentication)
# ============================================

@albums_bp.route('/admin/albums', methods=['GET'])
@require_admin
def admin_list_albums():
    """
    GET /admin/albums
    Returns all albums (including unpublished) with photo counts
    Requires admin authentication
    """
    try:
        # Fetch all albums (no published filter)
        albums_response = supabase.table('albums') \
            .select('*') \
            .order('order_index') \
            .execute()

        albums = albums_response.data

        # Get photo counts for each album
        photo_counts_response = supabase.table('photos') \
            .select('album_id') \
            .execute()

        # Build photo count map
        photo_counts = {}
        for row in photo_counts_response.data:
            album_id = row.get('album_id')
            photo_counts[album_id] = photo_counts.get(album_id, 0) + 1

        # Add photo_count to each album
        for album in albums:
            album['photo_count'] = photo_counts.get(album['id'], 0)

        return jsonify({'albums': albums}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/albums', methods=['POST'])
@require_admin
def admin_create_album():
    """
    POST /admin/albums
    Create a new album
    """
    try:
        data = request.json

        # Insert album
        result = supabase.table('albums').insert({
            'slug': data['slug'],
            'name': data['name'],
            'subtitle': data.get('subtitle', ''),
            'categories': data.get('categories'),
            'published': data.get('published', True),
            'order_index': data.get('order_index', 0)
        }).execute()

        return jsonify({'album': result.data[0]}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/albums/<slug>', methods=['PUT'])
@require_admin
def admin_update_album(slug):
    """
    PUT /admin/albums/:slug
    Update album metadata
    """
    try:
        data = request.json

        result = supabase.table('albums').update(data).eq('slug', slug).execute()

        if not result.data:
            return jsonify({'error': 'Album not found'}), 404

        return jsonify({'album': result.data[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/albums/<slug>', methods=['DELETE'])
@require_admin
def admin_delete_album(slug):
    """
    DELETE /admin/albums/:slug
    Delete album and all its photos (CASCADE)
    """
    try:
        supabase.table('albums').delete().eq('slug', slug).execute()
        return '', 204

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# PHOTO MANAGEMENT
# ============================================

@albums_bp.route('/admin/albums/<slug>/photos', methods=['GET'])
@require_admin
def admin_list_photos(slug):
    """
    GET /admin/albums/:slug/photos
    Returns all photos in album (including unpublished)
    Query params: ?sort=upload_date|file_name|caption|category
    """
    try:
        # Get album
        album_response = supabase.table('albums').select('id,slug,name').eq('slug', slug).single().execute()

        if not album_response.data:
            return jsonify({'error': 'Album not found'}), 404

        album_id = album_response.data['id']

        # Get sort parameter
        sort_by = request.args.get('sort', 'order_index')

        # Map sort parameter to column
        sort_map = {
            'upload_date': 'created_at',
            'file_name': 'url',
            'caption': 'caption',
            'category': 'category',
            'order': 'order_index'
        }

        sort_column = sort_map.get(sort_by, 'order_index')

        # Fetch all photos (no published filter)
        photos_response = supabase.table('photos') \
            .select('*') \
            .eq('album_id', album_id) \
            .order(sort_column) \
            .execute()

        return jsonify({'photos': photos_response.data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/upload', methods=['POST'])
@require_admin
def admin_upload_file():
    """
    POST /admin/upload
    Upload file to Supabase Storage (bypasses RLS using service role)
    Expects multipart/form-data with 'file' and 'album' fields
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        album_slug = request.form.get('album')

        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not album_slug:
            return jsonify({'error': 'Album slug required'}), 400

        # Generate unique filename
        import time
        import random
        import string
        file_ext = file.filename.rsplit('.', 1)[1] if '.' in file.filename else 'jpg'
        timestamp = int(time.time() * 1000)
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        filename = f"{timestamp}-{random_str}.{file_ext}"
        filepath = f"{album_slug}/{filename}"

        # Read file content
        file_content = file.read()

        # Upload to Supabase Storage (service role bypasses RLS)
        upload_response = supabase.storage.from_('photos').upload(
            filepath,
            file_content,
            {
                'content-type': file.content_type,
                'cache-control': '3600',
                'upsert': 'false'
            }
        )

        # Check for errors
        if hasattr(upload_response, 'error') and upload_response.error:
            return jsonify({'error': f'Upload failed: {upload_response.error}'}), 500

        # Get public URL
        public_url_response = supabase.storage.from_('photos').get_public_url(filepath)

        return jsonify({
            'url': public_url_response,
            'path': filepath
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/albums/<slug>/photos', methods=['POST'])
@require_admin
def admin_create_photo(slug):
    """
    POST /admin/albums/:slug/photos
    Create a new photo in album
    """
    try:
        data = request.json

        # Get album ID
        album_response = supabase.table('albums').select('id').eq('slug', slug).single().execute()

        if not album_response.data:
            return jsonify({'error': 'Album not found'}), 404

        album_id = album_response.data['id']

        # Get max order_index for this album
        max_order_response = supabase.table('photos') \
            .select('order_index') \
            .eq('album_id', album_id) \
            .order('order_index', desc=True) \
            .limit(1) \
            .execute()

        max_order = max_order_response.data[0]['order_index'] if max_order_response.data else 0

        # Build insert data - only include type if column exists
        insert_data = {
            'album_id': album_id,
            'url': data['url'],
            'caption': data.get('caption', ''),
            'location': data.get('location'),
            'date_taken': data.get('date_taken'),
            'category': data.get('category'),
            'order_index': data.get('order_index', max_order + 1)
        }

        # Include type if provided (for future compatibility)
        if 'type' in data:
            insert_data['type'] = data['type']

        # Insert photo
        result = supabase.table('photos').insert(insert_data).execute()

        return jsonify({'photo': result.data[0]}), 201

    except Exception as e:
        print(f"Error creating photo in album '{slug}': {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Request data: {request.json}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/photos/<photo_id>', methods=['PUT'])
@require_admin
def admin_update_photo(photo_id):
    """
    PUT /admin/photos/:photo_id
    Update photo metadata
    """
    try:
        data = request.json

        result = supabase.table('photos').update(data).eq('id', photo_id).execute()

        if not result.data:
            return jsonify({'error': 'Photo not found'}), 404

        return jsonify({'photo': result.data[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/photos/<photo_id>', methods=['DELETE'])
@require_admin
def admin_delete_photo(photo_id):
    """
    DELETE /admin/photos/:photo_id
    Delete photo
    """
    try:
        supabase.table('photos').delete().eq('id', photo_id).execute()
        return '', 204

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/albums/<slug>/photos/batch', methods=['PUT'])
@require_admin
def admin_batch_update_photos(slug):
    """
    PUT /admin/albums/:slug/photos/batch
    Update multiple photos at once
    Body: { photo_ids: [1,2,3], updates: { category: 'usa' } }
    """
    try:
        data = request.json
        photo_ids = data.get('photo_ids', [])
        updates = data.get('updates', {})

        if not photo_ids or not updates:
            return jsonify({'error': 'photo_ids and updates required'}), 400

        # Update all photos with given IDs
        result = supabase.table('photos') \
            .update(updates) \
            .in_('id', photo_ids) \
            .execute()

        return jsonify({'updated_count': len(result.data)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@albums_bp.route('/admin/photos/<int:photo_id>/reorder', methods=['PUT'])
@require_admin
def admin_reorder_photo(photo_id):
    """
    PUT /admin/photos/:photo_id/reorder
    Update photo order_index
    Body: { new_order_index: 5 }
    """
    try:
        data = request.json
        new_order_index = data.get('new_order_index')

        if new_order_index is None:
            return jsonify({'error': 'new_order_index required'}), 400

        result = supabase.table('photos') \
            .update({'order_index': new_order_index}) \
            .eq('id', photo_id) \
            .execute()

        if not result.data:
            return jsonify({'error': 'Photo not found'}), 404

        return jsonify({'photo': result.data[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
