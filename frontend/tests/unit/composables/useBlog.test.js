import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useBlog } from '@/composables/useBlog'

// Mock fetch globally
global.fetch = vi.fn()

describe('useBlog', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.clearAllMocks()
  })

  describe('fetchPosts', () => {
    it('calls API and updates posts ref', async () => {
      const mockPosts = [
        {
          slug: 'post-1',
          title: 'Post 1',
          excerpt: 'Excerpt 1',
          author: 'Richwell Perez',
          tags: ['python'],
          published_at: '2024-01-01T00:00:00Z',
          reading_time: 5
        },
        {
          slug: 'post-2',
          title: 'Post 2',
          excerpt: 'Excerpt 2',
          author: 'Richwell Perez',
          tags: ['javascript'],
          published_at: '2024-01-02T00:00:00Z',
          reading_time: 3
        }
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: mockPosts, page: 1, per_page: 10 })
      })

      const { posts, loading, fetchPosts } = useBlog()

      // Initially empty
      expect(posts.value).toEqual([])
      expect(loading.value).toBe(false)

      // Call fetchPosts
      await fetchPosts()

      // Verify API was called correctly
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/posts?')
      )
      expect(global.fetch).toHaveBeenCalledTimes(1)

      // Verify posts were updated
      expect(posts.value).toEqual(mockPosts)
      expect(loading.value).toBe(false)
    })

    it('handles pagination parameters', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: [], page: 2, per_page: 5 })
      })

      const { fetchPosts } = useBlog()
      await fetchPosts({ page: 2, per_page: 5 })

      const callUrl = global.fetch.mock.calls[0][0]
      expect(callUrl).toContain('page=2')
      expect(callUrl).toContain('per_page=5')
    })

    it('handles tag filtering', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: [], page: 1, per_page: 10 })
      })

      const { fetchPosts } = useBlog()
      await fetchPosts({ tag: 'python' })

      const callUrl = global.fetch.mock.calls[0][0]
      expect(callUrl).toContain('tag=python')
    })

    it('sets loading state correctly', async () => {
      global.fetch.mockImplementationOnce(() =>
        new Promise(resolve => {
          setTimeout(() => {
            resolve({
              ok: true,
              json: async () => ({ posts: [], page: 1, per_page: 10 })
            })
          }, 10)
        })
      )

      const { loading, fetchPosts } = useBlog()

      expect(loading.value).toBe(false)

      const promise = fetchPosts()
      expect(loading.value).toBe(true)

      await promise
      expect(loading.value).toBe(false)
    })

    it('handles errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      const { error, fetchPosts } = useBlog()

      await fetchPosts()

      expect(error.value).toBe('Network error')
    })

    it('handles non-ok responses', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500
      })

      const { error, fetchPosts } = useBlog()

      await fetchPosts()

      expect(error.value).toBeTruthy()
    })
  })

  describe('getPostBySlug', () => {
    it('fetches single post', async () => {
      const mockPost = {
        slug: 'test-post',
        title: 'Test Post',
        content: '# Test\n\n## Section',
        excerpt: 'Excerpt',
        author: 'Richwell Perez',
        tags: ['test'],
        published_at: '2024-01-01T00:00:00Z',
        reading_time: 5,
        headings: [{ level: 2, text: 'Section', id: 'section' }]
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockPost
      })

      const { getPostBySlug } = useBlog()
      const post = await getPostBySlug('test-post')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/posts/test-post')
      )
      expect(post).toEqual(mockPost)
    })

    it('throws on 404', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404
      })

      const { getPostBySlug } = useBlog()

      await expect(getPostBySlug('nonexistent')).rejects.toThrow()
    })
  })

  describe('searchPosts', () => {
    it('queries API with encoded query', async () => {
      const mockResults = [
        { slug: 'post-1', title: 'Python Tutorial' },
        { slug: 'post-2', title: 'Advanced Python' }
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: mockResults, total: 2 })
      })

      const { searchPosts } = useBlog()
      const results = await searchPosts('python')

      const callUrl = global.fetch.mock.calls[0][0]
      expect(callUrl).toContain('/blog/search')
      expect(callUrl).toContain('q=python')
      expect(results.posts).toEqual(mockResults)
      expect(results.total).toBe(2)
    })

    it('encodes special characters in query', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: [], total: 0 })
      })

      const { searchPosts } = useBlog()
      await searchPosts('test & query')

      const callUrl = global.fetch.mock.calls[0][0]
      expect(callUrl).toContain('q=test%20%26%20query')
    })

    it('returns empty results for empty query', async () => {
      const { searchPosts } = useBlog()

      // Should not call API for empty query
      const results = await searchPosts('')

      expect(global.fetch).not.toHaveBeenCalled()
      expect(results.posts).toEqual([])
      expect(results.total).toBe(0)
    })
  })
})
