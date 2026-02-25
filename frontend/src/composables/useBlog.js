import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'
import { useAsyncRequest } from './useAsyncRequest'

const posts = ref([])
const { loading, error, execute } = useAsyncRequest()

export function useBlog() {
  const fetchPosts = async (options = {}) => {
    await execute(async () => {
      const params = new URLSearchParams()
      if (options.page) params.set('page', options.page)
      if (options.per_page) params.set('per_page', options.per_page)
      if (options.tag) params.set('tag', options.tag)

      const response = await fetch(`${API_ENDPOINTS.blogPosts}?${params}`)
      if (!response.ok) throw new Error('Failed to fetch posts')

      const data = await response.json()
      posts.value = data.posts
      return data
    }).catch(() => {
      // Error already handled by useAsyncRequest
    })
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
