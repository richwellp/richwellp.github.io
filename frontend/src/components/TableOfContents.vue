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
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.toc-toggle:hover {
  background: var(--bg-tertiary);
  border-color: var(--accent-primary);
}

.toc-icon {
  font-size: 1.25rem;
}

.toc-label {
  flex: 1;
  text-align: left;
}

.toc-arrow {
  font-size: 0.8rem;
  color: var(--text-secondary);
  transition: transform 0.3s ease;
}

.toc-toggle[aria-expanded="true"] .toc-arrow {
  transform: none;
}

/* Desktop TOC (Sticky Sidebar) */
.toc-nav.desktop {
  position: absolute;
  top: 0;
  right: -280px;
  width: 250px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  transition: all 0.3s ease;
}

.toc-nav.desktop.sticky {
  position: fixed;
  top: 80px;
  right: auto;
  left: calc(50% + 480px);
}

.toc-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-list li {
  margin-bottom: 0.75rem;
}

.toc-list li.level-2 > a {
  padding-left: 0;
}

.toc-list li.level-3 > a {
  padding-left: 1rem;
  font-size: 0.9rem;
}

.toc-list a {
  display: block;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  border-left: 2px solid transparent;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  line-height: 1.4;
}

.toc-list a:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.toc-list a.active {
  color: var(--accent-primary);
  border-left-color: var(--accent-primary);
  background: rgba(var(--accent-primary-rgb), 0.1);
  font-weight: 600;
}

/* Mobile Navigation */
.toc-nav.mobile {
  background: var(--bg-tertiary);
  border-radius: 8px;
  padding: 1rem 0;
  margin-top: 0.5rem;
  animation: slideDown 0.3s ease;
}

.toc-nav.mobile .toc-list {
  max-height: 300px;
  overflow-y: auto;
}

.toc-nav.mobile a {
  padding: 0.5rem 1.5rem;
  border-left: 3px solid transparent;
}

.toc-nav.mobile a.active {
  border-left-color: var(--accent-primary);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scrollbar styling for TOC */
.toc-nav::-webkit-scrollbar {
  width: 6px;
}

.toc-nav::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 3px;
}

.toc-nav::-webkit-scrollbar-thumb {
  background: var(--accent-primary);
  border-radius: 3px;
}

.toc-nav::-webkit-scrollbar-thumb:hover {
  background: var(--link-hover);
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
