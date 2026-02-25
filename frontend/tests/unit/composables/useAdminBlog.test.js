import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAdminBlog } from '@/composables/useAdminBlog'

// Mock fetch globally
global.fetch = vi.fn()

describe('useAdminBlog', () => {
  beforeEach(() => {
    // Reset fetch mock
    vi.clearAllMocks()
  })

  describe('fetchAdminPosts', () => {
    it('fetches all posts with auth headers', async () => {
      const mockPosts = [
        { slug: 'draft-post', title: 'Draft', published: false },
        { slug: 'published-post', title: 'Published', published: true }
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: mockPosts, page: 1, per_page: 10 })
      })

      const { fetchAdminPosts, posts } = useAdminBlog()
      await fetchAdminPosts()

      // Verify request made to correct endpoint
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/admin/blog/posts'),
        expect.objectContaining({
          method: 'GET',
          headers: expect.any(Object)
        })
      )

      expect(posts.value).toEqual(mockPosts)
    })

    it('handles status filter parameter', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ posts: [], page: 1, per_page: 10 })
      })

      const { fetchAdminPosts } = useAdminBlog()
      await fetchAdminPosts({ status: 'draft' })

      const callUrl = global.fetch.mock.calls[0][0]
      expect(callUrl).toContain('status=draft')
    })

    it('throws on 401 unauthorized', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401
      })

      const { fetchAdminPosts } = useAdminBlog()

      await expect(fetchAdminPosts()).rejects.toThrow('Unauthorized')
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

      const { fetchAdminPosts, loading } = useAdminBlog()

      const promise = fetchAdminPosts()
      expect(loading.value).toBe(true)

      await promise
      expect(loading.value).toBe(false)
    })
  })

  describe('getAdminPost', () => {
    it('fetches single post with auth', async () => {
      const mockPost = {
        slug: 'test-post',
        title: 'Test Post',
        content: '# Hello',
        published: false
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockPost
      })

      const { getAdminPost } = useAdminBlog()
      const post = await getAdminPost('test-post')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/admin/blog/posts/test-post'),
        expect.objectContaining({
          method: 'GET',
          headers: expect.any(Object)
        })
      )

      expect(post).toEqual(mockPost)
    })

    it('throws on 404', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 404
      })

      const { getAdminPost } = useAdminBlog()

      await expect(getAdminPost('nonexistent')).rejects.toThrow('Post not found')
    })
  })

  describe('createPost', () => {
    it('creates post with auth header', async () => {
      const postData = {
        slug: 'new-post',
        title: 'New Post',
        content: '# Hello',
        published: false
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({ ...postData, id: 1 })
      })

      const { createPost } = useAdminBlog()
      const result = await createPost(postData)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/admin/blog/posts'),
        expect.objectContaining({
          method: 'POST',
          headers: expect.any(Object),
          body: JSON.stringify(postData)
        })
      )

      expect(result.id).toBe(1)
    })

    it('throws on 401 unauthorized', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401
      })

      const { createPost } = useAdminBlog()

      await expect(createPost({})).rejects.toThrow('Unauthorized')
    })
  })

  describe('updatePost', () => {
    it('updates post with auth header', async () => {
      const updateData = { title: 'Updated Title' }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ slug: 'test-post', ...updateData })
      })

      const { updatePost } = useAdminBlog()
      await updatePost('test-post', updateData)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/admin/blog/posts/test-post'),
        expect.objectContaining({
          method: 'PUT',
          headers: expect.any(Object),
          body: JSON.stringify(updateData)
        })
      )
    })
  })

  describe('deletePost', () => {
    it('deletes post with auth header', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 204
      })

      const { deletePost } = useAdminBlog()
      const result = await deletePost('test-post')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/admin/blog/posts/test-post'),
        expect.objectContaining({
          method: 'DELETE',
          headers: expect.any(Object)
        })
      )

      expect(result).toBe(true)
    })

    it('throws on 401 unauthorized', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401
      })

      const { deletePost } = useAdminBlog()

      await expect(deletePost('test-post')).rejects.toThrow('Unauthorized')
    })
  })
})
