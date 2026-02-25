<template>
  <div class="album-page">
    <div class="container">
      <!-- Header -->
      <div class="album-header">
        <router-link to="/misc/albums" class="back-link">← Back to Albums</router-link>
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

        <!-- Slideshow -->
        <div v-if="currentPhotos.length > 0" class="slideshow-container">
          <!-- Main Slideshow Display -->
          <div class="slideshow-main">
            <button
              v-if="currentPhotos.length > 1"
              class="slideshow-nav prev"
              @click="previousSlide"
              aria-label="Previous photo"
            >
              &#10094;
            </button>

            <div class="slideshow-content" @click="openLightbox(currentPhotos[currentSlideIndex])">
              <OptimizedImage
                v-if="!isVideo(currentPhotos[currentSlideIndex])"
                :src="currentPhotos[currentSlideIndex].src"
                :alt="currentPhotos[currentSlideIndex].caption"
                size="lg"
                loading="eager"
                img-class="slideshow-image"
              />
              <video
                v-else
                :src="currentPhotos[currentSlideIndex].src"
                class="slideshow-video"
                autoplay
                muted
                loop
                playsinline
                preload="auto"
              />
            </div>

            <button
              v-if="currentPhotos.length > 1"
              class="slideshow-nav next"
              @click="nextSlide"
              aria-label="Next photo"
            >
              &#10095;
            </button>

            <!-- Caption -->
            <div class="slideshow-caption">
              <p>{{ currentPhotos[currentSlideIndex].caption }}</p>
              <span class="slideshow-counter">{{ currentSlideIndex + 1 }} / {{ currentPhotos.length }}</span>
            </div>
          </div>

          <!-- Playback Controls -->
          <div v-if="currentPhotos.length > 1" class="slideshow-controls">
            <button
              @click="toggleAutoplay"
              class="control-btn"
              :aria-label="isPlaying ? 'Pause slideshow' : 'Play slideshow'"
            >
              {{ isPlaying ? '⏸' : '▶' }}
            </button>
            <input
              type="range"
              min="1"
              max="10"
              v-model="playbackSpeed"
              class="speed-slider"
              aria-label="Slideshow speed"
            />
            <span class="speed-label">{{ playbackSpeed }}s</span>
          </div>

          <!-- Thumbnail Navigation -->
          <div v-if="currentPhotos.length > 1" class="slideshow-thumbnails">
            <div
              v-for="(item, index) in currentPhotos"
              :key="item.src"
              @click="currentSlideIndex = index"
              :class="['thumbnail', { active: index === currentSlideIndex }]"
            >
              <OptimizedImage
                v-if="!isVideo(item)"
                :src="item.src"
                :alt="item.caption"
                size="thumb"
                loading="lazy"
                img-class="thumbnail-image"
              />
              <video
                v-else
                :src="item.src"
                class="thumbnail-video"
                muted
                playsinline
                preload="metadata"
              />
            </div>
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
          preload="auto"
        />
        <p class="lightbox-caption">{{ lightboxPhoto.caption }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
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

// Slideshow state
const currentSlideIndex = ref(0)
const isPlaying = ref(false)
const playbackSpeed = ref(3) // seconds
let autoplayInterval = null

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

    // Check for video extensions
    const hasVideoExt = /\.(mp4|mov|webm|avi|mkv)(\?|#|$)/i.test(urlLower)
    if (hasVideoExt) return true

    // Check Content-Type in URL (Supabase includes it)
    if (urlLower.includes('video/')) return true
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

// Slideshow functions
const nextSlide = () => {
  currentSlideIndex.value = (currentSlideIndex.value + 1) % currentPhotos.value.length
}

const previousSlide = () => {
  currentSlideIndex.value = (currentSlideIndex.value - 1 + currentPhotos.value.length) % currentPhotos.value.length
}

const startAutoplay = () => {
  stopAutoplay()
  autoplayInterval = setInterval(() => {
    nextSlide()
  }, playbackSpeed.value * 1000)
}

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
    autoplayInterval = null
  }
}

const toggleAutoplay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    startAutoplay()
  } else {
    stopAutoplay()
  }
}

// Watch for changes in playback speed
watch(playbackSpeed, () => {
  if (isPlaying.value) {
    startAutoplay()
  }
})

// Reset slide index when photos change
watch(currentPhotos, () => {
  currentSlideIndex.value = 0
  stopAutoplay()
  isPlaying.value = false
})

// Cleanup on unmount
onUnmounted(() => {
  stopAutoplay()
})
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

/* Slideshow Container */
.slideshow-container {
  width: 100%;
  margin-top: 2rem;
}

.slideshow-main {
  position: relative;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border-color);
}

.slideshow-content {
  position: relative;
  width: 100%;
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  cursor: pointer;
}

.slideshow-content :deep(img),
:deep(.slideshow-image) {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.slideshow-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

/* Navigation Arrows */
.slideshow-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  font-size: 2rem;
  padding: 1rem 1.25rem;
  cursor: pointer;
  z-index: 10;
  transition: background 0.3s ease;
  border-radius: 4px;
}

.slideshow-nav:hover {
  background: rgba(0, 0, 0, 0.8);
}

.slideshow-nav.prev {
  left: 1rem;
}

.slideshow-nav.next {
  right: 1rem;
}

/* Caption */
.slideshow-caption {
  padding: 1.5rem;
  background: var(--bg-secondary);
  text-align: center;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.slideshow-caption p {
  color: var(--text-primary);
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.slideshow-counter {
  color: var(--text-tertiary);
  font-size: 0.9rem;
  white-space: nowrap;
}

/* Playback Controls */
.slideshow-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--bg-card);
  border-radius: 8px;
  margin: 2rem auto;
  max-width: 400px;
  border: 1px solid var(--border-color);
}

.control-btn {
  background: var(--accent-primary);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.control-btn:hover {
  background: var(--accent-hover);
  transform: scale(1.1);
}

.speed-slider {
  flex: 1;
  max-width: 200px;
  height: 6px;
  border-radius: 3px;
  background: var(--bg-tertiary);
  outline: none;
  -webkit-appearance: none;
}

.speed-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--accent-primary);
  cursor: pointer;
  transition: background 0.3s ease;
}

.speed-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--accent-primary);
  cursor: pointer;
  border: none;
  transition: background 0.3s ease;
}

.speed-slider::-webkit-slider-thumb:hover,
.speed-slider::-moz-range-thumb:hover {
  background: var(--accent-hover);
}

.speed-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  min-width: 40px;
  text-align: center;
}

/* Thumbnail Navigation */
.slideshow-thumbnails {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  margin-top: 2rem;
  border: 1px solid var(--border-color);
}

.slideshow-thumbnails::-webkit-scrollbar {
  height: 8px;
}

.slideshow-thumbnails::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.slideshow-thumbnails::-webkit-scrollbar-thumb {
  background: var(--accent-primary);
  border-radius: 4px;
}

.thumbnail {
  flex-shrink: 0;
  width: 120px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.3s ease;
  opacity: 0.6;
}

.thumbnail:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.thumbnail.active {
  opacity: 1;
  border-color: var(--accent-primary);
}

.thumbnail :deep(img),
:deep(.thumbnail-image) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumbnail-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
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

  .slideshow-content {
    height: 400px;
  }

  .slideshow-nav {
    font-size: 1.5rem;
    padding: 0.75rem 1rem;
  }

  .slideshow-caption {
    flex-direction: column;
    gap: 0.5rem;
  }

  .thumbnail {
    width: 90px;
    height: 60px;
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
