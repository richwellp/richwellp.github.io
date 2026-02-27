<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useTheme } from './composables/useTheme'
import { useProfessionalInfo } from './composables/useProfessionalInfo'
import { useBlog } from './composables/useBlog'
import { useChatAssistant } from './composables/useChatAssistant'
import { useSearch } from './composables/useSearch'
import ChatAssistant from './components/ChatAssistant.vue'
import CommandPalette from './components/CommandPalette.vue'

const mobileMenuOpen = ref(false)
const miscDropdownOpen = ref(false)
const { theme, toggleTheme } = useTheme()
const commandPaletteRef = ref(null)
const { searchQuery, searchResults, showSearchResults, isLoadingBlogContent, searchPages, clearSearch } = useSearch()
const { posts, fetchPosts } = useBlog()
const { loadProfessionalInfo } = useProfessionalInfo()
const { preloadContext } = useChatAssistant()

onMounted(async () => {
  fetchPosts()
  await loadProfessionalInfo()
  // Preload chatbot context in background (non-blocking)
  preloadContext().catch(err => console.warn('Failed to preload chat context:', err))
})

const openSearch = () => {
  commandPaletteRef.value?.openPalette()
}

const selectSearchResult = (path) => {
  clearSearch()
  closeMobileMenu()
}

const closeSearch = () => {
  showSearchResults.value = false
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  miscDropdownOpen.value = false
}

const toggleMiscDropdown = () => {
  miscDropdownOpen.value = !miscDropdownOpen.value
}

const closeMiscDropdown = () => {
  miscDropdownOpen.value = false
}
</script>

<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/" class="logo" @click="closeMobileMenu">
          Richwell Perez
        </RouterLink>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu" aria-label="Toggle menu">
          <span :class="{ open: mobileMenuOpen }"></span>
        </button>

        <!-- Navigation Links -->
        <div class="nav-links" :class="{ 'mobile-open': mobileMenuOpen }">
          <RouterLink to="/experience" @click="closeMobileMenu" active-class="active">
            Experience
          </RouterLink>
          <RouterLink to="/projects" @click="closeMobileMenu" active-class="active">
            Projects
          </RouterLink>
          <RouterLink to="/cv" @click="closeMobileMenu" active-class="active">
            CV
          </RouterLink>

          <RouterLink to="/contact" @click="closeMobileMenu" active-class="active">
            Contact
          </RouterLink>

          <!-- Misc Dropdown -->
          <div
            class="nav-dropdown"
            @mouseenter="miscDropdownOpen = true"
            @mouseleave="miscDropdownOpen = false"
          >
            <div class="dropdown-toggle-wrapper">
              <RouterLink
                to="/misc"
                @click="closeMobileMenu"
                active-class="active"
                class="dropdown-link"
              >
                Misc
              </RouterLink>
              <button
                class="dropdown-arrow-btn"
                @click="toggleMiscDropdown"
                :class="{ 'active': miscDropdownOpen }"
                aria-label="Toggle Misc menu"
              >
                <span class="dropdown-arrow" :class="{ 'open': miscDropdownOpen }">▼</span>
              </button>
            </div>
            <div class="dropdown-menu" :class="{ 'show': miscDropdownOpen }">
              <RouterLink to="/misc/blog" @click="closeMobileMenu" class="dropdown-item">
                Blog
              </RouterLink>
              <RouterLink to="/misc/albums" @click="closeMobileMenu" class="dropdown-item">
                Albums
              </RouterLink>
            </div>
          </div>

          <!-- Search Bar -->
          <div class="search-container">
            <div class="search-bar">
              <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <input
                id="mobile-search"
                type="text"
                class="search-input"
                v-model="searchQuery"
                @input="searchPages"
                @focus="searchPages"
                @blur="() => setTimeout(closeSearch, 200)"
                placeholder="Search"
                aria-label="Search pages"
              />
            </div>
            <!-- Search Results Dropdown -->
            <div v-if="showSearchResults" class="search-results">
              <!-- Loading indicator for blog content -->
              <div v-if="isLoadingBlogContent" class="results-header">
                <span>Loading blog content...</span>
              </div>

              <div v-if="searchResults.length > 0" class="results-header">
                Found {{ searchResults.length }} result{{ searchResults.length === 1 ? '' : 's' }}
              </div>
              <router-link
                v-for="result in searchResults"
                :key="result.path + result.title"
                :to="result.path"
                class="search-result-item"
                @click="selectSearchResult(result.path)"
              >
                <span class="result-icon">{{ result.icon }}</span>
                <div class="result-content">
                  <div class="result-title">{{ result.title }}</div>
                  <div v-if="result.subtitle" class="result-subtitle">{{ result.subtitle }}</div>
                </div>
              </router-link>
              <div v-if="searchResults.length === 0 && searchQuery.length > 0 && !isLoadingBlogContent" class="no-results">
                <span>No results found for "{{ searchQuery }}"</span>
              </div>
            </div>
          </div>

          <!-- Theme Toggle -->
          <button @click="toggleTheme" class="theme-toggle" :aria-label="`Theme: ${theme.charAt(0).toUpperCase() + theme.slice(1)}`">
            <div class="toggle-track">
              <span class="toggle-icon sun">☀️</span>
              <span class="toggle-icon moon">🌙</span>
              <div class="toggle-slider" :class="{ 'light-mode': theme === 'light', 'dark-mode': theme === 'dark' }"></div>
            </div>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>Let's Connect!</h4>
          <div class="social-links">
            <a href="mailto:richwell.perez@gmail.com" target="_blank" rel="noopener" class="social-link">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              Email
            </a>
            <a
              href="https://www.linkedin.com/in/richwell-perez"
              target="_blank"
              rel="noopener noreferrer"
              class="social-link"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
              LinkedIn
            </a>
          </div>
        </div>
        <div class="footer-section">
          <p class="copyright">© 2026 Richwell Perez. Built with Vue.js.</p>
        </div>
      </div>
    </footer>

    <!-- Chat Assistant -->
    <ChatAssistant />

    <!-- Command Palette -->
    <CommandPalette ref="commandPaletteRef" />
  </div>
