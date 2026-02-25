<template>
  <router-link
    :to="`/misc/albums/${album.slug}`"
    class="album-card"
  >
    <div v-if="currentPhoto" class="album-cover">
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
        loop
        playsinline
        preload="metadata"
        class="cover-media"
        @ended="nextPhoto"
      />
    </div>

    <!-- Fallback to cover_photo if no photos loaded -->
    <div v-else-if="album.cover_photo" class="album-cover">
      <img
        :src="album.cover_photo"
        :alt="`${album.name} Album`"
        class="cover-media"
      />
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
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
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

<script>
import { computed } from 'vue'
</script>

<style scoped>
.album-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  display: block;
  box-shadow: 0 4px 15px var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  aspect-ratio: 4 / 3;
}

.album-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px var(--shadow);
}

.album-cover {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.cover-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.album-card:hover .cover-media {
  transform: scale(1.1);
}

.album-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.8));
  display: flex;
  align-items: flex-end;
  padding: 2rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.album-card:hover .album-overlay {
  opacity: 1;
}

.overlay-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: white;
}

.album-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.album-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0 0 0.5rem 0;
}

.view-link {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-primary);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease 0.1s;
}

.album-card:hover .view-link {
  opacity: 1;
  transform: translateY(0);
}
</style>
