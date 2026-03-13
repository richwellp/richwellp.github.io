<template>
  <div v-if="headings.length >= 3" class="toc-wrapper">
    <!-- Mobile: Collapsible TOC -->
    <div class="toc-mobile">
      <button
        class="toc-toggle"
        @click="isOpen = !isOpen"
        :aria-expanded="isOpen"
      >
        <span class="toc-icon">📑</span>
        <span class="toc-label">Table of Contents</span>
        <span class="toc-arrow">{{ isOpen ? '▼' : '▶' }}</span>
      </button>
      <nav v-if="isOpen" class="toc-nav mobile">
        <ul class="toc-list">
          <li v-for="heading in headings" :key="heading.id" :class="`level-${heading.level}`">
            <a
              :href="`#${heading.id}`"
              @click="scrollToSection"
              :class="{ active: activeId === heading.id }"
            >
              {{ heading.text }}
            </a>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Desktop: Sticky Sidebar TOC -->
    <nav class="toc-nav desktop" :class="{ sticky: isSticky }">
      <h3 class="toc-title">Table of Contents</h3>
      <ul class="toc-list">
        <li v-for="heading in headings" :key="heading.id" :class="`level-${heading.level}`">
          <a
            :href="`#${heading.id}`"
            @click="scrollToSection"
            :class="{ active: activeId === heading.id }"
          >
            {{ heading.text }}
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  headings: {
    type: Array,
    required: true,
    validator: (value) =>
      value.every(h => h.level && h.text && h.id)
  },
  postContent: {
    type: String,
    required: true
  }
})

const isOpen = ref(false)
const isSticky = ref(false)
const activeId = ref('')

const handleScroll = () => {
  // Update sticky state for desktop
  isSticky.value = window.scrollY > 200

  // Find active section
  const headingElements = document.querySelectorAll('h2[id], h3[id]')
  let currentActive = ''

  for (const element of headingElements) {
    const rect = element.getBoundingClientRect()
    // Check if element is in viewport (at least partially visible)
    if (rect.top <= window.innerHeight * 0.3) {
      currentActive = element.id
    } else {
      break
    }
  }

  activeId.value = currentActive || (headingElements.length > 0 ? headingElements[0].id : '')
}

const scrollToSection = (event) => {
  event.preventDefault()
  const target = event.target.getAttribute('href')
  const element = document.querySelector(target)

  if (element) {
    // Close mobile menu after clicking
    isOpen.value = false

    // Smooth scroll with offset for header
    const offsetTop = element.offsetTop - 80
    window.scrollTo({
      top: offsetTop,
      behavior: 'smooth'
    })

    // Update active state
    activeId.value = target.slice(1)
  }
}

onMounted(() => {
  // Add IDs to headings in post content if they don't already have them
  const postContentElement = document.querySelector('.post-content')
  if (postContentElement) {
    const headingElements = postContentElement.querySelectorAll('h2, h3')
    headingElements.forEach((heading) => {
      if (!heading.id) {
        const id = heading.textContent
          .toLowerCase()
          .replace(/[^\w\s-]/g, '')
          .replace(/\s+/g, '-')
        heading.id = id
      }
    })
  }

  // Set initial active heading
  handleScroll()

  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.toc-wrapper {
  /* Position for desktop sticky sidebar */
  position: relative;
}

/* Mobile TOC (Collapsible) */
.toc-mobile {
  display: none;
  margin-bottom: 2rem;
}

.toc-toggle {
  width: 100%;
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  padding: 1.125rem 1.25rem;
  color: var(--text-primary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-weight: 600;
  letter-spacing: -0.01em;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
}

.toc-toggle::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.4s ease;
}

@media (hover: hover) {
  .toc-toggle:hover {
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4),
                0 0 16px rgba(129, 140, 248, 0.08);
  }

  .toc-toggle:hover::before {
    opacity: 1;
  }
}

.toc-icon {
  font-size: 1.375rem;
}

.toc-label {
  flex: 1;
  text-align: left;
}

.toc-arrow {
  font-size: 0.875rem;
  color: var(--accent-primary);
  font-weight: 700;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toc-toggle[aria-expanded="true"] .toc-arrow {
  transform: rotate(90deg);
}

/* Desktop TOC (Sticky Sidebar) */
.toc-nav.desktop {
  position: absolute;
  top: 0;
  right: -300px;
  width: 260px;
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 12px;
  padding: 1.75rem;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3),
              0 1px 4px rgba(0, 0, 0, 0.18),
              0 0 0 1px rgba(129, 140, 248, 0.04);
  position: relative;
}

.toc-nav.desktop::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 12px 12px 0 0;
}

.toc-nav.desktop.sticky {
  position: fixed;
  top: 90px;
  right: auto;
  left: calc(50% + 500px);
}

.toc-title {
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.075em;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-color);
  position: relative;
}

.toc-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 40px;
  height: 2px;
  background: var(--accent-primary);
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-list li {
  margin-bottom: 0.5rem;
}

.toc-list li.level-2 > a {
  padding-left: 0;
}

.toc-list li.level-3 > a {
  padding-left: 1.25rem;
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
}

.toc-list a {
  display: block;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.625rem 0.875rem;
  border-radius: 6px;
  border-left: 3px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.5;
  font-weight: 400;
  letter-spacing: -0.01em;
}

@media (hover: hover) {
  .toc-list a:hover {
    color: var(--text-primary);
    background: linear-gradient(90deg, rgba(129, 140, 248, 0.08), transparent);
    border-left-color: var(--accent-primary);
    transform: translateX(2px);
  }
}

.toc-list a.active {
  color: var(--accent-primary);
  border-left-color: var(--accent-primary);
  background: linear-gradient(90deg, rgba(129, 140, 248, 0.12), transparent);
  font-weight: 600;
}

/* Mobile Navigation */
.toc-nav.mobile {
  background: var(--bg-tertiary);
  border-radius: 10px;
  padding: 1.25rem 0;
  margin-top: 0.75rem;
  animation: slideDown 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1.5px solid var(--border-color);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3),
              0 1px 4px rgba(0, 0, 0, 0.18);
}

.toc-nav.mobile .toc-list {
  max-height: 320px;
  overflow-y: auto;
}

.toc-nav.mobile a {
  padding: 0.75rem 1.5rem;
  border-left: 4px solid transparent;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
}

.toc-nav.mobile a.active {
  border-left-color: var(--accent-primary);
  background: linear-gradient(90deg, rgba(129, 140, 248, 0.12), transparent);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Scrollbar styling for TOC */
.toc-nav::-webkit-scrollbar {
  width: 6px;
}

.toc-nav::-webkit-scrollbar-track {
  background: transparent;
  margin: 4px 0;
}

.toc-nav::-webkit-scrollbar-thumb {
  background: var(--accent-primary);
  border-radius: 10px;
  transition: background 0.3s ease;
}

.toc-nav::-webkit-scrollbar-thumb:hover {
  background: var(--accent-hover);
}

/* Responsive: Hide desktop TOC and show mobile */
@media (max-width: 1400px) {
  .toc-nav.desktop {
    display: none;
  }

  .toc-mobile {
    display: block;
  }
}

@media (max-width: 768px) {
  .toc-mobile {
    display: block;
  }

  .toc-nav.desktop {
    display: none;
  }
}
</style>
