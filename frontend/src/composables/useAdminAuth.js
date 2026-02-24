import { ref, computed } from 'vue'

const STORAGE_KEY = 'admin_token'

// Load token from localStorage on module initialization
const loadToken = () => {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch (e) {
    console.error('Failed to load admin token:', e)
    return null
  }
}

// Save token to localStorage
const saveToken = (token) => {
  try {
    if (token) {
      localStorage.setItem(STORAGE_KEY, token)
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  } catch (e) {
    console.error('Failed to save admin token:', e)
  }
}

// Shared state across all instances
const adminToken = ref(loadToken())
const isAuthenticated = computed(() => !!adminToken.value)

export function useAdminAuth() {
  const login = (key) => {
    if (!key || key.trim() === '') {
      return false
    }

    const trimmedKey = key.trim()
    adminToken.value = trimmedKey
    saveToken(trimmedKey)
    return true
  }

  const logout = () => {
    adminToken.value = null
    saveToken(null)
  }

  const getAuthHeaders = () => {
    if (!adminToken.value) {
      return {}
    }

    return {
      'Authorization': `Bearer ${adminToken.value}`
    }
  }

  return {
    adminToken,
    isAuthenticated,
    login,
    logout,
    getAuthHeaders
  }
}
