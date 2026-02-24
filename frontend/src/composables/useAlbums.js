/**
 * Composable for fetching albums and photos from API
 */
import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'

export function useAlbums() {
  const albums = ref([])
  const loading = ref(false)
  const error = ref(null)

  /**
   * Fetch all published albums
   * @returns {Promise<Array>} Array of albums
   */
  async function fetchAlbums() {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(API_ENDPOINTS.albums, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch albums: ${response.statusText}`)
      }

      const data = await response.json()
      albums.value = data.albums || []
      return albums.value
    } catch (err) {
      console.error('Error fetching albums:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch album by slug with photos
   * @param {string} slug - Album slug
   * @returns {Promise<Object>} Album with photos
   */
  async function fetchAlbumBySlug(slug) {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(API_ENDPOINTS.album(slug), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Album not found')
        }
        throw new Error(`Failed to fetch album: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (err) {
      console.error(`Error fetching album ${slug}:`, err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    albums,
    loading,
    error,
    fetchAlbums,
    fetchAlbumBySlug
  }
}
