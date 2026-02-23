<template>
  <div class="albums-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <h1>📸 Photo Albums</h1>
        <p class="page-intro">
          Moments captured through my lens—adventures, milestones, and memories from around the world.
        </p>
      </div>
    </div>

    <!-- Albums Grid -->
    <section class="albums-section">
      <div class="container">
        <div class="albums-grid">
          <!-- Travel Album -->
          <router-link to="/misc/travel" class="album-card featured">
            <div class="album-image">
              <OptimizedImage
                src="/assets/photos/travel/colorado/personal_emlake.jpg"
                alt="Travel Adventures"
                size="md"
              />
              <div class="album-overlay">
                <div class="overlay-content">
                  <span class="album-icon">✈️</span>
                  <span class="album-title">Travel</span>
                  <span class="album-subtitle">Exploring Philippines, USA, Japan, and many more</span>
                  <span class="view-link">View Album →</span>
                </div>
              </div>
            </div>
          </router-link>

          <!-- Professional Album -->
          <router-link to="/misc/professional" class="album-card">
            <div class="album-image">
              <OptimizedImage
                src="/assets/photos/professional/professional_1.jpg"
                alt="Professional Milestones"
                size="md"
              />
              <div class="album-overlay">
                <div class="overlay-content">
                  <span class="album-icon">💼</span>
                  <span class="album-title">Professional</span>
                  <span class="album-subtitle">Graduation • School/Work Events</span>
                  <span class="view-link">View Album →</span>
                </div>
              </div>
            </div>
          </router-link>

          <!-- Sports Album -->
          <router-link to="/misc/sports" class="album-card">
            <div class="album-image placeholder">
              <div class="placeholder-content">
                <span class="album-icon">🏐</span>
                <span class="album-title">Sports</span>
                <span class="album-subtitle">Coming Soon</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import OptimizedImage from '../components/OptimizedImage.vue'
</script>

<style scoped>
.albums-page {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: var(--bg-secondary);
  padding: 4rem 2rem;
  text-align: center;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.page-intro {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Albums Section */
.albums-section {
  background: var(--bg-primary);
  padding: 4rem 2rem;
}

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

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

.album-card.featured {
  grid-column: span 1;
}

.album-image {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.album-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.album-card:hover .album-image :deep(img) {
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

.album-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.album-title {
  font-size: 1.8rem;
  font-weight: 700;
}

.album-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
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

.album-image.placeholder {
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: var(--text-secondary);
}

.placeholder-content .album-icon {
  font-size: 4rem;
  margin: 0;
}

.placeholder-content .album-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.placeholder-content .album-subtitle {
  font-size: 1rem;
  opacity: 0.7;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section,
  .albums-section {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .page-intro {
    font-size: 1rem;
  }

  .albums-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .album-card.featured {
    grid-column: span 1;
  }

  .album-overlay {
    padding: 1.5rem;
  }

  .album-title {
    font-size: 1.5rem;
  }

  .album-subtitle {
    font-size: 0.85rem;
  }
}
</style>