</template>

<style>
/* Import distinctive fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap');

/* Warm Editorial Theme Variables */
:root[data-theme='dark'] {
  --bg-primary: #0f1419;
  --bg-secondary: #1a1f26;
  --bg-tertiary: #252b33;
  --bg-card: #1a1f26;
  --bg-hover: #252b33;
  --text-primary: #e8e6e3;
  --text-secondary: #a8a29e;
  --text-tertiary: #78716c;
  --border-color: #38332d;
  --accent-primary: #c86c4a;
  --accent-hover: #d4825f;
  --accent-secondary: #d4a574;
  --accent-tertiary: #2d5f5f;
  --link-color: #d4a574;
  --link-hover: #e8b887;
  --shadow: rgba(0, 0, 0, 0.4);
  --gradient-subtle: linear-gradient(135deg, rgba(200, 108, 74, 0.08) 0%, rgba(212, 165, 116, 0.08) 100%);
}

:root[data-theme='light'] {
  --bg-primary: #fafaf9;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f5f5f4;
  --bg-card: #ffffff;
  --bg-hover: #f5f5f4;
  --text-primary: #1c1917;
  --text-secondary: #57534e;
  --text-tertiary: #78716c;
  --border-color: #e7e5e4;
  --accent-primary: #b85a42;
  --accent-hover: #c96d54;
  --accent-secondary: #6b7b5e;
  --accent-tertiary: #3d6b6b;
  --link-color: #9d5d48;
  --link-hover: #b85a42;
  --shadow: rgba(0, 0, 0, 0.08);
  --gradient-subtle: linear-gradient(135deg, rgba(184, 90, 66, 0.06) 0%, rgba(107, 123, 94, 0.06) 100%);
}

/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--text-primary);
  line-height: 1.65;
  letter-spacing: -0.011em;
  font-weight: 400;
  background: var(--bg-primary);
  transition: background-color 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              color 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Subtle texture overlay for depth */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='4.2' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.028;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: overlay;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Playfair Display', Georgia, serif;
  font-weight: 600;
  letter-spacing: -0.025em;
  line-height: 1.2;
  color: var(--text-primary);
}

h1 {
  font-size: clamp(2.25rem, 5vw, 3.75rem);
  font-weight: 700;
}

h2 {
  font-size: clamp(1.875rem, 4vw, 2.75rem);
}

h3 {
  font-size: clamp(1.5rem, 3vw, 2rem);
}

