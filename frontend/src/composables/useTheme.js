import { ref, watch, onMounted } from 'vue'

const theme = ref('dark')

/**
 * Detect the system's color scheme preference
 */
function getSystemPreference() {
  if (typeof window === 'undefined') return 'dark'
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  return mediaQuery.matches ? 'dark' : 'light'
}

export function useTheme() {
  onMounted(() => {
    // Load saved preference from localStorage, or use system preference on first visit
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme && ['light', 'dark'].includes(savedTheme)) {
      theme.value = savedTheme
    } else {
      // First visit - detect system preference
      theme.value = getSystemPreference()
    }

    // Apply initial theme
    applyTheme()
  })

  const applyTheme = () => {
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  const toggleTheme = () => {
    // Simple toggle: light <-> dark
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    applyTheme()
    localStorage.setItem('theme', theme.value)
  }

  const setTheme = (newTheme) => {
    if (['light', 'dark'].includes(newTheme)) {
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
    toggleTheme,
    setTheme
  }
}
