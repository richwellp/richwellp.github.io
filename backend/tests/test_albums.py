import pytest
from api.albums import albums_bp
from unittest.mock import patch, MagicMock
import os


@pytest.fixture
def client():
    """Create a test client for the albums blueprint"""
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(albums_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_headers(monkeypatch):
    """Admin authentication headers for testing"""
    # Patch the ADMIN_KEY in the albums module
    from api import albums
    monkeypatch.setattr(albums, 'ADMIN_KEY', 'test-admin-key')
    return {'Authorization': 'Bearer test-admin-key'}


class TestListAlbums:
    """Test GET /albums - List all published albums"""

    @patch('api.albums.supabase')
    def test_list_albums_success(self, mock_supabase, client):
        """Should return list of published albums ordered by order_index"""
        # Arrange
        mock_albums_data = [
            {
                'id': 1,
                'slug': 'travel',
                'name': 'Travel',
                'subtitle': 'Travel adventures',
                'order_index': 1,
                'published': True
            },
            {
                'id': 2,
                'slug': 'me',
                'name': 'Me',
                'subtitle': 'Personal moments',
                'order_index': 2,
                'published': True
            }
        ]

        # Mock photos for cover photo selection
        mock_photos_data = [
            {'url': 'https://example.com/photo1.jpg'},
            {'url': 'https://example.com/photo2.mp4'}  # Second album has video
        ]

        # Mock table() to return different data for albums vs photos queries
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value.order.return_value.execute.return_value.data = mock_albums_data
            elif table_name == 'photos':
                # Return appropriate photos for each album based on query
                mock_select = MagicMock()
                mock_eq = MagicMock()
                mock_order = MagicMock()

                # photos query returns photos for the album
                mock_order.execute.return_value.data = mock_photos_data
                mock_eq.order.return_value = mock_order
                mock_select.eq.return_value = mock_eq
                mock_table.select.return_value = mock_select
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        # Act
        response = client.get('/albums')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'albums' in data
        assert len(data['albums']) == 2
        assert data['albums'][0]['slug'] == 'travel'
        assert data['albums'][1]['slug'] == 'me'

    @patch('api.albums.supabase')
    def test_list_albums_empty(self, mock_supabase, client):
        """Should return empty list when no published albums"""
        # Arrange
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = []

        # Act
        response = client.get('/albums')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['albums'] == []

    @patch('api.albums.supabase')
    def test_list_albums_database_error(self, mock_supabase, client):
        """Should handle database errors gracefully"""
        # Arrange
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.side_effect = Exception('Database error')

        # Act
        response = client.get('/albums')

        # Assert
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


class TestGetAlbum:
    """Test GET /albums/<slug> - Get album with photos"""

    @patch('api.albums.supabase')
    def test_get_album_success(self, mock_supabase, client):
        """Should return album with photos grouped by category"""
        # Arrange - Mock album query
        mock_album_data = [{
            'id': 1,
            'slug': 'travel',
            'name': 'Travel',
            'icon': '✈️',
            'subtitle': 'Travel adventures',
            'published': True
        }]

        # Mock photos query
        mock_photos_data = [
            {
                'id': 1,
                'url': '/assets/photos/travel/usa1.jpg',
                'caption': 'USA photo',
                'type': 'image',
                'category': 'usa',
                'order_index': 1
            },
            {
                'id': 2,
                'url': '/assets/photos/travel/japan1.jpg',
                'caption': 'Japan photo',
                'type': 'image',
                'category': 'japan',
                'order_index': 1
            }
        ]

        # Setup mock chain for album
        album_mock = MagicMock()
        album_mock.execute.return_value.data = mock_album_data
        mock_supabase.table.return_value.select.return_value.eq.return_value = album_mock

        # Setup mock chain for photos (separate call)
        photos_mock = MagicMock()
        photos_mock.execute.return_value.data = mock_photos_data

        # Configure mock to return different results for album vs photos queries
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value = album_mock
            elif table_name == 'photos':
                mock_table.select.return_value.eq.return_value.order.return_value = photos_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        # Act
        response = client.get('/albums/travel')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'album' in data
        assert data['album']['slug'] == 'travel'
        assert 'photos' in data
        assert 'categories' in data
        assert len(data['categories']) == 2

    @patch('api.albums.supabase')
    def test_get_album_not_found(self, mock_supabase, client):
        """Should return 404 when album doesn't exist"""
        # Arrange
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        # Act
        response = client.get('/albums/nonexistent')

        # Assert
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    @patch('api.albums.supabase')
    def test_get_album_unpublished(self, mock_supabase, client):
        """Should return 404 for unpublished albums"""
        # Arrange
        mock_album_data = [{
            'id': 1,
            'slug': 'sports',
            'name': 'Sports',
            'published': False
        }]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        # Act
        response = client.get('/albums/sports')

        # Assert
        assert response.status_code == 404

    @patch('api.albums.supabase')
    def test_get_album_with_categories(self, mock_supabase, client):
        """Should group photos by category for albums with categories (like Travel)"""
        # Arrange
        mock_album_data = [{'id': 1, 'slug': 'travel', 'name': 'Travel', 'subtitle': 'Travel', 'published': True}]
        mock_photos_data = [
            {'url': '/1.jpg', 'caption': 'Photo 1', 'category': 'usa', 'order_index': 1},
            {'url': '/2.jpg', 'caption': 'Photo 2', 'category': 'usa', 'order_index': 2},
            {'url': '/3.jpg', 'caption': 'Photo 3', 'category': 'japan', 'order_index': 1}
        ]

        album_mock = MagicMock()
        album_mock.execute.return_value.data = mock_album_data
        photos_mock = MagicMock()
        photos_mock.execute.return_value.data = mock_photos_data

        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value = album_mock
            elif table_name == 'photos':
                mock_table.select.return_value.eq.return_value.order.return_value = photos_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        # Act
        response = client.get('/albums/travel')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['categories']) == 2
        assert 'usa' in data['categories']
        assert 'japan' in data['categories']
        assert len(data['photos']['usa']) == 2
        assert len(data['photos']['japan']) == 1

    @patch('api.albums.supabase')
    def test_get_album_without_categories(self, mock_supabase, client):
        """Should return flat photo array for albums without categories (like Me)"""
        # Arrange
        mock_album_data = [{'id': 2, 'slug': 'me', 'name': 'Me', 'subtitle': 'Personal', 'published': True}]
        mock_photos_data = [
            {'url': '/1.jpg', 'caption': 'Photo 1', 'category': None, 'order_index': 1},
            {'url': '/2.jpg', 'caption': 'Photo 2', 'category': None, 'order_index': 2}
        ]

        album_mock = MagicMock()
        album_mock.execute.return_value.data = mock_album_data
        photos_mock = MagicMock()
        photos_mock.execute.return_value.data = mock_photos_data

        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value = album_mock
            elif table_name == 'photos':
                mock_table.select.return_value.eq.return_value.order.return_value = photos_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        # Act
        response = client.get('/albums/me')

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data['photos'], list)
        assert len(data['photos']) == 2
        assert data['categories'] == []


