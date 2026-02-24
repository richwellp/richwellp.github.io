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

      <!-- Filter Controls -->
      <div v-if="!loading && !error && albums.length > 0" class="filter-controls">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search albums..."
            class="search-input"
          />
        </div>
        <div class="filter-stats">
          {{ filteredAlbums.length }} {{ filteredAlbums.length === 1 ? 'album' : 'albums' }}
        </div>
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
      <div v-if="!loading && !error && filteredAlbums.length > 0" class="albums-grid">
        <router-link
          v-for="album in filteredAlbums"
          :key="album.id"
          :to="getAlbumRoute(album.slug)"
          :class="['album-card', { 'coming-soon': !album.published }]"
        >
          <div v-if="album.cover_photo" class="album-image">
            <img
              :src="album.cover_photo"
              :alt="`${album.name} Album`"
              loading="lazy"
            />
          </div>
          <div v-else class="album-image placeholder">
            <div class="placeholder-text">No cover photo</div>
          </div>
          <div class="album-content">
            <div class="album-header">
              <h2>{{ album.name }}</h2>
            </div>
            <p class="album-description">{{ album.subtitle }}</p>
            <span v-if="album.published" class="view-more">View Album →</span>
            <span v-else class="coming-soon-badge">Coming Soon</span>
          </div>
        </router-link>
      </div>

      <!-- Empty State (No Results from Search) -->
      <div v-if="!loading && !error && albums.length > 0 && filteredAlbums.length === 0" class="empty-state">
        <p>No albums match your search "{{ searchQuery }}"</p>
        <button @click="searchQuery = ''" class="btn-clear">Clear Search</button>
      </div>

      <!-- Empty State (No Albums) -->
      <div v-if="!loading && !error && albums.length === 0" class="empty-state">
        <p>No albums available yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAlbums } from '../composables/useAlbums'

const { albums, loading, error, fetchAlbums } = useAlbums()
const searchQuery = ref('')

// All albums use dynamic route: /misc/albums/:slug
function getAlbumRoute(slug) {
  return `/misc/albums/${slug}`
}

// Filter albums by search query
const filteredAlbums = computed(() => {
  if (!searchQuery.value.trim()) {
    return albums.value
  }

  const query = searchQuery.value.toLowerCase().trim()
  return albums.value.filter(album => {
    const nameMatch = album.name?.toLowerCase().includes(query)
    const subtitleMatch = album.subtitle?.toLowerCase().includes(query)
    const slugMatch = album.slug?.toLowerCase().includes(query)
    return nameMatch || subtitleMatch || slugMatch
  })
})

onMounted(async () => {
  try {
    await fetchAlbums()
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

/* Filter Controls */
.filter-controls {
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

.filter-stats {
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
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

.placeholder-text {
  font-size: 1.2rem;
  color: var(--text-secondary);
  opacity: 0.7;
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

.btn-clear {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-clear:hover {
  background: var(--bg-tertiary);
  border-color: var(--accent-primary);
}

/* Responsive */
@media (max-width: 768px) {
  .albums-page {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .filter-stats {
    text-align: center;
  }

  .albums-grid {
    grid-template-columns: 1fr;
  }

  .album-image {
    height: 200px;
  }
}
</style>
