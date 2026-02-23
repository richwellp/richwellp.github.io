import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAdminBlog } from '@/composables/useAdminBlog'
import { useAdminAuth } from '@/composables/useAdminAuth'

// Mock fetch globally
global.fetch = vi.fn()

describe('useAdminBlog', () => {
  beforeEach(() => {
    // Reset fetch mock and auth state
    vi.clearAllMocks()
    const { logout } = useAdminAuth()
    logout()
  })

  describe('fetchAdminPosts', () => {
    it('fetches all posts with auth header', async () => {
      const { login } = useAdminAuth()
      login('test-admin-key')

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

      // Verify auth header sent
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/admin/posts'),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-admin-key'
          })
        })
      )

      expect(posts.value).toEqual(mockPosts)
    })

    it('handles status filter parameter', async () => {
      const { login } = useAdminAuth()
      login('test-key')

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
      const { login } = useAdminAuth()
      login('test-key')

      global.fetch.mockImplementationOnce(() =>
        new Promise(resolve => {
          setTimeout(() => {
            resolve({
              ok: true,
              json: async () => ({ posts: [] })
            })
          }, 10)
        })
      )

      const { loading, fetchAdminPosts } = useAdminBlog()

      expect(loading.value).toBe(false)

      const promise = fetchAdminPosts()
      expect(loading.value).toBe(true)

      await promise
      expect(loading.value).toBe(false)
    })
  })

  describe('getAdminPost', () => {
    it('fetches single post with auth', async () => {
      const { login } = useAdminAuth()
      login('test-key')

      const mockPost = {
        slug: 'test-post',
        title: 'Test Post',
        content: '# Content',
        published: false
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockPost
      })

      const { getAdminPost } = useAdminBlog()
      const post = await getAdminPost('test-post')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/admin/posts/test-post'),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-key'
          })
        })
      )

      expect(post).toEqual(mockPost)
    })

    it('throws on 404', async () => {
      const { login } = useAdminAuth()
      login('test-key')

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
      const { login } = useAdminAuth()
      login('test-key')

      const postData = {
        slug: 'new-post',
        title: 'New Post',
        content: '# Hello',
        published: false
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({ ...postData, id: '123' })
      })

      const { createPost } = useAdminBlog()
      const result = await createPost(postData)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/posts'),
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-key'
          }),
          body: JSON.stringify(postData)
        })
      )

      expect(result.id).toBe('123')
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
      const { login } = useAdminAuth()
      login('test-key')

      const updateData = { title: 'Updated Title' }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ slug: 'test-post', ...updateData })
      })

      const { updatePost } = useAdminBlog()
      await updatePost('test-post', updateData)

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/posts/test-post'),
        expect.objectContaining({
          method: 'PUT',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-key'
          }),
          body: JSON.stringify(updateData)
        })
      )
    })
  })

  describe('deletePost', () => {
    it('deletes post with auth header', async () => {
      const { login } = useAdminAuth()
      login('test-key')

      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 204
      })

      const { deletePost } = useAdminBlog()
      const result = await deletePost('test-post')

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/blog/posts/test-post'),
        expect.objectContaining({
          method: 'DELETE',
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-key'
          })
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
