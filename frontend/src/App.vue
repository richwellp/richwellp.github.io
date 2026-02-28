<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useTheme } from './composables/useTheme'
import { useProfessionalInfo } from './composables/useProfessionalInfo'
import { CONTACT } from './config/contact'
import { useBlog } from './composables/useBlog'
import { useChatAssistant } from './composables/useChatAssistant'
import { useSearch } from './composables/useSearch'
import ChatAssistant from './components/ChatAssistant.vue'

const mobileMenuOpen = ref(false)
const miscDropdownOpen = ref(false)
const { theme, toggleTheme } = useTheme()
const { searchQuery, searchResults, showSearchResults, isLoadingBlogContent, searchPages, clearSearch } = useSearch()
const { fetchPosts } = useBlog()
const { personal, content, loadProfessionalInfo } = useProfessionalInfo()
const { preloadContext } = useChatAssistant()

onMounted(async () => {
  fetchPosts()
  await loadProfessionalInfo()
  // Preload chatbot context in background (non-blocking)
  preloadContext().catch(err => console.warn('Failed to preload chat context:', err))
})

const selectSearchResult = () => {
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

</script>

<template>
  <div id="app">
    <!-- Mobile menu backdrop -->
    <Transition name="overlay">
      <div
        v-if="mobileMenuOpen"
        class="mobile-overlay"
        @click="closeMobileMenu"
        aria-hidden="true"
      ></div>
    </Transition>

    <!-- Navigation -->
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/" class="logo" @click="closeMobileMenu">
          {{ personal.name || 'Richwell Perez' }}
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
                <svg
                  class="dropdown-arrow"
                  :class="{ 'open': miscDropdownOpen }"
                  viewBox="0 0 24 24"
                  width="10"
                  height="10"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
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
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-inner">

        <!-- Brand + status -->
        <div class="footer-brand">
          <RouterLink to="/" class="footer-name">{{ personal.name || 'Richwell Perez' }}</RouterLink>
          <span class="footer-status">
            <span class="footer-dot"></span>
            {{ content.availabilityLabel }}
          </span>
        </div>

        <!-- Nav quick-links -->
        <nav class="footer-nav">
          <RouterLink to="/experience">Experience</RouterLink>
          <RouterLink to="/projects">Projects</RouterLink>
          <RouterLink to="/cv">CV</RouterLink>
          <RouterLink to="/contact">Contact</RouterLink>
        </nav>

        <!-- Social + copyright -->
        <div class="footer-social">
          <div class="footer-links">
            <a :href="`mailto:${CONTACT.email}`" aria-label="Email">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </a>
            <a :href="CONTACT.github" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a :href="CONTACT.linkedin" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
          <p class="copyright">© 2026 {{ personal.name || 'Richwell Perez' }}</p>
        </div>

      </div>
    </footer>

    <!-- Chat Assistant -->
    <ChatAssistant />

  </div>
</template>

<style>
/* Urbanist (display headings) · Nunito (body) · JetBrains Mono (labels) */
@import url('https://fonts.googleapis.com/css2?family=Urbanist:ital,wght@0,300..900;1,300..900&family=Nunito:ital,wght@0,300..800;1,300..800&family=JetBrains+Mono:ital,wght@0,400..700;1,400..700&display=swap');

/* Midnight Depth — void-black / soft indigo / violet */
:root[data-theme='dark'] {
  --bg-primary: #05060f;
  --bg-secondary: #090b1a;
  --bg-tertiary: #0f1228;
  --bg-card: #090b1a;
  --bg-hover: #0f1228;
  --text-primary: #e2e8f0;
  --text-secondary: #8896b3;
  --text-tertiary: #4d5a7a;
  --border-color: #1a2040;
  --accent-primary: #818cf8;
  --accent-hover: #a5b0ff;
  --accent-secondary: #a78bfa;
  --accent-tertiary: #0d1030;
  --link-color: #818cf8;
  --link-hover: #a5b0ff;
  --shadow: rgba(0, 0, 0, 0.7);
  --gradient-subtle: linear-gradient(135deg, rgba(129, 140, 248, 0.1) 0%, rgba(167, 139, 250, 0.05) 100%);
}

:root[data-theme='light'] {
  --bg-primary: #f2f3fa;
  --bg-secondary: #ffffff;
  --bg-tertiary: #e4e6f5;
  --bg-card: #ffffff;
  --bg-hover: #e4e6f5;
  --text-primary: #0f1033;
  --text-secondary: #3a4466;
  --text-tertiary: #606890;
  --border-color: #c2c8e8;
  --accent-primary: #4f46e5;
  --accent-hover: #6366f1;
  --accent-secondary: #7c3aed;
  --accent-tertiary: #eef0ff;
  --link-color: #4f46e5;
  --link-hover: #6366f1;
  --shadow: rgba(0, 0, 0, 0.05);
  --gradient-subtle: linear-gradient(135deg, rgba(79, 70, 229, 0.07) 0%, rgba(124, 58, 237, 0.04) 100%);
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
  font-family: 'Nunito', system-ui, sans-serif;
  color: var(--text-primary);
  line-height: 1.7;
  letter-spacing: 0;
  font-weight: 400;
  background: var(--bg-primary);
  transition: background-color 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              color 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Global scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--accent-primary) 30%, var(--border-color));
  border-radius: 4px;
  border: 2px solid var(--bg-primary);
}

::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--accent-primary) 55%, var(--border-color));
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
  font-family: 'Urbanist', sans-serif;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.15;
  color: var(--text-primary);
}

h1 {
  font-size: clamp(2.25rem, 5vw, 3.75rem);
  font-weight: 800;
}

