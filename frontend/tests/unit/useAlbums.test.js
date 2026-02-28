import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAlbums } from '../../src/composables/useAlbums'

// Mock API_ENDPOINTS
vi.mock('../../src/config/api', () => ({
  API_ENDPOINTS: {
    albums: 'http://localhost:5000/albums',
    album: (slug) => `http://localhost:5000/albums/${slug}`
  }
}))

describe('useAlbums', () => {
  let fetchMock

  beforeEach(() => {
    // Reset fetch mock before each test
    fetchMock = vi.fn()
    global.fetch = fetchMock
  })

  describe('fetchAlbums', () => {
    it('should fetch albums successfully', async () => {
      // Arrange
      const mockAlbums = [
        { id: 1, slug: 'travel', name: 'Travel', icon: '✈️' },
        { id: 2, slug: 'me', name: 'Me', icon: '📷' }
      ]

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ albums: mockAlbums })
      })

      const { fetchAlbums, albums, loading, error } = useAlbums()

      // Act
      const result = await fetchAlbums()

      // Assert
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/albums')
      )
      expect(result).toEqual(mockAlbums)
      expect(albums.value).toEqual(mockAlbums)
      expect(loading.value).toBe(false)
      expect(error.value).toBe(null)
    })

    it('should handle empty albums list', async () => {
      // Arrange
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ albums: [] })
      })

      const { fetchAlbums, albums } = useAlbums()

      // Act
      await fetchAlbums()

      // Assert
      expect(albums.value).toEqual([])
    })

    it('should handle fetch error', async () => {
      // Arrange
      fetchMock.mockResolvedValueOnce({
        ok: false,
        statusText: 'Internal Server Error'
      })

      const { fetchAlbums, error } = useAlbums()

      // Act & Assert
      await expect(fetchAlbums()).rejects.toThrow('Failed to fetch albums')
      expect(error.value).toContain('Failed to fetch albums')
    })

    it('should handle network error', async () => {
      // Arrange
      fetchMock.mockRejectedValueOnce(new Error('Network error'))

      const { fetchAlbums, error } = useAlbums()

      // Act & Assert
      await expect(fetchAlbums()).rejects.toThrow('Network error')
      expect(error.value).toBe('Network error')
    })

    it('should set loading state correctly', async () => {
      // Arrange
      fetchMock.mockImplementation(() => new Promise(resolve => {
        setTimeout(() => resolve({
          ok: true,
          json: async () => ({ albums: [] })
        }), 100)
      }))

      const { fetchAlbums, loading } = useAlbums()

      // Act
      const promise = fetchAlbums()
      expect(loading.value).toBe(true)

      await promise
      expect(loading.value).toBe(false)
    })
  })

  describe('fetchAlbumBySlug', () => {
    it('should fetch album with photos successfully', async () => {
      // Arrange
      const mockAlbum = {
        album: { id: 1, slug: 'travel', name: 'Travel' },
        photos: { usa: [{ src: '/photo1.jpg', caption: 'Photo 1' }] },
        categories: ['usa']
      }

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => mockAlbum
      })

      const { fetchAlbumBySlug, loading, error } = useAlbums()

      // Act
      const result = await fetchAlbumBySlug('travel')

      // Assert
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/albums/travel')
      )
      expect(result).toEqual(mockAlbum)
      expect(loading.value).toBe(false)
      expect(error.value).toBe(null)
    })

    it('should handle album not found (404)', async () => {
      // Arrange
      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found'
      })

      const { fetchAlbumBySlug, error } = useAlbums()

      // Act & Assert
      await expect(fetchAlbumBySlug('nonexistent')).rejects.toThrow('Album not found')
      expect(error.value).toBe('Album not found')
    })

    it('should handle server error', async () => {
      // Arrange
      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      })

      const { fetchAlbumBySlug, error } = useAlbums()

      // Act & Assert
      await expect(fetchAlbumBySlug('travel')).rejects.toThrow('Failed to fetch album')
      expect(error.value).toContain('Failed to fetch album')
    })

    it('should handle albums with categories', async () => {
      // Arrange
      const mockAlbum = {
        album: { id: 1, slug: 'travel', name: 'Travel' },
        photos: {
          usa: [{ src: '/1.jpg', caption: 'USA' }],
          japan: [{ src: '/2.jpg', caption: 'Japan' }]
        },
        categories: ['usa', 'japan']
      }

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => mockAlbum
      })

      const { fetchAlbumBySlug } = useAlbums()

      // Act
      const result = await fetchAlbumBySlug('travel')

      // Assert
      expect(result.categories).toHaveLength(2)
      expect(result.photos).toHaveProperty('usa')
      expect(result.photos).toHaveProperty('japan')
    })

    it('should handle albums without categories', async () => {
      // Arrange
      const mockAlbum = {
        album: { id: 2, slug: 'me', name: 'Me' },
        photos: [
          { src: '/1.jpg', caption: 'Photo 1' },
          { src: '/2.jpg', caption: 'Photo 2' }
        ],
        categories: []
      }

      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => mockAlbum
      })

      const { fetchAlbumBySlug } = useAlbums()

      // Act
      const result = await fetchAlbumBySlug('me')

      // Assert
      expect(result.categories).toHaveLength(0)
      expect(Array.isArray(result.photos)).toBe(true)
      expect(result.photos).toHaveLength(2)
    })
  })
})
