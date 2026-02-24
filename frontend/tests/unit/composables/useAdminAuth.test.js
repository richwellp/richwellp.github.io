import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { useAdminAuth } from '@/composables/useAdminAuth'

describe('useAdminAuth', () => {
  let fetchMock

  beforeEach(() => {
    // Mock fetch for authentication endpoints
    fetchMock = vi.spyOn(global, 'fetch').mockImplementation((url) => {
      if (url.includes('/auth/login')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            message: 'Login successful',
            authenticated: true,
            method: 'cookie'
          })
        })
      }
      if (url.includes('/auth/logout')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            message: 'Logged out successfully',
            authenticated: false
          })
        })
      }
      if (url.includes('/auth/status')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            authenticated: false,
            method: null,
            expires_in: null
          })
        })
      }
      return Promise.reject(new Error('Unknown endpoint'))
    })

    // Reset auth state
    const { logout } = useAdminAuth()
    logout()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('login', () => {
    it('sets authenticated state with valid key', async () => {
      const { login, isAuthenticated } = useAdminAuth()

      expect(isAuthenticated.value).toBe(false)

      const result = await login('test-admin-key')

      expect(result).toBe(true)
      expect(isAuthenticated.value).toBe(true)
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({
          method: 'POST',
          credentials: 'include',
          body: JSON.stringify({ key: 'test-admin-key' })
        })
      )
    })

    it('trims whitespace from key', async () => {
      const { login } = useAdminAuth()

      await login('  test-key  ')

      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({
          body: JSON.stringify({ key: 'test-key' })
        })
      )
    })

    it('rejects empty key', async () => {
      const { login, isAuthenticated, authError } = useAdminAuth()

      const result = await login('')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
      expect(authError.value).toBeTruthy()
    })

    it('rejects whitespace-only key', async () => {
      const { login, isAuthenticated } = useAdminAuth()

      const result = await login('   ')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })

    it('rejects null key', async () => {
      const { login, isAuthenticated } = useAdminAuth()

      const result = await login(null)

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })

    it('handles invalid key from server', async () => {
      const { login, isAuthenticated } = useAdminAuth()

      fetchMock.mockImplementationOnce(() =>
        Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ error: 'Invalid admin key' })
        })
      )

      const result = await login('wrong-key')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
    })
  })

  describe('logout', () => {
    it('clears authenticated state', async () => {
      const { login, logout, isAuthenticated } = useAdminAuth()

      await login('test-key')
      expect(isAuthenticated.value).toBe(true)

      await logout()
      expect(isAuthenticated.value).toBe(false)
    })

    it('sends logout request to server', async () => {
      const { login, logout } = useAdminAuth()

      await login('test-key')
      await logout()

      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/auth/logout'),
        expect.objectContaining({
          method: 'POST',
          credentials: 'include'
        })
      )
    })
  })

  describe('getAuthFetchOptions', () => {
    it('returns fetch options with credentials included', () => {
      const { getAuthFetchOptions } = useAdminAuth()

      const options = getAuthFetchOptions('GET')

      expect(options).toEqual({
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      })
    })

    it('includes body when provided', () => {
      const { getAuthFetchOptions } = useAdminAuth()

      const data = { title: 'Test' }
      const options = getAuthFetchOptions('POST', data)

      expect(options.body).toBe(JSON.stringify(data))
    })
  })

  describe('shared state', () => {
    it('shares authentication state across instances', async () => {
      const instance1 = useAdminAuth()
      const instance2 = useAdminAuth()

      await instance1.login('test-key')

      // Both instances see the same state
      expect(instance1.isAuthenticated.value).toBe(true)
      expect(instance2.isAuthenticated.value).toBe(true)
    })

    it('shares auth method across instances', async () => {
      const instance1 = useAdminAuth()
      const instance2 = useAdminAuth()

      await instance1.login('test-key')

      expect(instance1.authMethod.value).toBe('cookie')
      expect(instance2.authMethod.value).toBe('cookie')
    })
  })

  describe('error handling', () => {
    it('handles network errors during login', async () => {
      const { login, isAuthenticated, authError } = useAdminAuth()

      fetchMock.mockRejectedValueOnce(new Error('Network error'))

      const result = await login('test-key')

      expect(result).toBe(false)
      expect(isAuthenticated.value).toBe(false)
      expect(authError.value).toContain('Network error')
    })

    it('handles network errors during logout', async () => {
      const { login, logout, isAuthenticated } = useAdminAuth()

      await login('test-key')
      expect(isAuthenticated.value).toBe(true)

      fetchMock.mockRejectedValueOnce(new Error('Network error'))

      await logout()

      // Still clears local state even if request fails
      expect(isAuthenticated.value).toBe(false)
    })
  })
})
