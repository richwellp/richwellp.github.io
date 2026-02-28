<template>
  <router-link
    :to="`/misc/albums/${album.slug}`"
    class="album-card"
  >
    <!-- Slideshow with fade transitions -->
    <div class="album-cover">
      <TransitionGroup name="fade-slide">
        <div
          v-if="currentPhoto"
          :key="currentPhotoIndex"
          class="slide-item"
        >
          <!-- Photo -->
          <img
            v-if="!isVideoPhoto(currentPhoto)"
            :src="currentPhoto.src"
            :alt="currentPhoto.caption || album.name"
            class="cover-media"
          />
          <!-- Video -->
          <video
            v-else
            :src="currentPhoto.src"
            muted
            autoplay
            playsinline
            preload="metadata"
            class="cover-media"
            @ended="nextPhoto"
          />
        </div>
        <!-- Fallback to cover_photo if no photos loaded -->
        <div
          v-else-if="album.cover_photo"
          key="fallback"
          class="slide-item"
        >
          <img
            :src="album.cover_photo"
            :alt="`${album.name} Album`"
            class="cover-media"
          />
        </div>
      </TransitionGroup>
    </div>

    <!-- Album Info Overlay -->
    <div class="album-overlay">
      <div class="overlay-content">
        <h3 class="album-title">{{ album.name }}</h3>
        <p class="album-subtitle">{{ album.subtitle }}</p>
        <span class="view-link">View Album →</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useAlbums } from '../composables/useAlbums'

const props = defineProps({
  album: {
    type: Object,
    required: true
  }
})

const { fetchAlbumBySlug } = useAlbums()

const photos = ref([])
const currentPhotoIndex = ref(0)
let photoTimer = null

const PHOTO_DURATION = 5000 // 5 seconds per photo

// Current photo being displayed
const currentPhoto = computed(() => {
  if (photos.value.length === 0) return null
  return photos.value[currentPhotoIndex.value]
})

// Check if photo is a video
const isVideoPhoto = (photo) => {
  if (!photo || !photo.src) return false
  if (photo.type === 'video') return true
  const urlLower = photo.src.toLowerCase()
  return /\.(mp4|mov|webm|avi|mkv)(\?|#|$)/i.test(urlLower) || urlLower.includes('video/')
}

// Load album photos
const loadPhotos = async () => {
  try {
    const fullAlbum = await fetchAlbumBySlug(props.album.slug)
    if (fullAlbum && fullAlbum.photos) {
      // Extract photos array
      const albumPhotos = Array.isArray(fullAlbum.photos)
        ? fullAlbum.photos
        : Object.values(fullAlbum.photos).flat()

      photos.value = albumPhotos
      startPhotoTimer()
    }
  } catch (error) {
    console.error(`Failed to load photos for album ${props.album.slug}:`, error)
  }
}

// Move to next photo
const nextPhoto = () => {
  if (photos.value.length === 0) return
  currentPhotoIndex.value = (currentPhotoIndex.value + 1) % photos.value.length
}

// Start timer for photo transitions (videos handle themselves)
const startPhotoTimer = () => {
  clearTimeout(photoTimer)

  const photo = currentPhoto.value
  if (!photo || isVideoPhoto(photo)) {
    return // Videos handle timing with @ended
  }

  photoTimer = setTimeout(() => {
    nextPhoto()
  }, PHOTO_DURATION)
}

// Watch for photo changes
watch(currentPhotoIndex, () => {
  startPhotoTimer()
})

onMounted(() => {
  loadPhotos()
})

onBeforeUnmount(() => {
  clearTimeout(photoTimer)
})
</script>

<style scoped>
.album-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  display: block;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35),
              0 1px 4px rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-color);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  aspect-ratio: 4 / 3;
}

.album-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 3;
}

.album-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.6),
              0 10px 24px rgba(0, 0, 0, 0.35),
              0 0 0 1px rgba(129, 140, 248, 0.1),
              0 0 50px rgba(129, 140, 248, 0.08);
  border-color: color-mix(in srgb, var(--accent-primary) 30%, transparent);
}

.album-card:hover::before {
  opacity: 1;
}

.album-cover {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.slide-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.cover-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.album-card:hover .cover-media {
  transform: scale(1.12);
}

/* Fade transition animations */
.fade-slide-enter-active {
  transition: opacity 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-leave-active {
  transition: opacity 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
}

.fade-slide-leave-to {
  opacity: 0;
}

.fade-slide-enter-to {
  opacity: 1;
}

.fade-slide-leave-from {
  opacity: 1;
}

.album-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom,
    rgba(15, 20, 25, 0.1) 0%,
    rgba(15, 20, 25, 0.6) 50%,
    rgba(15, 20, 25, 0.9) 100%);
  display: flex;
  align-items: flex-end;
  padding: 2.25rem;
  opacity: 0;
  transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 2;
}

.album-card:hover .album-overlay {
  opacity: 1;
}

.overlay-content {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  color: white;
}

.album-title {
  font-size: clamp(1.5rem, 2vw, 1.875rem);
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.album-subtitle {
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  opacity: 0.95;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
  font-weight: 400;
  letter-spacing: -0.01em;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

.view-link {
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-weight: 600;
  color: var(--accent-secondary);
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  opacity: 0;
  transform: translateY(15px);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s;
  letter-spacing: -0.01em;
  text-shadow: none;
  display: inline-block;
}

.album-card:hover .view-link {
  opacity: 1;
  transform: translateY(0) translateX(3px);
}
</style>