/* Improved link styling */
a {
  color: var(--link-color);
  text-decoration: underline;
  text-decoration-color: transparent;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 3px;
  transition: text-decoration-color 0.25s ease, color 0.25s ease;
}

a:hover {
  color: var(--link-hover);
  text-decoration-color: currentColor;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Navigation */
.navbar {
  background: var(--bg-card)f5;
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  box-shadow: 0 1px 0 var(--border-color)60;
  border-bottom: 1px solid var(--border-color)80;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.navbar::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-subtle);
  opacity: 0.6;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.375rem;
  font-weight: 700;
  font-style: italic;
  color: var(--text-primary);
  text-decoration: none;
  letter-spacing: -0.02em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.logo::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo:hover {
  color: var(--accent-primary);
  transform: translateY(-1px);
}

.logo:hover::after {
  width: 100%;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 25px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 101;
}

.mobile-menu-btn span,
.mobile-menu-btn span::before,
.mobile-menu-btn span::after {
  display: block;
  width: 30px;
  height: 3px;
  background: var(--text-primary);
  transition: all 0.3s ease;
}

.mobile-menu-btn span::before,
.mobile-menu-btn span::after {
  content: '';
  position: absolute;
}

.mobile-menu-btn span::before {
  transform: translateY(-10px);
}

.mobile-menu-btn span::after {
  transform: translateY(10px);
}

.mobile-menu-btn span.open {
  background: transparent;
}

.mobile-menu-btn span.open::before {
  transform: rotate(45deg);
}

.mobile-menu-btn span.open::after {
  transform: rotate(-45deg);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9375rem;
  letter-spacing: -0.01em;
  padding: 0.625rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--accent-primary);
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-links a:hover {
  color: var(--text-primary);
}

.nav-links a:hover::after {
  width: 100%;
}

.nav-links a.active {
  color: var(--text-primary);
  font-weight: 600;
}

.nav-links a.active::after {
  width: 100%;
}

/* Dropdown Navigation */
.nav-dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.dropdown-toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.dropdown-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.dropdown-link:hover {
  color: var(--text-primary);
}

.dropdown-link.active {
  color: var(--text-primary);
  border-bottom-color: var(--accent-primary);
}

.dropdown-arrow-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.5rem 0.25rem 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  height: 100%;
}

.dropdown-arrow-btn:hover {
  color: var(--text-primary);
}

.dropdown-arrow-btn.active {
  color: var(--text-primary);
}

.dropdown-arrow {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
  display: inline-block;
}

.dropdown-arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 0.625rem;
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12),
              0 4px 8px rgba(0, 0, 0, 0.06);
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-12px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  padding: 0.375rem;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9375rem;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  border-radius: 7px;
  position: relative;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: var(--accent-primary);
  border-radius: 0 2px 2px 0;
  transition: height 0.25s ease;
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
  padding-left: 1.25rem;
}

.dropdown-item:hover::before {
  height: 60%;
}

.dropdown-item.router-link-active {
  background: var(--bg-hover);
  color: var(--accent-primary);
  font-weight: 600;
  padding-left: 1.25rem;
}

.dropdown-item.router-link-active::before {
  height: 60%;
}

.item-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

/* Search Container */
.search-container {
  position: relative;
}

/* Search Bar */
.search-bar {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5625rem 0.875rem;
  background: var(--bg-primary);
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: 220px;
}

.search-bar:focus-within {
  border-color: var(--accent-primary);
  background: var(--bg-tertiary);
  box-shadow: 0 0 0 3px var(--accent-primary)15,
              0 2px 8px rgba(0, 0, 0, 0.06);
  transform: translateY(-1px);
}

.search-icon {
  color: var(--text-tertiary);
  flex-shrink: 0;
  width: 18px;
  height: 18px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.875rem;
  font-family: inherit;
  min-width: 0;
  padding: 0;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

/* Search Results Dropdown */
.search-results {
  position: absolute;
  top: calc(100% + 0.625rem);
  left: 0;
  right: 0;
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12),
              0 4px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  overflow-y: auto;
  max-height: 420px;
  z-index: 1000;
  min-width: 280px;
  animation: dropdownFadeIn 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-results::-webkit-scrollbar {
  width: 6px;
}

.search-results::-webkit-scrollbar-track {
  background: transparent;
}

.search-results::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
}

