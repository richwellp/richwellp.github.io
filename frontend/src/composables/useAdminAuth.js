import { ref } from 'vue'

// Shared state across all instances
const adminKey = ref(null)
const isAuthenticated = ref(false)

export function useAdminAuth() {
  const login = (key) => {
    if (!key || key.trim() === '') {
      return false
    }

    adminKey.value = key.trim()
    isAuthenticated.value = true
    return true
  }

  const logout = () => {
    adminKey.value = null
    isAuthenticated.value = false
  }

  const getAuthHeaders = () => {
    if (!adminKey.value) {
      return {}
    }

    return {
      'Authorization': `Bearer ${adminKey.value}`
    }
  }

  return {
    isAuthenticated,
    login,
    logout,
    getAuthHeaders
  }
}
