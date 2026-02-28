<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Fuse from 'fuse.js'
import { useProfessionalInfo } from '../composables/useProfessionalInfo.js'
import { useBlog } from '../composables/useBlog.js'

const router = useRouter()
const { projects, experience, skills, loadProfessionalInfo } = useProfessionalInfo()
const isOpen = ref(false)
const searchQuery = ref('')
const selectedIndex = ref(0)
const searchInput = ref(null)
const resultsContainer = ref(null)
const isLoading = ref(false)
const recentSearches = ref([])

// Search data sources
const blogPosts = ref([])
const searchableContent = ref([])

// Load blog posts from API
const { fetchPosts } = useBlog()

async function loadBlogPosts() {
  try {
    const data = await fetchPosts()
    blogPosts.value = data.posts || []
  } catch (error) {
    // Silently fail in development (expected)
    console.debug('Blog posts unavailable:', error.message)
    blogPosts.value = []
  }
}

// Build searchable content index
function buildSearchIndex() {
  const content = []

  // Add blog posts
  blogPosts.value.forEach(post => {
    content.push({
      type: 'blog',
      icon: '📝',
      title: post.title,
      subtitle: post.excerpt,
      tags: post.tags,
      path: `/misc/blog/${post.slug}`,
      searchText: `${post.title} ${post.excerpt} ${post.tags.join(' ')}`
    })
  })

  // Add projects
  projects.value.forEach(project => {
    content.push({
      type: 'project',
      icon: '🚀',
      title: project.name,
      subtitle: project.subtitle,
      description: project.description,
      path: '/projects',
      searchText: `${project.name} ${project.subtitle} ${project.description} ${project.technologies.join(' ')}`
    })
  })

  // Add experience
  experience.value.forEach(exp => {
    content.push({
      type: 'experience',
      icon: '💼',
      title: `${exp.title} at ${exp.company}`,
      subtitle: exp.dates,
      description: exp.description,
      path: '/experience',
      searchText: `${exp.title} ${exp.company} ${exp.description} ${exp.technologies.join(' ')}`
    })
  })

  // Add skills - dynamically iterate over all categories
  const allSkills = []
  if (skills.value) {
    Object.entries(skills.value).forEach(([categoryKey, categorySkills]) => {
      if (Array.isArray(categorySkills)) {
        // Convert category key to readable name (e.g., 'ai_ml' -> 'AI/ML', 'languages' -> 'Languages')
        const categoryName = categoryKey
          .split('_')
          .map(word => word.toUpperCase())
          .join('/')

        categorySkills.forEach(skillName => {
          allSkills.push({
            category: categoryName,
            name: skillName
          })
        })
      }
    })
  }

  allSkills.forEach(skill => {
    content.push({
      type: 'skill',
      icon: '⚡',
      title: skill.name,
      subtitle: skill.category,
      path: '/experience',
      searchText: `${skill.name} ${skill.category}`
    })
  })

  // Add pages
  const pages = [
    { title: 'About Me', path: '/', icon: '👤', description: 'Learn more about Richwell Perez' },
    { title: 'Experience', path: '/experience', icon: '💼', description: 'Professional work experience' },
    { title: 'Projects', path: '/projects', icon: '🚀', description: 'Portfolio projects and work' },
    { title: 'CV', path: '/cv', icon: '📄', description: 'Download resume and CV' },
    { title: 'Blog', path: '/misc/blog', icon: '📝', description: 'Read blog posts and articles' },
    { title: 'Contact', path: '/contact', icon: '✉️', description: 'Get in touch' }
  ]

  pages.forEach(page => {
    content.push({
      type: 'page',
      icon: page.icon,
      title: page.title,
      subtitle: page.description,
      path: page.path,
      searchText: `${page.title} ${page.description}`
    })
  })

  searchableContent.value = content
}

// Fuse.js configuration
const fuseOptions = {
  keys: ['title', 'subtitle', 'searchText', 'tags'],
  threshold: 0.4,
  distance: 100,
  minMatchCharLength: 2,
  includeScore: true
}

// Search function
const searchResults = computed(() => {
  if (!searchQuery.value.trim()) {
    return []
  }

  const fuse = new Fuse(searchableContent.value, fuseOptions)
  const results = fuse.search(searchQuery.value)

  // Group by type and limit to 10 results per category
  const grouped = {
    page: [],
    blog: [],
    project: [],
    experience: [],
    skill: []
  }

  results.forEach(result => {
    const type = result.item.type
    if (grouped[type] && grouped[type].length < 10) {
      grouped[type].push(result.item)
    }
  })

  return grouped
})

// Flat results for keyboard navigation
const flatResults = computed(() => {
  const flat = []
  const groups = searchResults.value
  const order = ['page', 'blog', 'project', 'experience', 'skill']

  order.forEach(type => {
    if (groups[type] && groups[type].length > 0) {
      flat.push(...groups[type])
    }
  })

  return flat
})

