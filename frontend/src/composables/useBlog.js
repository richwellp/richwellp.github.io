import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'

const posts = ref([])
const loading = ref(false)
const error = ref(null)

export function useBlog() {
  const fetchPosts = async (options = {}) => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      if (options.page) params.set('page', options.page)
      if (options.per_page) params.set('per_page', options.per_page)
      if (options.tag) params.set('tag', options.tag)

      const response = await fetch(`${API_ENDPOINTS.blogPosts}?${params}`)
      if (!response.ok) throw new Error('Failed to fetch posts')

      const data = await response.json()
      posts.value = data.posts
      return data
    } catch (err) {
      error.value = err.message
      // Don't re-throw, just set error state
    } finally {
      loading.value = false
    }
  }

  const getPostBySlug = async (slug) => {
    const response = await fetch(API_ENDPOINTS.blogPost(slug))
    if (!response.ok) throw new Error('Post not found')
    return await response.json()
  }

  const searchPosts = async (query) => {
    // Return empty results for empty query without calling API
    if (!query || query.trim() === '') {
      return { posts: [], total: 0 }
    }

    const response = await fetch(`${API_ENDPOINTS.blogSearch}?q=${encodeURIComponent(query)}`)
    if (!response.ok) throw new Error('Search failed')
    return await response.json()
  }

  return {
    posts,
    loading,
    error,
    fetchPosts,
    getPostBySlug,
    searchPosts
  }
}
