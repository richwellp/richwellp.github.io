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

// Transform API categories to the format AlbumViewer expects
const categoryList = computed(() => {
  if (!albumData.value || !albumData.value.categories) return []

  return albumData.value.categories.map(category => ({
    id: category,
    name: category.charAt(0).toUpperCase() + category.slice(1)
  }))
})

// Transform photos from API format to AlbumViewer format
const transformedPhotos = computed(() => {
  if (!albumData.value || !albumData.value.photos) return []

  const transformPhoto = (photo) => ({
    src: photo.url,
    caption: photo.caption || '',
    type: photo.url?.match(/\.(mp4|mov|webm)$/i) ? 'video' : 'image'
  })

  // If photos is an object (categorized), transform each category
  if (typeof albumData.value.photos === 'object' && !Array.isArray(albumData.value.photos)) {
    const transformed = {}
    for (const [category, photos] of Object.entries(albumData.value.photos)) {
      transformed[category] = photos.map(transformPhoto)
    }
    return transformed
  }

  // If photos is an array (uncategorized), transform the array
  return albumData.value.photos.map(transformPhoto)
})

function getComingSoonMessage() {
  const slug = route.params.slug
  if (slug === 'sports') {
    return 'Photos from volleyball matches and powerlifting sessions will be added here!'
  }
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
