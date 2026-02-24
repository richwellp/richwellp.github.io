import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'
import { useAdminAuth } from './useAdminAuth'

// Shared state
const albums = ref([])
const photos = ref([])
const loading = ref(false)
const error = ref(null)

export function useAdminAlbums() {
  const { getAuthHeaders } = useAdminAuth()

  const fetchAdminAlbums = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(API_ENDPOINTS.adminAlbums, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        if (response.status === 401) throw new Error('Unauthorized')
        throw new Error('Failed to fetch albums')
      }

      const data = await response.json()
      albums.value = data.albums
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createAlbum = async (albumData) => {
    const response = await fetch(API_ENDPOINTS.adminAlbums, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(albumData)
    })

    if (!response.ok) throw new Error('Failed to create album')
    return await response.json()
  }

  const updateAlbum = async (slug, updates) => {
    const response = await fetch(API_ENDPOINTS.adminAlbum(slug), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(updates)
    })

    if (!response.ok) throw new Error('Failed to update album')
    return await response.json()
  }

  const deleteAlbum = async (slug) => {
    const response = await fetch(API_ENDPOINTS.adminAlbum(slug), {
      method: 'DELETE',
      headers: getAuthHeaders()
    })

    if (!response.ok) throw new Error('Failed to delete album')
  }

  const fetchAlbumPhotos = async (slug, sort = 'order') => {
    loading.value = true
    error.value = null

    try {
      const url = `${API_ENDPOINTS.adminAlbumPhotos(slug)}?sort=${sort}`
      const response = await fetch(url, {
        headers: getAuthHeaders()
      })

      if (!response.ok) throw new Error('Failed to fetch photos')

      const data = await response.json()
      photos.value = data.photos
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createPhoto = async (slug, photoData) => {
    const response = await fetch(API_ENDPOINTS.adminAlbumPhotos(slug), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(photoData)
    })

    if (!response.ok) throw new Error('Failed to create photo')
    return await response.json()
  }

  const updatePhoto = async (photoId, updates) => {
    const response = await fetch(API_ENDPOINTS.adminPhoto(photoId), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(updates)
    })

    if (!response.ok) throw new Error('Failed to update photo')
    return await response.json()
  }

  const deletePhoto = async (photoId) => {
    const response = await fetch(API_ENDPOINTS.adminPhoto(photoId), {
      method: 'DELETE',
      headers: getAuthHeaders()
    })

    if (!response.ok) throw new Error('Failed to delete photo')
  }

  const batchUpdatePhotos = async (slug, photoIds, updates) => {
    const response = await fetch(API_ENDPOINTS.adminAlbumPhotosBatch(slug), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({ photo_ids: photoIds, updates })
    })

    if (!response.ok) throw new Error('Failed to batch update photos')
    return await response.json()
  }

  const reorderPhoto = async (photoId, newOrderIndex) => {
    const response = await fetch(API_ENDPOINTS.adminPhotoReorder(photoId), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({ new_order_index: newOrderIndex })
    })

    if (!response.ok) throw new Error('Failed to reorder photo')
    return await response.json()
  }

  return {
    albums,
    photos,
    loading,
    error,
    fetchAdminAlbums,
    createAlbum,
    updateAlbum,
    deleteAlbum,
    fetchAlbumPhotos,
    createPhoto,
    updatePhoto,
    deletePhoto,
    batchUpdatePhotos,
    reorderPhoto
  }
}
