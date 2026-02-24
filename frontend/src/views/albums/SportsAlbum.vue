<template>
  <AlbumViewer
    v-if="!loading && albumData"
    :title="albumData.album.name"
    icon="⚽"
    :subtitle="albumData.album.subtitle"
    :photos="albumData.photos"
    coming-soon
    coming-soon-message="Photos from volleyball matches and powerlifting sessions will be added here!"
  />
  <div v-else-if="loading" class="loading-state">
    <p>Loading album...</p>
  </div>
  <div v-else-if="error" class="error-state">
    <AlbumViewer
      title="Sports"
      icon="🏐"
      subtitle="Volleyball and powerlifting adventures"
      :photos="[]"
      coming-soon
      coming-soon-message="Photos from volleyball matches and powerlifting sessions will be added here!"
    />
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
    albumData.value = await fetchAlbumBySlug('sports')
  } catch (err) {
    // Sports album might not be published yet, show coming soon message
    console.log('Sports album not available yet (expected for unpublished album)')
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
</style>