// Category labels
const categoryLabels = {
  page: 'Pages',
  blog: 'Blog Posts',
  project: 'Projects',
  experience: 'Experience',
  skill: 'Skills'
}

// Open/close palette
function openPalette() {
  isOpen.value = true
  searchQuery.value = ''
  selectedIndex.value = 0
  nextTick(() => {
    searchInput.value?.focus()
  })
}

function closePalette() {
  isOpen.value = false
  searchQuery.value = ''
  selectedIndex.value = 0
}

// Expose openPalette so parent components can trigger it
defineExpose({
  openPalette
})

// Handle keyboard shortcuts
function handleKeyDown(event) {
  // Cmd/Ctrl + K to open
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    if (isOpen.value) {
      closePalette()
    } else {
      openPalette()
    }
    return
  }

  // Only handle these keys when palette is open
  if (!isOpen.value) return

  switch (event.key) {
    case 'Escape':
      event.preventDefault()
      closePalette()
      break
    case 'ArrowDown':
      event.preventDefault()
      if (flatResults.value.length > 0) {
        selectedIndex.value = (selectedIndex.value + 1) % flatResults.value.length
        scrollToSelected()
      }
      break
    case 'ArrowUp':
      event.preventDefault()
      if (flatResults.value.length > 0) {
        selectedIndex.value = selectedIndex.value === 0
          ? flatResults.value.length - 1
          : selectedIndex.value - 1
        scrollToSelected()
      }
      break
    case 'Enter':
      event.preventDefault()
      if (flatResults.value.length > 0) {
        selectResult(flatResults.value[selectedIndex.value])
      }
      break
  }
}

// Scroll selected item into view
function scrollToSelected() {
  nextTick(() => {
    const selected = resultsContainer.value?.querySelector('.result-item.selected')
    if (selected) {
      selected.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
    }
  })
}

// Select a result
function selectResult(result) {
  if (!result) return

  // Add to recent searches
  const recentItem = {
    title: result.title,
    path: result.path,
    icon: result.icon,
    timestamp: Date.now()
  }

  // Remove duplicates and add to front
  recentSearches.value = [
    recentItem,
    ...recentSearches.value.filter(item => item.path !== result.path)
  ].slice(0, 5) // Keep only 5 most recent

  // Save to localStorage
  localStorage.setItem('commandPaletteRecent', JSON.stringify(recentSearches.value))

  // Navigate
  router.push(result.path)
  closePalette()
}

// Load recent searches from localStorage
function loadRecentSearches() {
  try {
    const saved = localStorage.getItem('commandPaletteRecent')
    if (saved) {
      recentSearches.value = JSON.parse(saved)
    }
  } catch (error) {
    console.error('Error loading recent searches:', error)
  }
}

// Click outside to close
function handleClickOutside(event) {
  if (isOpen.value && !event.target.closest('.command-palette-modal')) {
    closePalette()
  }
}

// Watch search query changes
watch(searchQuery, () => {
  selectedIndex.value = 0
})

// Lifecycle
onMounted(async () => {
  await loadProfessionalInfo()
  await loadBlogPosts()
  buildSearchIndex()
  loadRecentSearches()
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('click', handleClickOutside)
})

// Get flat index for a specific item
function getFlatIndex(item) {
  return flatResults.value.findIndex(r => r === item)
}
</script>

