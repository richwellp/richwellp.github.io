import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'
import { useAdminAuth } from './useAdminAuth'

// Shared state across all instances
const posts = ref([])
const loading = ref(false)
const error = ref(null)

export function useAdminBlog() {
  const { getAuthHeaders } = useAdminAuth()

  const fetchAdminPosts = async (options = {}) => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      if (options.page) params.set('page', options.page)
      if (options.per_page) params.set('per_page', options.per_page)
      if (options.status) params.set('status', options.status)

      const response = await fetch(`${API_ENDPOINTS.adminPosts}?${params}`, {
        headers: {
          ...getAuthHeaders()
        }
      })

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Unauthorized')
        }
        throw new Error('Failed to fetch admin posts')
      }

      const data = await response.json()
      posts.value = data.posts
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getAdminPost = async (slug) => {
    const response = await fetch(API_ENDPOINTS.adminPost(slug), {
      headers: {
        ...getAuthHeaders()
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized')
      }
      if (response.status === 404) {
        throw new Error('Post not found')
      }
      throw new Error('Failed to fetch post')
    }

    return await response.json()
  }

  const createPost = async (postData) => {
    const response = await fetch(API_ENDPOINTS.adminCreatePost, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(postData)
    })

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized')
      }
      const data = await response.json()
      throw new Error(data.error || 'Failed to create post')
    }

    return await response.json()
  }

  const updatePost = async (slug, postData) => {
    const response = await fetch(API_ENDPOINTS.adminUpdatePost(slug), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(postData)
    })

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized')
      }
      if (response.status === 404) {
        throw new Error('Post not found')
      }
      const data = await response.json()
      throw new Error(data.error || 'Failed to update post')
    }

    return await response.json()
  }

  const deletePost = async (slug) => {
    const response = await fetch(API_ENDPOINTS.adminDeletePost(slug), {
      method: 'DELETE',
      headers: {
        ...getAuthHeaders()
      }
    })

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized')
      }
      if (response.status === 404) {
        throw new Error('Post not found')
      }
      throw new Error('Failed to delete post')
    }

    // 204 No Content - success
    return true
  }

  return {
    posts,
    loading,
    error,
    fetchAdminPosts,
    getAdminPost,
    createPost,
    updatePost,
    deletePost
  }
}
