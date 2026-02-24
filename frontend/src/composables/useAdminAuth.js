/**
 * useAdminAuth - Admin authentication with secure httpOnly cookies
 * Uses server-side session cookies instead of localStorage for better security
 */
import { ref, computed } from 'vue'
import { API_ENDPOINTS } from '../config/api'

// Shared authentication state
const isAuthenticated = ref(false)
const authMethod = ref(null) // 'cookie' or 'bearer'
const isLoading = ref(false)
const authError = ref(null)

/**
 * Check authentication status from server
 */
async function checkAuthStatus() {
  isLoading.value = true
  authError.value = null

  try {
    const response = await fetch(API_ENDPOINTS.authStatus, {
      method: 'GET',
      credentials: 'include', // Include cookies in request
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      isAuthenticated.value = data.authenticated
      authMethod.value = data.method
      return data.authenticated
    } else {
      isAuthenticated.value = false
      authMethod.value = null
      return false
    }
  } catch (error) {
    console.error('Failed to check auth status:', error)
    authError.value = error.message
    isAuthenticated.value = false
    authMethod.value = null
    return false
  } finally {
    isLoading.value = false
  }
}

/**
 * Login with admin key
 * Sets httpOnly secure cookie on success
 */
async function login(key) {
  if (!key || key.trim() === '') {
    authError.value = 'Admin key is required'
    return false
  }

  isLoading.value = true
  authError.value = null

  try {
    const response = await fetch(API_ENDPOINTS.authLogin, {
      method: 'POST',
      credentials: 'include', // Include cookies in request
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key: key.trim() })
    })

    if (response.ok) {
      const data = await response.json()
      isAuthenticated.value = true
      authMethod.value = data.method || 'cookie'
      return true
    } else {
      const errorData = await response.json()
      authError.value = errorData.error || 'Login failed'
      isAuthenticated.value = false
      return false
    }
  } catch (error) {
    console.error('Login failed:', error)
    authError.value = 'Network error during login'
    isAuthenticated.value = false
    return false
  } finally {
    isLoading.value = false
  }
}

/**
 * Logout and clear session cookie
 */
async function logout() {
  isLoading.value = true
  authError.value = null

  try {
    const response = await fetch(API_ENDPOINTS.authLogout, {
      method: 'POST',
      credentials: 'include', // Include cookies in request
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      isAuthenticated.value = false
      authMethod.value = null
      return true
    } else {
      // Even if logout fails, clear local state
      isAuthenticated.value = false
      authMethod.value = null
      return false
    }
  } catch (error) {
    console.error('Logout failed:', error)
    authError.value = 'Network error during logout'
    // Clear local state even on error
    isAuthenticated.value = false
    authMethod.value = null
    return false
  } finally {
    isLoading.value = false
  }
}

/**
 * Get headers for authenticated API requests
 * No Authorization header needed - cookies are sent automatically
 */
function getAuthHeaders() {
  // With httpOnly cookies, no headers needed
  // Cookies are automatically included with credentials: 'include'
  return {
    'Content-Type': 'application/json'
  }
}

/**
 * Get fetch options for authenticated requests
 */
function getAuthFetchOptions(method = 'GET', body = null) {
  const options = {
    method,
    credentials: 'include', // Critical: include cookies
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
  // Check auth status on first use
  if (isAuthenticated.value === null) {
    checkAuthStatus()
  }

  return {
    isAuthenticated,
    authMethod,
    isLoading,
    authError,
    login,
    logout,
    checkAuthStatus,
    getAuthHeaders,
    getAuthFetchOptions
  }
}
