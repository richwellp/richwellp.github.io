import { ref } from 'vue'

/**
 * Reusable composable for handling async operations with loading/error states
 * Eliminates duplicated try/catch/finally patterns across composables
 */
export function useAsyncRequest() {
  const loading = ref(false)
  const error = ref(null)

  /**
   * Execute an async function with automatic loading and error handling
   * @param {Function} fn - Async function to execute
   * @returns {Promise} Result from the async function
   */
  const execute = async (fn) => {
    loading.value = true
    error.value = null

    try {
      const result = await fn()
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return { loading, error, execute }
}