h2 {
  font-size: clamp(1.875rem, 4vw, 2.75rem);
  font-weight: 700;
}

h3 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
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

/* Page Transitions */
.page-enter-active {
  transition: opacity 0.38s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.38s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-leave-active {
  transition: opacity 0.22s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(24px) scale(0.99);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-14px) scale(0.99);
}

/* Navigation */
.navbar {
  background: rgba(5, 6, 15, 0.96);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-bottom: 1px solid rgba(129, 140, 248, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background-color 0.35s ease;
}

:root[data-theme='light'] .navbar {
  background: rgba(242, 243, 250, 0.96);
  border-bottom-color: rgba(79, 70, 229, 0.15);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.875rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-family: 'Urbanist', sans-serif;
  font-size: 1.0625rem;
  font-weight: 800;
  font-style: normal;
  color: var(--text-primary);
  text-decoration: none;
  letter-spacing: -0.02em;
  transition: color 0.2s ease;
  position: relative;
  flex-shrink: 0;
}

.logo::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--accent-primary);
  box-shadow: 0 0 6px var(--accent-primary);
  transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo:hover {
  color: var(--accent-primary);
}

.logo:hover::after {
  width: 100%;
}

.logo:hover {
  text-decoration-color: transparent;
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
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 400;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.5rem 0;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
  position: relative;
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 1px;
  background: var(--accent-primary);
  box-shadow: 0 0 4px var(--accent-primary);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-links a:hover {
  color: var(--accent-primary);
}

.nav-links a:hover::after {
  width: 100%;
}

.nav-links a.active {
  color: var(--accent-primary);
  font-weight: 500;
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
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 400;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.5rem 0;
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
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
  display: block;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
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
  border: 1px solid rgba(129, 140, 248, 0.15);
  border-radius: 8px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(129, 140, 248, 0.05);
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
  padding: 0.625rem 1rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  transition: all 0.2s ease;
  border: none;
  border-radius: 6px;
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
  gap: 0.5rem;
  padding: 0.4375rem 0.75rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  transition: all 0.2s ease;
  width: 190px;
}

.search-bar:focus-within {
  border-color: var(--accent-primary);
  background: var(--bg-secondary);
  box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.1),
              0 0 8px rgba(129, 140, 248, 0.08);
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
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.02em;
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
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.55),
              0 6px 16px rgba(0, 0, 0, 0.3),
              0 0 0 1px rgba(129, 140, 248, 0.06);
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
  background: color-mix(in srgb, var(--accent-primary) 40%, var(--border-color));
  border-radius: 3px;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: var(--accent-primary);
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
  border-bottom: 1px solid color-mix(in srgb, var(--border-color) 31%, transparent);
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
  line-clamp: 2;
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
  width: 62px;
  height: 30px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
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
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  border-radius: 50%;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
}

.toggle-slider.light-mode {
  transform: translateX(0);
}

.toggle-slider.dark-mode {
  transform: translateX(32px);
}

.theme-toggle:hover .toggle-slider {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2),
              0 2px 4px rgba(0, 0, 0, 0.12);
}

/* Footer */
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  padding: 2rem 2rem 1.75rem;
  transition: background-color 0.35s ease;
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, var(--accent-primary) 40%, var(--accent-primary) 60%, transparent 100%);
  opacity: 0.35;
  box-shadow: 0 0 8px var(--accent-primary);
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 2rem;
}

/* Brand */
.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.footer-name {
  font-family: 'Urbanist', sans-serif;
  font-size: 0.9375rem;
  font-weight: 800;
  color: var(--text-primary);
  text-decoration: none;
  letter-spacing: -0.02em;
  transition: color 0.2s ease;
}

.footer-name:hover {
  color: var(--accent-primary);
}

.footer-status {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.footer-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--accent-primary);
  box-shadow: 0 0 5px rgba(129, 140, 248, 0.6);
  animation: footerDotBlink 2.5s ease-in-out infinite;
  flex-shrink: 0;
}

@keyframes footerDotBlink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}

/* Nav quick-links — centered */
.footer-nav {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.footer-nav a {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-nav a:hover {
  color: var(--accent-primary);
}

/* Social icons + copyright — right-aligned */
.footer-social {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.footer-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.footer-links a {
  color: var(--text-tertiary);
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: color 0.2s ease, transform 0.2s ease;
}

.footer-links a:hover {
  color: var(--accent-primary);
  transform: translateY(-2px);
}

.copyright {
  color: var(--text-tertiary);
  font-size: 0.72rem;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.03em;
}

/* Mobile overlay backdrop */
.mobile-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(5, 6, 15, 0.65);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 99;
}

.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.3s ease;
}

.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .mobile-overlay {
    display: block;
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
    box-shadow: -8px 0 40px rgba(0, 0, 0, 0.55),
                0 0 0 1px rgba(129, 140, 248, 0.07);
    border-left: 1px solid color-mix(in srgb, var(--accent-primary) 18%, var(--border-color));
    border-top: 3px solid var(--accent-primary);
    transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    gap: 1.5rem;
    align-items: flex-start;
  }

  .nav-links.mobile-open {
    right: 0;
  }

  .nav-links a {
    font-size: 1rem;
    width: 100%;
    padding: 0.625rem 0;
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
    font-size: 1rem;
    padding: 0.625rem 0;
  }

  .dropdown-arrow-btn {
    font-size: 1rem;
    padding: 0.625rem 0.5rem;
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
    line-clamp: 2;
    font-size: 0.75rem;
  }

  .footer-inner {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 1.5rem;
  }

  .footer-brand {
    align-items: center;
  }

  .footer-nav {
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .footer-social {
    align-items: center;
  }
}
</style>
