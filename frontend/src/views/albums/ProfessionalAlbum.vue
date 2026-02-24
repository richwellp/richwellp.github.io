<template>
  <AlbumViewer
    v-if="!loading && albumData"
    :title="albumData.album.name"
    icon="👤"
    :subtitle="albumData.album.subtitle"
    :photos="albumData.photos"
  />
  <div v-else-if="loading" class="loading-state">
    <p>Loading album...</p>
  </div>
  <div v-else-if="error" class="error-state">
    <p>Error: {{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AlbumViewer from '../../components/AlbumViewer.vue'
import { useAlbums } from '../../composables/useAlbums'

const { loading, error, fetchAlbumBySlug } = useAlbums()
const albumData = ref(null)

onMounted(async () => {
  try {
    albumData.value = await fetchAlbumBySlug('me')
  } catch (err) {
    console.error('Failed to load Me album:', err)
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