class TestAdminListAlbums:
    """Test GET /admin/albums - List all albums (admin only)"""

    def test_admin_list_albums_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.get('/admin/albums')
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'Unauthorized'

    @patch('api.albums.supabase')
    def test_admin_list_albums_returns_all_albums(self, mock_supabase, client, admin_headers):
        """Should return all albums including unpublished"""
        # Mock albums response
        mock_albums_data = [
            {
                'id': 1,
                'slug': 'travel',
                'name': 'Travel',
                'subtitle': 'Travel photos',
                'categories': ['usa', 'philippines', 'japan'],
                'published': True,
                'order_index': 1
            },
            {
                'id': 3,
                'slug': 'sports',
                'name': 'Sports',
                'subtitle': 'Sports photos',
                'categories': None,
                'published': False,  # Unpublished
                'order_index': 3
            }
        ]

        # Mock photo counts - return list of dicts with album_id
        mock_photos_data = [
            {'album_id': 1},  # 11 photos for travel
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
            {'album_id': 1},
        ]

        albums_mock = MagicMock()
        albums_mock.execute.return_value.data = mock_albums_data

        photos_mock = MagicMock()
        photos_mock.execute.return_value.data = mock_photos_data

        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.order.return_value = albums_mock
            elif table_name == 'photos':
                mock_table.select.return_value = photos_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        response = client.get('/admin/albums', headers=admin_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data['albums']) == 2
        assert data['albums'][0]['photo_count'] == 11
        assert data['albums'][1]['photo_count'] == 0
        # Should include unpublished albums
        assert any(album['slug'] == 'sports' for album in data['albums'])


