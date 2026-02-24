<template>
  <div class="album-page">
    <div class="container">
      <!-- Header -->
      <div class="album-header">
        <router-link to="/misc" class="back-link">← Back to Misc</router-link>
        <h1>{{ title }}</h1>
        <p class="album-subtitle">{{ subtitle }}</p>
      </div>

      <!-- Coming Soon State -->
      <div v-if="comingSoon" class="coming-soon">
        <h2>Coming Soon</h2>
        <p>{{ comingSoonMessage || 'Photos will be added here soon!' }}</p>
      </div>

      <!-- Content (when not coming soon) -->
      <template v-else>
        <!-- Tabs (if categories exist) -->
        <div v-if="hasCategories" class="tabs">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="activeTab = category.id"
            :class="['tab', { active: activeTab === category.id }]"
          >
            {{ category.name }}
          </button>
        </div>

        <!-- Sort and Search Controls -->
        <div class="photo-controls">
          <div class="search-box">
            <input
              id="photo-search"
              v-model="searchQuery"
              type="text"
              placeholder="Search photos..."
              class="search-input"
              aria-label="Search photos by caption or location"
            />
          </div>
          <div class="sort-box">
            <label for="photo-sort" class="sort-label">Sort:</label>
            <select
              id="photo-sort"
              v-model="sortBy"
              class="sort-select"
            >
              <option value="order">Display Order</option>
              <option value="date-newest">Date (Newest First)</option>
              <option value="date-oldest">Date (Oldest First)</option>
            </select>
          </div>
        </div>

        <!-- Photo Grid -->
        <div v-if="currentPhotos.length > 0" class="photos-grid">
          <div v-for="item in currentPhotos" :key="item.src" class="photo-item">
            <OptimizedImage
              v-if="!isVideo(item)"
              :src="item.src"
              :alt="item.caption"
              size="md"
              loading="lazy"
              img-class="photo-image"
              @click="openLightbox(item)"
            />
            <video
              v-else
              :src="item.src"
              class="photo-video"
              @click="openLightbox(item)"
              muted
              loop
              playsinline
            />
            <p class="photo-caption">{{ item.caption }}</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="currentPhotos.length === 0 && !comingSoon" class="empty-state">
          <p>📸 No photos yet for this section. Check back later!</p>
        </div>
      </template>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxPhoto" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button class="lightbox-close" @click="closeLightbox">×</button>
        <OptimizedImage
          v-if="!isVideo(lightboxPhoto)"
          :src="lightboxPhoto.src"
          :alt="lightboxPhoto.caption"
          size="full"
          loading="eager"
          img-class="lightbox-image"
        />
        <video
          v-else
          :src="lightboxPhoto.src"
          class="lightbox-video"
          controls
          autoplay
          loop
          playsinline
        />
        <p class="lightbox-caption">{{ lightboxPhoto.caption }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import OptimizedImage from './OptimizedImage.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: '📷'
  },
  subtitle: {
    type: String,
    default: ''
  },
  photos: {
    type: [Array, Object],
    default: () => []
  },
  categories: {
    type: Array,
    default: () => []
  },
  defaultCategory: {
    type: String,
    default: null
  },
  comingSoon: {
    type: Boolean,
    default: false
  },
  comingSoonMessage: {
    type: String,
    default: ''
  }
})

const activeTab = ref(props.defaultCategory || (props.categories[0]?.id || null))
const lightboxPhoto = ref(null)
const searchQuery = ref('')
const sortBy = ref('order')

const hasCategories = computed(() => props.categories.length > 0)

// Helper to sort photos
function sortPhotos(photos) {
  const sorted = [...photos]

  if (sortBy.value === 'date-newest') {
    sorted.sort((a, b) => {
      if (!a.date_taken) return 1
      if (!b.date_taken) return -1
      return new Date(b.date_taken) - new Date(a.date_taken)
    })
  } else if (sortBy.value === 'date-oldest') {
    sorted.sort((a, b) => {
      if (!a.date_taken) return 1
      if (!b.date_taken) return -1
      return new Date(a.date_taken) - new Date(b.date_taken)
    })
  } else {
    // Display order (default)
    sorted.sort((a, b) => (a.order_index || 0) - (b.order_index || 0))
  }

  return sorted
}

// Helper to check if item is a video
function isVideo(item) {
  // Check type field if available
  if (item.type === 'video') return true
  if (item.type === 'image') return false

  // Fallback: detect from URL extension if type field is missing
  if (item.src) {
    const urlLower = item.src.toLowerCase()
    return /\.(mp4|mov|webm|avi|mkv)(\?|#|$)/.test(urlLower)
  }

  return false
}

// Helper to filter photos by search query
function filterPhotos(photos) {
  if (!searchQuery.value.trim()) return photos

  const query = searchQuery.value.toLowerCase().trim()
  return photos.filter(photo => {
    const captionMatch = photo.caption?.toLowerCase().includes(query)
    const locationMatch = photo.location?.toLowerCase().includes(query)
    return captionMatch || locationMatch
  })
}

const currentPhotos = computed(() => {
  let photos = []

  if (hasCategories.value && typeof props.photos === 'object' && !Array.isArray(props.photos)) {
    photos = props.photos[activeTab.value] || []
  } else {
    photos = Array.isArray(props.photos) ? props.photos : []
  }

  // Apply search filter
  photos = filterPhotos(photos)

  // Apply sorting
  photos = sortPhotos(photos)

  return photos
})

const openLightbox = (photo) => {
  lightboxPhoto.value = photo
}

const closeLightbox = () => {
  lightboxPhoto.value = null
}
</script>

<style scoped>
.album-page {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.album-header {
  margin-bottom: 2rem;
}

.back-link {
  display: inline-block;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--link-hover);
}

h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.album-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

/* Coming Soon */
.coming-soon {
  text-align: center;
  padding: 6rem 2rem;
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.coming-soon .icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
}

.coming-soon h2 {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.coming-soon p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.tab {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 6px 6px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.tab:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.tab.active {
  color: var(--accent-primary);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-bottom-color: var(--bg-card);
  position: relative;
  bottom: -2px;
}

/* Photo Controls */
.photo-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.sort-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-label {
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
}

.sort-select {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.sort-select:focus {
  outline: none;
  border-color: var(--accent-primary);
}

/* Photos Grid */
.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.photo-item {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.photo-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
}

.photo-item :deep(img),
.photo-item video,
:deep(.photo-image),
.photo-video {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
  cursor: pointer;
}

.photo-item video,
.photo-video {
  background: #000;
}

.photo-caption {
  padding: 1rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
  text-align: center;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: transparent;
  border: none;
  color: white;
  font-size: 3rem;
  cursor: pointer;
  font-weight: 300;
  transition: transform 0.2s ease;
}

.lightbox-close:hover {
  transform: scale(1.2);
}

.lightbox-content :deep(img),
.lightbox-content video,
:deep(.lightbox-image) {
  max-width: 100%;
  max-height: calc(90vh - 100px);
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-content video {
  background: #000;
}

.lightbox-caption {
  color: white;
  font-size: 1.1rem;
  margin-top: 1rem;
  text-align: center;
}

/* Responsive */
@media (max-width: 768px) {
  .album-page {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .tabs {
    gap: 0.25rem;
  }

  .tab {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .photo-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .sort-box {
    justify-content: space-between;
  }

  .photos-grid {
    grid-template-columns: 1fr;
  }

  .coming-soon {
    padding: 4rem 1rem;
  }

  .coming-soon .icon {
    font-size: 4rem;
  }

  .lightbox-close {
    top: -50px;
    font-size: 2.5rem;
  }
}
</style>
