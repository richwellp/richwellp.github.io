import { ref, watch, onMounted, onUnmounted } from 'vue'

const theme = ref('auto')
const systemPreference = ref(getSystemPreference())
let mediaQueryList = null

/**
 * Detect the system's color scheme preference
 */
function getSystemPreference() {
  if (typeof window === 'undefined') return 'dark'
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  return mediaQuery.matches ? 'dark' : 'light'
}

/**
 * Get the effective theme to apply (resolves 'auto' to actual preference)
 */
function getEffectiveTheme(themeMode, systemPref) {
  if (themeMode === 'auto') {
    return systemPref
  }
  return themeMode
}

export function useTheme() {
  onMounted(() => {
    // Load saved preference from localStorage
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme && ['light', 'dark', 'auto'].includes(savedTheme)) {
      theme.value = savedTheme
    } else {
      theme.value = 'auto'
    }

    // Set up system preference listener
    if (typeof window !== 'undefined' && window.matchMedia) {
      mediaQueryList = window.matchMedia('(prefers-color-scheme: dark)')

      // Modern browsers
      if (mediaQueryList.addEventListener) {
        mediaQueryList.addEventListener('change', handleSystemPreferenceChange)
      } else if (mediaQueryList.addListener) {
        // Fallback for older browsers
        mediaQueryList.addListener(handleSystemPreferenceChange)
      }
    }

    // Apply initial theme
    applyTheme()
  })

  onUnmounted(() => {
    // Clean up listener
    if (mediaQueryList) {
      if (mediaQueryList.removeEventListener) {
        mediaQueryList.removeEventListener('change', handleSystemPreferenceChange)
      } else if (mediaQueryList.removeListener) {
        mediaQueryList.removeListener(handleSystemPreferenceChange)
      }
    }
  })

  const handleSystemPreferenceChange = (e) => {
    systemPreference.value = e.matches ? 'dark' : 'light'
    // Reapply theme if in auto mode
    if (theme.value === 'auto') {
      applyTheme()
    }
  }

  const applyTheme = () => {
    const effectiveTheme = getEffectiveTheme(theme.value, systemPreference.value)
    document.documentElement.setAttribute('data-theme', effectiveTheme)
  }

  const toggleTheme = () => {
    // Cycle through: light -> auto -> dark -> light
    const currentTheme = theme.value
    if (currentTheme === 'light') {
      theme.value = 'auto'
    } else if (currentTheme === 'auto') {
      theme.value = 'dark'
    } else {
      theme.value = 'light'
    }
    applyTheme()
    localStorage.setItem('theme', theme.value)
  }

  const setTheme = (newTheme) => {
    if (['light', 'dark', 'auto'].includes(newTheme)) {
      theme.value = newTheme
      applyTheme()
      localStorage.setItem('theme', newTheme)
    }
  }

  watch(theme, () => {
    applyTheme()
  })

  return {
    theme,
    systemPreference,
    toggleTheme,
    setTheme,
    getEffectiveTheme: () => getEffectiveTheme(theme.value, systemPreference.value)
  }
}
