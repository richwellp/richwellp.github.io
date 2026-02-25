import { describe, it, expect, vi } from 'vitest'
import { useAsyncRequest } from '../../../src/composables/useAsyncRequest'

describe('useAsyncRequest', () => {
  it('should start with loading false and no error', () => {
    const { loading, error } = useAsyncRequest()

    expect(loading.value).toBe(false)
    expect(error.value).toBe(null)
  })

  it('should set loading to true during execution', async () => {
    const { loading, execute } = useAsyncRequest()
    const asyncFn = vi.fn(() => new Promise(resolve => setTimeout(resolve, 100)))

    const promise = execute(asyncFn)
    expect(loading.value).toBe(true)

    await promise
    expect(loading.value).toBe(false)
  })

  it('should clear error on new execution', async () => {
    const { error, execute } = useAsyncRequest()

    // First call fails
    await execute(() => Promise.reject(new Error('First error'))).catch(() => {})
    expect(error.value).toBe('First error')

    // Second call succeeds - should clear error
    await execute(() => Promise.resolve('success'))
    expect(error.value).toBe(null)
  })

  it('should capture and set error on failure', async () => {
    const { error, execute } = useAsyncRequest()

    await execute(() => Promise.reject(new Error('Test error'))).catch(() => {})

    expect(error.value).toBe('Test error')
  })

  it('should return result from async function', async () => {
    const { execute } = useAsyncRequest()
    const result = await execute(() => Promise.resolve('success'))

    expect(result).toBe('success')
  })

  it('should set loading to false even if execution throws', async () => {
    const { loading, execute } = useAsyncRequest()

    await execute(() => Promise.reject(new Error('Fail'))).catch(() => {})

    expect(loading.value).toBe(false)
  })
})
