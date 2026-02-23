<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import { useTheme } from './composables/useTheme'
import ChatAssistant from './components/ChatAssistant.vue'

const mobileMenuOpen = ref(false)
const miscDropdownOpen = ref(false)
const { theme, toggleTheme } = useTheme()

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
              <RouterLink to="/misc" @click="closeMobileMenu" class="dropdown-item">
                Albums
              </RouterLink>
            </div>
          </div>

          <RouterLink to="/contact" @click="closeMobileMenu" active-class="active">
            Contact
          </RouterLink>

          <!-- Theme Toggle -->
          <button @click="toggleTheme" class="theme-toggle" aria-label="Toggle theme">
            <div class="toggle-track">
              <span class="toggle-icon sun">☀️</span>
              <span class="toggle-icon moon">🌙</span>
              <div class="toggle-slider" :class="{ 'dark-mode': theme === 'dark' }"></div>
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
  </div>
</template>

<style>
/* GitHub-Style Theme Variables */
:root[data-theme='dark'] {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --bg-card: #161b22;
  --bg-hover: #21262d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-tertiary: #6e7681;
  --border-color: #30363d;
  --accent-primary: #238636;
  --accent-hover: #2ea043;
  --accent-muted: #1a7f37;
  --link-color: #58a6ff;
  --link-hover: #79c0ff;
  --shadow: rgba(0, 0, 0, 0.3);
}

:root[data-theme='light'] {
  --bg-primary: #ffffff;
  --bg-secondary: #f6f8fa;
  --bg-tertiary: #eaeef2;
  --bg-card: #ffffff;
  --bg-hover: #f6f8fa;
  --text-primary: #1f2328;
  --text-secondary: #656d76;
  --text-tertiary: #8c959f;
  --border-color: #d1d9e0;
  --accent-primary: #1a7f37;
  --accent-hover: #2da44e;
  --accent-muted: #218bff;
  --link-color: #0969da;
  --link-hover: #0550ae;
  --shadow: rgba(0, 0, 0, 0.1);
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    sans-serif;
  color: var(--text-primary);
  line-height: 1.6;
  background: var(--bg-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
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
  background: var(--bg-card);
  box-shadow: 0 1px 0 var(--border-color);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background-color 0.3s ease;
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
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.logo:hover {
  color: var(--accent-primary);
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
  font-size: 1rem;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.nav-links a:hover {
  color: var(--text-primary);
}

.nav-links a.active {
  color: var(--text-primary);
  border-bottom-color: var(--accent-primary);
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
  padding: 0.5rem 0.25rem;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
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
  margin-top: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px var(--shadow);
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
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
  transition: all 0.2s ease;
  border: none;
  border-bottom: none;
}

.dropdown-item:first-child {
  border-radius: 8px 8px 0 0;
}

.dropdown-item:last-child {
  border-radius: 0 0 8px 8px;
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.dropdown-item.router-link-active {
  background: var(--bg-hover);
  color: var(--accent-primary);
}

.item-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

/* Theme Toggle Button */
.theme-toggle {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.toggle-track {
  position: relative;
  width: 70px;
  height: 32px;
  background: var(--bg-hover);
  border: 2px solid var(--border-color);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px;
  transition: all 0.3s ease;
}

.theme-toggle:hover .toggle-track {
  border-color: var(--accent-primary);
}

.toggle-icon {
  font-size: 1rem;
  z-index: 1;
  transition: all 0.3s ease;
  line-height: 1;
}

.toggle-icon.sun {
  opacity: 0.4;
}

.toggle-icon.moon {
  opacity: 0.4;
}

/* Highlight active icon */
:root[data-theme='light'] .toggle-icon.sun {
  opacity: 1;
  transform: scale(1.1);
}

:root[data-theme='dark'] .toggle-icon.moon {
  opacity: 1;
  transform: scale(1.1);
}

.toggle-slider {
  position: absolute;
  left: 2px;
  width: 24px;
  height: 24px;
  background: var(--accent-primary);
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px var(--shadow);
}

.toggle-slider.dark-mode {
  transform: translateX(38px);
}

/* Footer */
.footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 2rem;
  margin-top: 4rem;
  transition: background-color 0.3s ease;
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

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .social-links {
    justify-content: center;
  }
}
</style>
