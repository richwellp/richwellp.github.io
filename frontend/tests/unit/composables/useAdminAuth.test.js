import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { useAdminAuth } from '@/composables/useAdminAuth'

describe('useAdminAuth', () => {
  const STORAGE_KEY = 'admin_token'

  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    // Reset auth state before each test
    const { logout } = useAdminAuth()
    logout()
  })

  afterEach(() => {
    localStorage.clear()
  })

  describe('login', () => {
    it('sets authenticated state with valid key', () => {
      const { login, isAuthenticated } = useAdminAuth()

      expect(isAuthenticated.value).toBe(false)

      const result = login('test-admin-key')

      expect(result).toBe(true)
      expect(isAuthenticated.value).toBe(true)
    })

    it('trims whitespace from key', () => {
      const { login, getAuthHeaders } = useAdminAuth()

      login('  test-key  ')

      const headers = getAuthHeaders()
      expect(headers.Authorization).toBe('Bearer test-key')
    })

    it('rejects empty key', () => {
      const { login, isAuthenticated } = useAdminAuth()

      const result = login('')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })

    it('rejects whitespace-only key', () => {
      const { login, isAuthenticated } = useAdminAuth()

      const result = login('   ')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })

    it('rejects null key', () => {
      const { login, isAuthenticated } = useAdminAuth()

      const result = login(null)

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })
  })

  describe('logout', () => {
    it('clears authenticated state', () => {
      const { login, logout, isAuthenticated } = useAdminAuth()

      login('test-key')
      expect(isAuthenticated.value).toBe(true)

      logout()

      expect(isAuthenticated.value).toBe(false)
    })

    it('clears auth headers', () => {
      const { login, logout, getAuthHeaders } = useAdminAuth()

      login('test-key')
      logout()

      const headers = getAuthHeaders()
      expect(headers).toEqual({})
    })
  })

  describe('getAuthHeaders', () => {
    it('returns Authorization header when authenticated', () => {
      const { login, getAuthHeaders } = useAdminAuth()

      login('my-secret-key')

      const headers = getAuthHeaders()
      expect(headers).toHaveProperty('Authorization')
      expect(headers.Authorization).toBe('Bearer my-secret-key')
    })

    it('returns empty object when not authenticated', () => {
      const { getAuthHeaders } = useAdminAuth()

      const headers = getAuthHeaders()
      expect(headers).toEqual({})
    })
  })

  describe('shared state', () => {
    it('shares authentication state across instances', () => {
      const instance1 = useAdminAuth()
      const instance2 = useAdminAuth()

      expect(instance1.isAuthenticated.value).toBe(false)
      expect(instance2.isAuthenticated.value).toBe(false)

      instance1.login('test-key')

      // Both instances see the same state
      expect(instance1.isAuthenticated.value).toBe(true)
      expect(instance2.isAuthenticated.value).toBe(true)
    })

    it('shares auth headers across instances', () => {
      const instance1 = useAdminAuth()
      const instance2 = useAdminAuth()

      instance1.login('shared-key')

      const headers1 = instance1.getAuthHeaders()
      const headers2 = instance2.getAuthHeaders()

      expect(headers1.Authorization).toBe('Bearer shared-key')
      expect(headers2.Authorization).toBe('Bearer shared-key')
    })
  })

  describe('localStorage persistence', () => {
    it('persists token to localStorage on login', () => {
      const { login } = useAdminAuth()

      login('persisted-key')

      expect(localStorage.getItem(STORAGE_KEY)).toBe('persisted-key')
    })

    it('removes token from localStorage on logout', () => {
      const { login, logout } = useAdminAuth()

      login('test-key')
      expect(localStorage.getItem(STORAGE_KEY)).toBe('test-key')

      logout()
      expect(localStorage.getItem(STORAGE_KEY)).toBeNull()
    })

    it('persists token across instances (simulates page refresh)', () => {
      const instance1 = useAdminAuth()

      // Login with first instance
      instance1.login('persisted-key')
      expect(localStorage.getItem(STORAGE_KEY)).toBe('persisted-key')

      // Second instance should see the same token (simulating page refresh)
      const instance2 = useAdminAuth()
      expect(instance2.isAuthenticated.value).toBe(true)
      expect(instance2.adminToken.value).toBe('persisted-key')
    })

    it('handles localStorage write errors gracefully', () => {
      const setItemSpy = vi.spyOn(Storage.prototype, 'setItem')
        .mockImplementation(() => {
          throw new Error('Storage quota exceeded')
        })

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

      const { login, isAuthenticated } = useAdminAuth()
      const result = login('test-key')

      expect(result).toBe(true)
      expect(isAuthenticated.value).toBe(true)
      expect(consoleErrorSpy).toHaveBeenCalled()

      setItemSpy.mockRestore()
      consoleErrorSpy.mockRestore()
    })
  })
})
