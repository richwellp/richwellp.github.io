/**
 * useAdminAuth - Admin authentication with Bearer tokens
 * Uses localStorage to store admin key and sends as Authorization header
 */
import { ref } from 'vue'
import { API_ENDPOINTS } from '../config/api'

const TOKEN_KEY = 'admin_token'

// Shared authentication state
const isAuthenticated = ref(!!localStorage.getItem(TOKEN_KEY))
const isLoading = ref(false)
const authError = ref(null)

/**
 * Get stored token from localStorage
 */
function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Store token in localStorage
 */
function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
  isAuthenticated.value = true
}

/**
 * Remove token from localStorage
 */
function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
  isAuthenticated.value = false
}

/**
 * Login with admin key
 * Stores key in localStorage for subsequent requests
 */
async function login(key) {
  if (!key || key.trim() === '') {
    authError.value = 'Admin key is required'
    return false
  }

  isLoading.value = true
  authError.value = null

  try {
    // Verify the key works by calling a test endpoint
    const response = await fetch(API_ENDPOINTS.authLogin, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key.trim()}`
      },
      body: JSON.stringify({ key: key.trim() })
    })

    if (response.ok) {
      // Store the admin key for future requests
      setToken(key.trim())
      return true
    } else {
      const errorData = await response.json()
      authError.value = errorData.error || 'Invalid admin key'
      clearToken()
      return false
    }
  } catch (error) {
    console.error('Login failed:', error)
    authError.value = 'Network error during login'
    clearToken()
    return false
  } finally {
    isLoading.value = false
  }
}

/**
 * Logout and clear stored token
 */
function logout() {
  clearToken()
  authError.value = null
}

/**
 * Check if user is authenticated
 */
function checkAuthStatus() {
  const token = getToken()
  isAuthenticated.value = !!token
  return isAuthenticated.value
}

/**
 * Get headers for authenticated API requests
 * Includes Authorization Bearer token
 */
function getAuthHeaders() {
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json'
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return headers
}

/**
 * Get fetch options for authenticated requests
 */
function getAuthFetchOptions(method = 'GET', body = null) {
  const options = {
    method,
    headers: getAuthHeaders()
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  return options
}

/**
 * Composable for admin authentication
 */
export function useAdminAuth() {
  return {
    isAuthenticated,
    isLoading,
    authError,
    login,
    logout,
    checkAuthStatus,
    getAuthHeaders,
    getAuthFetchOptions
  }
}
