import { ref, watch, onMounted } from 'vue'

const theme = ref('dark')

export function useTheme() {
  onMounted(() => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      theme.value = savedTheme
    }
    applyTheme(theme.value)
  })

  const applyTheme = (newTheme) => {
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    applyTheme(theme.value)
    localStorage.setItem('theme', theme.value)
  }

  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  })

  return {
    theme,
    toggleTheme
  }
}