.search-result-item {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  padding: 1rem 1.125rem;
  color: var(--text-primary);
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border-bottom: 1px solid var(--border-color)50;
  position: relative;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--accent-primary);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.search-result-item:hover {
  background: var(--bg-hover);
  padding-left: 1.375rem;
}

.search-result-item:hover::before {
  opacity: 1;
}

.result-icon {
  font-size: 1.3rem;
  flex-shrink: 0;
  line-height: 1;
  margin-top: 0.2rem;
}

.result-title {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.25rem;
  color: var(--text-primary);
}

.result-subtitle {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-top: 0.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.results-header {
  padding: 0.625rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 1;
}

.no-results {
  padding: 1.5rem;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

/* Theme Toggle Button */
.theme-toggle {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: transform 0.2s ease;
}

.theme-toggle:active {
  transform: scale(0.96);
}

.toggle-track {
  position: relative;
  width: 68px;
  height: 34px;
  background: var(--bg-hover);
  border: 1.5px solid var(--border-color);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 7px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

.theme-toggle:hover .toggle-track {
  border-color: var(--accent-primary);
  background: var(--bg-tertiary);
}

.toggle-icon {
  font-size: 0.875rem;
  z-index: 1;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.35;
  filter: grayscale(1);
}

/* Highlight active icon based on theme */
:root[data-theme='light'] .toggle-icon.sun {
  opacity: 1;
  transform: scale(1.15);
  filter: grayscale(0);
}

:root[data-theme='dark'] .toggle-icon.moon {
  opacity: 1;
  transform: scale(1.15);
  filter: grayscale(0);
}

.toggle-slider {
  position: absolute;
  left: 4px;
  width: 26px;
  height: 26px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  border-radius: 50%;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15),
              0 1px 2px rgba(0, 0, 0, 0.1);
}

.toggle-slider.light-mode {
  transform: translateX(0);
}

.toggle-slider.dark-mode {
  transform: translateX(30px);
}

.theme-toggle:hover .toggle-slider {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2),
              0 2px 4px rgba(0, 0, 0, 0.12);
}

/* Footer */
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 3rem 2rem 2.5rem;
  margin-top: 0;
  transition: background-color 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-subtle);
  opacity: 0.8;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.footer-section h4 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.social-links {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.social-links a {
  color: var(--link-color);
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.social-links a svg {
  flex-shrink: 0;
}

.social-links a:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.copyright {
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .mobile-menu-btn {
    display: flex;
    position: relative;
  }

  .nav-links {
    position: fixed;
    top: 0;
    right: -100%;
    height: 100vh;
    width: 70%;
    max-width: 300px;
    background: var(--bg-card);
    flex-direction: column;
    padding: 5rem 2rem 2rem;
    box-shadow: -2px 0 10px var(--shadow);
    border-left: 1px solid var(--border-color);
    transition: right 0.3s ease;
    gap: 1.5rem;
    align-items: flex-start;
  }

  .nav-links.mobile-open {
    right: 0;
  }

  .nav-links a {
    font-size: 1.2rem;
    width: 100%;
    padding: 0.75rem 0;
  }

  /* Mobile Dropdown Styles */
  .nav-dropdown {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }

  .dropdown-toggle-wrapper {
    width: 100%;
    justify-content: space-between;
  }

  .dropdown-link {
    flex: 1;
    font-size: 1.2rem;
    padding: 0.75rem 0;
  }

  .dropdown-arrow-btn {
    font-size: 1.2rem;
    padding: 0.75rem 0.5rem;
  }

  .dropdown-menu {
    position: static;
    width: 100%;
    margin-top: 0;
    margin-left: 1rem;
    box-shadow: none;
    border: none;
    border-left: 2px solid var(--border-color);
    border-radius: 0;
    background: transparent;
    opacity: 1;
    visibility: visible;
    transform: none;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }

  .dropdown-menu.show {
    max-height: 500px;
  }

  .dropdown-item {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }

  .dropdown-item:first-child,
  .dropdown-item:last-child {
    border-radius: 0;
  }

  .search-container {
    width: 100%;
    margin: 0.5rem 0;
  }

  .search-bar {
    width: 100%;
  }

  .search-results {
    position: static;
    min-width: auto;
    margin-top: 0.5rem;
    border-radius: 6px;
    max-height: 300px;
  }

  .result-subtitle {
    -webkit-line-clamp: 2;
    font-size: 0.75rem;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .social-links {
    justify-content: center;
  }
}
</style>
