/**
 * Centralized API configuration
 */

// API Base URL - from environment variable or error
export const API_BASE_URL = import.meta.env.VITE_API_URL

if (!API_BASE_URL) {
  console.error('VITE_API_URL environment variable is not set. API calls will fail.')
}

// API Endpoints
export const API_ENDPOINTS = {
  // Chat endpoints
  chat: `${API_BASE_URL}/chat`,
  chatStream: `${API_BASE_URL}/chat/stream`,

  // Blog endpoints (public)
  blogPosts: `${API_BASE_URL}/blog/posts`,
  blogPost: (slug) => `${API_BASE_URL}/blog/posts/${slug}`,
  blogSearch: `${API_BASE_URL}/blog/search`,

  // Admin blog endpoints (require authentication)
  adminPosts: `${API_BASE_URL}/blog/admin/posts`,
  adminPost: (slug) => `${API_BASE_URL}/blog/admin/posts/${slug}`,
  adminCreatePost: `${API_BASE_URL}/blog/posts`,
  adminUpdatePost: (slug) => `${API_BASE_URL}/blog/posts/${slug}`,
  adminDeletePost: (slug) => `${API_BASE_URL}/blog/posts/${slug}`,

  // Albums endpoints (public)
  albums: `${API_BASE_URL}/albums`,
  album: (slug) => `${API_BASE_URL}/albums/${slug}`,

  // Admin albums endpoints (require authentication)
  adminAlbums: `${API_BASE_URL}/admin/albums`,
  adminAlbum: (slug) => `${API_BASE_URL}/admin/albums/${slug}`,
  adminAlbumPhotos: (slug) => `${API_BASE_URL}/admin/albums/${slug}/photos`,
  adminAlbumPhotosBatch: (slug) => `${API_BASE_URL}/admin/albums/${slug}/photos/batch`,
  adminPhoto: (photoId) => `${API_BASE_URL}/admin/photos/${photoId}`,
  adminPhotoReorder: (photoId) => `${API_BASE_URL}/admin/photos/${photoId}/reorder`,
}

// API Configuration
export const API_CONFIG = {
  messageLimit: 2000,  // Maximum message length
  historyLimit: 10,    // Maximum messages to send in history
}
