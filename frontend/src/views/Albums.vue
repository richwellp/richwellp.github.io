<template>
  <div class="albums-page">
    <div class="container">
      <!-- Header -->
      <div class="albums-header">
        <router-link to="/misc" class="back-link">← Back to Misc</router-link>
        <h1>📸 Photo Albums</h1>
        <p class="albums-subtitle">
          Moments captured through my lens—adventures, milestones, and memories from around the world
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading albums...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>Error loading albums: {{ error }}</p>
      </div>

      <!-- Albums Grid -->
      <div v-if="!loading && !error && albums.length > 0" class="albums-grid">
        <router-link
          v-for="album in albums"
          :key="album.id"
          :to="getAlbumRoute(album.slug)"
          :class="['album-card', { 'coming-soon': !album.published }]"
        >
          <div v-if="album.coverPhoto" class="album-image">
            <OptimizedImage
              :src="album.coverPhoto"
              :alt="`${album.name} Album`"
              size="md"
            />
          </div>
          <div v-else class="album-image placeholder">
            <div class="placeholder-icon">{{ album.icon }}</div>
          </div>
          <div class="album-content">
            <div class="album-header">
              <span class="album-icon">{{ album.icon }}</span>
              <h2>{{ album.name }}</h2>
            </div>
            <p class="album-description">{{ album.subtitle }}</p>
            <span v-if="album.published" class="view-more">View Album →</span>
            <span v-else class="coming-soon-badge">Coming Soon</span>
          </div>
        </router-link>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && albums.length === 0" class="empty-state">
        <p>No albums available yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import OptimizedImage from '../components/OptimizedImage.vue'
import { useAlbums } from '../composables/useAlbums'

const { albums, loading, error, fetchAlbums } = useAlbums()

// Map album slugs to routes
const albumRouteMap = {
  'travel': '/misc/travel',
  'me': '/misc/professional',
  'sports': '/misc/sports'
}

function getAlbumRoute(slug) {
  return albumRouteMap[slug] || `/misc/${slug}`
}

onMounted(async () => {
  try {
    const fetchedAlbums = await fetchAlbums()

    // Add cover photos for albums (hardcoded for now since photos are still in static files)
    fetchedAlbums.forEach(album => {
      if (album.slug === 'travel') {
        album.coverPhoto = '/assets/photos/travel/colorado/personal_emlake.jpg'
      } else if (album.slug === 'me') {
        album.coverPhoto = '/assets/photos/professional/professional_1.jpg'
      }
    })
  } catch (err) {
    console.error('Failed to load albums:', err)
  }
})
</script>

<style scoped>
.albums-page {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.albums-header {
  margin-bottom: 3rem;
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

.albums-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 800px;
}

/* Loading & Error States */
.loading,
.error,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.error {
  color: #ef4444;
}

/* Albums Grid */
.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.album-card {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-decoration: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  display: flex;
  flex-direction: column;
}

.album-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.album-image {
  width: 100%;
  height: 240px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.album-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.album-card:hover .album-image :deep(img) {
  transform: scale(1.05);
}

.album-image.placeholder {
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.album-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.album-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.album-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.album-content h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.3;
}

.album-description {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
}

.view-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: 0.95rem;
  margin-top: auto;
}

.album-card:hover .view-more {
  color: var(--link-hover);
}

.coming-soon-badge {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  margin-top: auto;
}

.album-card.coming-soon {
  opacity: 0.8;
}

.album-card.coming-soon:hover {
  opacity: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .albums-page {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .albums-grid {
    grid-template-columns: 1fr;
  }

  .album-image {
    height: 200px;
  }
}
</style>
