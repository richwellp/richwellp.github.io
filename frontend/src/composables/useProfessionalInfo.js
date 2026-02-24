/**
 * Composable for loading professional information
 * Loads data from JSON file (dynamic, no rebuild needed)
 * Shared across components for consistency
 */
import { ref, computed } from 'vue'

// Shared state - loads once, used everywhere
const professionalInfo = ref(null)
const isLoading = ref(false)
const error = ref(null)

export function useProfessionalInfo() {
  const loadProfessionalInfo = async () => {
    // Only load once
    if (professionalInfo.value || isLoading.value) {
      return professionalInfo.value
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/data/professionalInfo.json')

      if (!response.ok) {
        throw new Error(`Failed to load professional info: ${response.status}`)
      }

      professionalInfo.value = await response.json()
      return professionalInfo.value
    } catch (err) {
      error.value = err.message
      console.error('Error loading professional info:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  // Computed getters for easy access
  const personal = computed(() => professionalInfo.value?.personal || {})
  const education = computed(() => professionalInfo.value?.education || [])
  const experience = computed(() => professionalInfo.value?.experience || [])
  const projects = computed(() => professionalInfo.value?.projects || [])
  const skills = computed(() => professionalInfo.value?.skills || {})

  return {
    // State
    professionalInfo,
    isLoading,
    error,

    // Actions
    loadProfessionalInfo,

    // Computed getters
    personal,
    education,
    experience,
    projects,
    skills
  }
}
