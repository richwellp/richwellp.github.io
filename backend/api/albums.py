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
                "icon": "✈️",
                "subtitle": "Description",
                "order_index": 1
            }
        ]
    }
    """
    try:
        # Query published albums ordered by order_index
        response = supabase.table('albums') \
            .select('id,slug,name,icon,subtitle,order_index') \
            .eq('published', True) \
            .order('order_index') \
            .execute()

        return jsonify({
            'albums': response.data
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
            .select('url,caption,category,order_index') \
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
                        'type': photo.get('type', 'image')
                    }
                    photos_by_category[category].append(photo_obj)

            return jsonify({
                'album': {
                    'id': album['id'],
                    'slug': album['slug'],
                    'name': album['name'],
                    'icon': album['icon'],
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
                    'caption': photo['caption']
                })

            return jsonify({
                'album': {
                    'id': album['id'],
                    'slug': album['slug'],
                    'name': album['name'],
                    'icon': album['icon'],
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
            'icon': data.get('icon', '📷'),
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

        # Insert photo
        result = supabase.table('photos').insert({
            'album_id': album_id,
            'url': data['url'],
            'caption': data.get('caption', ''),
            'location': data.get('location'),
            'date_taken': data.get('date_taken'),
            'category': data.get('category'),
            'order_index': data.get('order_index', max_order + 1)
        }).execute()

        return jsonify({'photo': result.data[0]}), 201

    except Exception as e:
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
