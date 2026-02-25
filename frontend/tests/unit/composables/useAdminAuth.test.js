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
            method: 'bearer'
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
            method: null
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
          headers: expect.objectContaining({
            'Authorization': expect.stringContaining('Bearer'),
            'Content-Type': 'application/json'
          }),
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

      logout()
      expect(isAuthenticated.value).toBe(false)
    })

    it('clears token from localStorage', async () => {
      const { login, logout } = useAdminAuth()

      await login('test-key')
      expect(localStorage.getItem('admin_token')).toBeTruthy()

      logout()
      expect(localStorage.getItem('admin_token')).toBeNull()
    })
  })

  describe('getAuthFetchOptions', () => {
    it('returns fetch options with Authorization header', () => {
      const { getAuthFetchOptions } = useAdminAuth()

      const options = getAuthFetchOptions('GET')

      expect(options).toEqual({
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
    })

    it('includes Authorization header when token exists', async () => {
      const { login, getAuthFetchOptions } = useAdminAuth()

      await login('test-key')
      const options = getAuthFetchOptions('GET')

      expect(options.headers['Authorization']).toBe('Bearer test-key')
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

    it('shares token across instances', async () => {
      const instance1 = useAdminAuth()
      const instance2 = useAdminAuth()

      await instance1.login('test-key')

      const headers1 = instance1.getAuthHeaders()
      const headers2 = instance2.getAuthHeaders()

      expect(headers1['Authorization']).toBe('Bearer test-key')
      expect(headers2['Authorization']).toBe('Bearer test-key')
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

    it('clears error on successful login', async () => {
      const { login, authError } = useAdminAuth()

      // First login fails
      fetchMock.mockRejectedValueOnce(new Error('Network error'))
      await login('wrong-key')
      expect(authError.value).toBeTruthy()

      // Second login succeeds
      const result = await login('test-key')
      expect(result).toBe(true)
      expect(authError.value).toBeNull()
    })
  })
})
