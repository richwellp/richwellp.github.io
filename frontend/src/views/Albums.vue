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

      <!-- Albums Grid with Slideshows -->
      <div v-if="!loading && !error && albums.length > 0" class="albums-grid">
        <AlbumCoverSlideshow
          v-for="album in albums"
          :key="album.id"
          :album="album"
        />
      </div>

      <!-- Empty State (No Albums) -->
      <div v-if="!loading && !error && albums.length === 0" class="empty-state">
        <p>No albums available yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AlbumCoverSlideshow from '../components/AlbumCoverSlideshow.vue'
import { useAlbums } from '../composables/useAlbums'

const { albums, loading, error, fetchAlbums } = useAlbums()

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
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.albums-header {
  margin-bottom: 4rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  margin-bottom: 1.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
}

.back-link:hover {
  color: var(--accent-hover);
  transform: translateX(-3px);
}

h1 {
  font-size: clamp(2.25rem, 4vw, 3rem);
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.025em;
}

.albums-subtitle {
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 720px;
  font-weight: 400;
}

/* Loading & Error States */
.loading,
.error,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  font-weight: 400;
}

.error {
  color: #dc2626;
  background: rgba(220, 38, 38, 0.08);
  border: 1.5px solid rgba(220, 38, 38, 0.3);
  border-radius: 10px;
  padding: 2rem;
  margin: 2rem 0;
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
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06),
              0 1px 3px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  position: relative;
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
  transition: opacity 0.4s ease;
  z-index: 2;
}

.album-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12),
              0 6px 12px rgba(0, 0, 0, 0.08);
  border-color: var(--accent-primary)60;
}

.album-card:hover::before {
  opacity: 1;
}

.album-image {
  width: 100%;
  height: 280px;
  overflow: hidden;
  background: var(--bg-secondary);
  position: relative;
}

.album-image :deep(img),
.album-image video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.album-image video {
  background: #000;
}

.album-card:hover .album-image :deep(img),
.album-card:hover .album-image video {
  transform: scale(1.08);
}

.album-image.placeholder {
  background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  font-size: clamp(1.125rem, 1.4vw, 1.25rem);
  color: var(--text-secondary);
  opacity: 0.6;
  font-weight: 500;
}

.album-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.album-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1rem;
}

.album-content h2 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin: 0;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.02em;
  transition: color 0.3s ease;
}

.album-card:hover .album-content h2 {
  color: var(--accent-primary);
}

.album-description {
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.65;
  margin-bottom: 1.25rem;
  flex: 1;
  font-weight: 400;
}

.view-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  margin-top: auto;
  letter-spacing: -0.01em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.album-card:hover .view-more {
  color: var(--accent-hover);
  transform: translateX(3px);
}

.coming-soon-badge {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
  font-weight: 500;
  margin-top: auto;
  border: 1px solid var(--border-color);
  letter-spacing: -0.01em;
}

.album-card.coming-soon {
  opacity: 0.7;
}

.album-card.coming-soon:hover {
  opacity: 0.95;
}

/* Responsive */
@media (max-width: 768px) {
  .albums-page {
    padding: 3.5rem 1.5rem;
  }

  .albums-header {
    margin-bottom: 3rem;
  }

  .albums-grid {
    grid-template-columns: 1fr;
    gap: 1.75rem;
  }

  .album-image {
    height: 240px;
  }

  .album-content {
    padding: 1.75rem;
  }
}

@media (max-width: 480px) {
  .albums-page {
    padding: 3rem 1.25rem;
  }

  .albums-header {
    margin-bottom: 2.5rem;
  }

  .albums-grid {
    gap: 1.5rem;
  }

  .album-image {
    height: 220px;
  }

  .album-content {
    padding: 1.5rem;
  }
}
</style>