<template>
  <div>
    <!-- Backdrop -->
    <Transition name="fade">
      <div v-if="isOpen" class="command-palette-backdrop"></div>
    </Transition>

    <!-- Modal -->
    <Transition name="slide-fade">
      <div v-if="isOpen" class="command-palette-modal">
        <!-- Search Input -->
        <div class="search-header">
          <span class="search-icon">🔍</span>
          <input
            id="command-palette-search"
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            class="search-input"
            aria-label="Search pages and commands"
            placeholder="Search pages, blog posts, projects, experience, skills..."
            autocomplete="off"
            spellcheck="false"
          />
          <kbd class="kbd">ESC</kbd>
        </div>

        <!-- Results -->
        <div ref="resultsContainer" class="results-container">
          <!-- Loading State -->
          <div v-if="isLoading" class="loading-state">
            <div class="spinner"></div>
            <p>Searching...</p>
          </div>

          <!-- Recent Searches (show when no query) -->
          <div v-else-if="!searchQuery.trim() && recentSearches.length > 0" class="results-section">
            <div class="section-header">
              <span class="section-icon">🕐</span>
              <h3>Recent</h3>
            </div>
            <div
              v-for="(item, index) in recentSearches"
              :key="index"
              class="result-item"
              @click="router.push(item.path); closePalette()"
            >
              <span class="result-icon">{{ item.icon }}</span>
              <div class="result-content">
                <div class="result-title">{{ item.title }}</div>
              </div>
            </div>
          </div>

          <!-- No Results -->
          <div v-else-if="searchQuery.trim() && flatResults.length === 0" class="empty-state">
            <span class="empty-icon">🔍</span>
            <p>No results found for "{{ searchQuery }}"</p>
            <small>Try searching for pages, blog posts, projects, or skills</small>
          </div>

          <!-- Grouped Results -->
          <template v-else-if="searchQuery.trim()">
            <div
              v-for="(items, type) in searchResults"
              :key="type"
              v-show="items.length > 0"
              class="results-section"
            >
              <div class="section-header">
                <span class="section-icon">{{ items[0]?.icon || '📄' }}</span>
                <h3>{{ categoryLabels[type] }}</h3>
                <span class="result-count">{{ items.length }}</span>
              </div>
              <div
                v-for="(item, index) in items"
                :key="index"
                class="result-item"
                :class="{ selected: getFlatIndex(item) === selectedIndex }"
                @click="selectResult(item)"
                @mouseenter="selectedIndex = getFlatIndex(item)"
              >
                <span class="result-icon">{{ item.icon }}</span>
                <div class="result-content">
                  <div class="result-title">{{ item.title }}</div>
                  <div v-if="item.subtitle" class="result-subtitle">{{ item.subtitle }}</div>
                </div>
                <kbd class="kbd">↵</kbd>
              </div>
            </div>
          </template>

          <!-- Help Text (show when no query) -->
          <div v-if="!searchQuery.trim() && recentSearches.length === 0" class="help-text">
            <p>Start typing to search...</p>
            <div class="help-shortcuts">
              <div class="help-item">
                <kbd class="kbd">↑</kbd>
                <kbd class="kbd">↓</kbd>
                <span>Navigate</span>
              </div>
              <div class="help-item">
                <kbd class="kbd">↵</kbd>
                <span>Select</span>
              </div>
              <div class="help-item">
                <kbd class="kbd">ESC</kbd>
                <span>Close</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="palette-footer">
          <div class="footer-shortcuts">
            <div class="shortcut-group">
              <kbd class="kbd">↑</kbd>
              <kbd class="kbd">↓</kbd>
              <span>Navigate</span>
            </div>
            <div class="shortcut-group">
              <kbd class="kbd">↵</kbd>
              <span>Select</span>
            </div>
            <div class="shortcut-group">
              <kbd class="kbd">ESC</kbd>
              <span>Close</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<style scoped>
/* Backdrop */
.command-palette-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(6px) saturate(120%);
  -webkit-backdrop-filter: blur(6px) saturate(120%);
  z-index: 9998;
}

/* Modal */
.command-palette-modal {
  position: fixed;
  top: 20vh;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 640px;
  max-height: 60vh;
  background: var(--bg-card);
  border: 1px solid color-mix(in srgb, var(--accent-primary) 18%, var(--border-color));
  border-radius: 12px;
  box-shadow: 0 20px 80px rgba(0, 0, 0, 0.7),
              0 0 0 1px rgba(129, 140, 248, 0.06),
              0 0 60px rgba(129, 140, 248, 0.07);
  display: flex;
  flex-direction: column;
  z-index: 9999;
  overflow: hidden;
}

.command-palette-modal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  z-index: 1;
  border-radius: 12px 12px 0 0;
}

/* Search Header */
.search-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-card);
}

.search-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1rem;
  color: var(--text-primary);
  font-family: 'Nunito', system-ui, sans-serif;
  font-weight: 400;
  letter-spacing: 0;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

/* Keyboard Shortcuts */
.kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 6px;
  font-size: 0.75rem;
  font-family: monospace;
  font-weight: 600;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Results Container */
.results-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.results-container::-webkit-scrollbar {
  width: 8px;
}

.results-container::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.results-container::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--accent-primary) 28%, var(--border-color));
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--accent-primary) 52%, var(--border-color));
}

/* Results Section */
.results-section {
  margin-bottom: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-icon {
  font-size: 1rem;
}

.result-count {
  margin-left: auto;
  padding: 0.125rem 0.5rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  font-size: 0.7rem;
}

/* Result Item */
.result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: all 0.15s ease;
  border-left: 3px solid transparent;
}

.result-item:hover,
.result-item.selected {
  background: var(--bg-hover);
  border-left-color: var(--accent-primary);
}

.result-item.selected {
  background: var(--bg-hover);
}

.result-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.result-content {
  flex: 1;
  min-width: 0;
}

.result-title {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-subtitle {
  font-size: 0.85rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.125rem;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-state small {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

/* Help Text */
.help-text {
  padding: 2rem 1.25rem;
  text-align: center;
  color: var(--text-secondary);
}

.help-text p {
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.help-shortcuts {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.help-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}

/* Footer */
.palette-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.footer-shortcuts {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.shortcut-group {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.2s ease;
}

.slide-fade-leave-active {
  transition: all 0.15s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .command-palette-modal {
    top: 10vh;
    width: 95%;
    max-height: 70vh;
  }

  .result-item {
    padding: 0.875rem 1rem;
  }

  .search-header {
    padding: 0.875rem 1rem;
  }

  .section-header {
    padding: 0.5rem 1rem;
  }
}
</style>
