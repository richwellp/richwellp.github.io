/**
 * Composable for fetching albums and photos from API
 */
import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'
import { useAsyncRequest } from './useAsyncRequest'

export function useAlbums() {
  const albums = ref([])
  const { loading, error, execute } = useAsyncRequest()

  /**
   * Fetch all published albums
   * @returns {Promise<Array>} Array of albums
   */
  async function fetchAlbums() {
    return await execute(async () => {
      const response = await fetch(API_ENDPOINTS.albums)

      if (!response.ok) {
        throw new Error(`Failed to fetch albums: ${response.statusText}`)
      }

      const data = await response.json()
      albums.value = data.albums || []
      return albums.value
    }).catch(err => {
      console.error('Error fetching albums:', err)
      throw err
    })
  }

  /**
   * Fetch album by slug with photos
   * @param {string} slug - Album slug
   * @returns {Promise<Object>} Album with photos
   */
  async function fetchAlbumBySlug(slug) {
    return await execute(async () => {
      const response = await fetch(API_ENDPOINTS.album(slug))

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Album not found')
        }
        throw new Error(`Failed to fetch album: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    }).catch(err => {
      console.error(`Error fetching album ${slug}:`, err)
      throw err
    })
  }

  return {
    albums,
    loading,
    error,
    fetchAlbums,
    fetchAlbumBySlug
  }
}