class TestAdminCreateAlbum:
    """Test POST /admin/albums - Create album"""

    def test_admin_create_album_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.post('/admin/albums', json={
            'slug': 'food',
            'name': 'Food',
        })
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_create_album_succeeds(self, mock_supabase, client, admin_headers):
        """Should create album with valid data"""
        mock_response = MagicMock()
        mock_response.data = [{
            'id': 4,
            'slug': 'food',
            'name': 'Food',
            'icon': '🍜',
            'subtitle': 'Culinary adventures',
            'categories': ['japanese', 'filipino'],
            'published': True,
            'order_index': 4
        }]

        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response

        response = client.post('/admin/albums',
            headers=admin_headers,
            json={
                'slug': 'food',
                'name': 'Food',
                'icon': '🍜',
                'subtitle': 'Culinary adventures',
                'categories': ['japanese', 'filipino'],
                'published': True,
                'order_index': 4
            }
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['album']['slug'] == 'food'
        assert data['album']['name'] == 'Food'


class TestAdminUpdateAlbum:
    """Test PUT /admin/albums/:slug - Update album"""

    def test_admin_update_album_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.put('/admin/albums/travel', json={'name': 'Updated'})
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_update_album_succeeds(self, mock_supabase, client, admin_headers):
        """Should update album"""
        mock_response = MagicMock()
        mock_response.data = [{
            'slug': 'travel',
            'name': 'Updated Travel',
            'categories': ['usa', 'canada']
        }]

        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

        response = client.put('/admin/albums/travel',
            headers=admin_headers,
            json={
                'name': 'Updated Travel',
                'categories': ['usa', 'canada']
            }
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['album']['name'] == 'Updated Travel'


class TestAdminDeleteAlbum:
    """Test DELETE /admin/albums/:slug - Delete album"""

    def test_admin_delete_album_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.delete('/admin/albums/sports')
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_delete_album_succeeds(self, mock_supabase, client, admin_headers):
        """Should delete album"""
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock()

        response = client.delete('/admin/albums/sports', headers=admin_headers)

        assert response.status_code == 204


class TestAdminListPhotos:
    """Test GET /admin/albums/:slug/photos - List photos (admin only)"""

    def test_admin_list_photos_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.get('/admin/albums/travel/photos')
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_list_photos_returns_all_photos(self, mock_supabase, client, admin_headers):
        """Should return all photos including unpublished"""
        album_mock = MagicMock()
        album_mock.execute.return_value.data = {'id': 1, 'slug': 'travel', 'name': 'Travel'}

        photos_mock = MagicMock()
        photos_mock.execute.return_value.data = [
            {
                'id': 1,
                'album_id': 1,
                'url': '/assets/photos/travel/1.jpg',
                'caption': 'Photo 1',
                'category': 'usa',
                'order_index': 1,
                'published': True
            },
            {
                'id': 2,
                'album_id': 1,
                'url': '/assets/photos/travel/2.jpg',
                'caption': 'Photo 2',
                'category': 'usa',
                'order_index': 2,
                'published': False  # Unpublished
            }
        ]

        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value.single.return_value = album_mock
            elif table_name == 'photos':
                mock_table.select.return_value.eq.return_value.order.return_value = photos_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        response = client.get('/admin/albums/travel/photos', headers=admin_headers)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data['photos']) == 2
        # Should include unpublished photos
        assert any(photo['published'] == False for photo in data['photos'])


class TestAdminCreatePhoto:
    """Test POST /admin/albums/:slug/photos - Create photo"""

    def test_admin_create_photo_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.post('/admin/albums/travel/photos', json={
            'file_path': 'https://example.com/photo.jpg'
        })
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_create_photo_succeeds(self, mock_supabase, client, admin_headers):
        """Should create photo"""
        album_mock = MagicMock()
        album_mock.execute.return_value.data = {'id': 1, 'slug': 'travel'}

        max_order_mock = MagicMock()
        max_order_mock.execute.return_value.data = [{'order_index': 10}]

        photo_mock = MagicMock()
        photo_mock.execute.return_value.data = [{
            'id': 100,
            'album_id': 1,
            'url': 'https://example.com/photo.jpg',
            'caption': 'New photo',
            'category': 'usa',
            'order_index': 11
        }]

        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'albums':
                mock_table.select.return_value.eq.return_value.single.return_value = album_mock
            elif table_name == 'photos':
                # For max order query
                mock_table.select.return_value.eq.return_value.order.return_value.limit.return_value = max_order_mock
                # For insert
                mock_table.insert.return_value = photo_mock
            return mock_table

        mock_supabase.table.side_effect = table_side_effect

        response = client.post('/admin/albums/travel/photos',
            headers=admin_headers,
            json={
                'url': 'https://example.com/photo.jpg',
                'caption': 'New photo',
                'category': 'usa'
            }
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['photo']['url'] == 'https://example.com/photo.jpg'


class TestAdminUpdatePhoto:
    """Test PUT /admin/photos/:photo_id - Update photo"""

    def test_admin_update_photo_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.put('/admin/photos/1', json={'caption': 'Updated'})
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_update_photo_succeeds(self, mock_supabase, client, admin_headers):
        """Should update photo"""
        mock_response = MagicMock()
        mock_response.data = [{
            'id': 1,
            'caption': 'Updated caption',
            'category': 'philippines'
        }]

        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

        response = client.put('/admin/photos/1',
            headers=admin_headers,
            json={
                'caption': 'Updated caption',
                'category': 'philippines'
            }
        )

        assert response.status_code == 200


class TestAdminDeletePhoto:
    """Test DELETE /admin/photos/:photo_id - Delete photo"""

    def test_admin_delete_photo_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.delete('/admin/photos/1')
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_delete_photo_succeeds(self, mock_supabase, client, admin_headers):
        """Should delete photo"""
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock()

        response = client.delete('/admin/photos/1', headers=admin_headers)

        assert response.status_code == 204


class TestAdminBatchUpdatePhotos:
    """Test PUT /admin/albums/:slug/photos/batch - Batch update photos"""

    def test_admin_batch_update_photos_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.put('/admin/albums/travel/photos/batch', json={
            'photo_ids': [1, 2, 3],
            'updates': {'category': 'usa'}
        })
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_batch_update_photos_succeeds(self, mock_supabase, client, admin_headers):
        """Should update multiple photos"""
        mock_response = MagicMock()
        mock_response.data = [
            {'id': 1, 'category': 'usa'},
            {'id': 2, 'category': 'usa'},
            {'id': 3, 'category': 'usa'}
        ]

        mock_supabase.table.return_value.update.return_value.in_.return_value.execute.return_value = mock_response

        response = client.put('/admin/albums/travel/photos/batch',
            headers=admin_headers,
            json={
                'photo_ids': [1, 2, 3],
                'updates': {'category': 'usa'}
            }
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['updated_count'] == 3


class TestAdminReorderPhoto:
    """Test PUT /admin/photos/:photo_id/reorder - Reorder photo"""

    def test_admin_reorder_photo_requires_auth(self, client):
        """Should return 401 without auth"""
        response = client.put('/admin/photos/5/reorder', json={'new_order_index': 1})
        assert response.status_code == 401

    @patch('api.albums.supabase')
    def test_admin_reorder_photo_succeeds(self, mock_supabase, client, admin_headers):
        """Should update order_index"""
        mock_response = MagicMock()
        mock_response.data = [{'id': 5, 'order_index': 1}]

        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response

        response = client.put('/admin/photos/5/reorder',
            headers=admin_headers,
            json={'new_order_index': 1}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['photo']['order_index'] == 1


class TestAdminUpload:
    """Test POST /admin/upload - Upload file to storage"""

    def test_admin_upload_requires_auth(self, client):
        """Should return 401 without auth"""
        from io import BytesIO
        data = {
            'file': (BytesIO(b'fake image data'), 'test.jpg'),
            'album': 'sports'
        }
        response = client.post('/admin/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 401

    def test_admin_upload_requires_file(self, client, admin_headers):
        """Should return 400 if no file provided"""
        response = client.post('/admin/upload',
            headers=admin_headers,
            data={'album': 'sports'},
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'No file' in data['error']

    def test_admin_upload_requires_album(self, client, admin_headers):
        """Should return 400 if no album slug provided"""
        from io import BytesIO
        data = {
            'file': (BytesIO(b'fake image data'), 'test.jpg')
        }
        response = client.post('/admin/upload',
            headers=admin_headers,
            data=data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'Album slug required' in data['error']

    @patch('api.albums.supabase')
    def test_admin_upload_succeeds(self, mock_supabase, client, admin_headers):
        """Should upload file and return URL"""
        from io import BytesIO

        # Mock storage upload
        mock_storage = MagicMock()
        mock_supabase.storage.from_.return_value = mock_storage

        # Mock successful upload
        mock_upload_response = MagicMock()
        mock_upload_response.error = None
        mock_storage.upload.return_value = mock_upload_response

        # Mock public URL
        mock_storage.get_public_url.return_value = 'https://storage.supabase.co/object/public/photos/sports/test.jpg'

        data = {
            'file': (BytesIO(b'fake image data'), 'test.jpg'),
            'album': 'sports'
        }
        response = client.post('/admin/upload',
            headers=admin_headers,
            data=data,
            content_type='multipart/form-data'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'url' in data
        assert 'path' in data
        assert 'sports' in data['path']
