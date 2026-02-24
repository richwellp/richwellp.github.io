<template>
  <AlbumViewer
    v-if="!loading && albumData"
    :title="albumData.album.name"
    :subtitle="albumData.album.subtitle"
    :photos="transformedPhotos"
    :categories="categoryList"
    :defaultCategory="categoryList[0]?.id"
    :coming-soon="!transformedPhotos || (Array.isArray(transformedPhotos) && transformedPhotos.length === 0)"
    :coming-soon-message="getComingSoonMessage()"
  />
  <div v-else-if="loading" class="loading-state">
    <p>Loading album...</p>
  </div>
  <div v-else-if="error" class="error-state">
    <p>Error: {{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AlbumViewer from '../../components/AlbumViewer.vue'
import { useAlbums } from '../../composables/useAlbums'

const route = useRoute()
const { loading, error, fetchAlbumBySlug } = useAlbums()
const albumData = ref(null)

// Helper to properly capitalize category names (handles abbreviations)
function formatCategoryName(category) {
  // Uppercase common country/region abbreviations
  const abbreviations = ['usa', 'uk', 'uae', 'ussr', 'us']
  if (abbreviations.includes(category.toLowerCase())) {
    return category.toUpperCase()
  }

  // Standard title case for other categories
  return category.charAt(0).toUpperCase() + category.slice(1)
}

// Transform API categories to the format AlbumViewer expects
const categoryList = computed(() => {
  if (!albumData.value || !albumData.value.categories) return []

  return albumData.value.categories.map(category => ({
    id: category,
    name: formatCategoryName(category)
  }))
})

// Add video type detection to photos (API already returns correct format with 'src')
const transformedPhotos = computed(() => {
  if (!albumData.value || !albumData.value.photos) return []

  const addVideoType = (photo) => ({
    ...photo,
    type: photo.type || (photo.src?.match(/\.(mp4|mov|webm)$/i) ? 'video' : 'image')
  })

  // If photos is an object (categorized), add type to each photo
  if (typeof albumData.value.photos === 'object' && !Array.isArray(albumData.value.photos)) {
    const transformed = {}
    for (const [category, photos] of Object.entries(albumData.value.photos)) {
      transformed[category] = photos.map(addVideoType)
    }
    return transformed
  }

  // If photos is an array (uncategorized), add type to each photo
  return albumData.value.photos.map(addVideoType)
})

function getComingSoonMessage() {
  return `Photos will be added to this album soon!`
}

onMounted(async () => {
  try {
    const slug = route.params.slug
    albumData.value = await fetchAlbumBySlug(slug)
  } catch (err) {
    console.error('Failed to load album:', err)
  }
})
</script>

<style scoped>
.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-state {
  color: #ef4444;
}
</style>
