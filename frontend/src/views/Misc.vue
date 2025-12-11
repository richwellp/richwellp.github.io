<template>
  <div class="misc">
    <div class="container">
      <h1>Miscellaneous</h1>
      <p class="page-intro">
        Random things I want to share—photos, thoughts, and other stuff that doesn't quite fit
        elsewhere.
      </p>

      <!-- Blog Section -->
      <section class="blog-section">
        <div class="section-header">
          <h2 class="section-title">Blog</h2>
          <router-link to="/misc/blog" class="view-all-link">View All →</router-link>
        </div>
        <p class="section-description">Thoughts, reflections, and technical write-ups</p>
        <div class="blog-preview">
          <router-link to="/misc/blog" class="blog-cta">
            <div class="blog-icon">📝</div>
            <div>
              <h3>Read My Posts</h3>
              <p>Explore articles about AI, software engineering, and personal experiences</p>
            </div>
          </router-link>
        </div>
      </section>
      
      <!-- Photo Albums Section -->
      <section class="albums-section">
        <h2 class="section-title">Photo Albums</h2>
        <div class="albums-grid">
          <!-- Travel Album -->
          <router-link to="/misc/travel" class="album-card">
            <div class="album-cover">
              <img src="/assets/photos/travel/colorado/personal_emlake.jpg" alt="Travel" />
              <div class="album-overlay">
                <span class="view-album">View Album →</span>
              </div>
            </div>
            <div class="album-info">
              <h3>✈️ Travel</h3>
              <p class="album-description">Adventures around the world</p>
              <span class="photo-count">Philippines • Japan • Wyoming • Colorado • California • Illinois and more </span>
            </div>
          </router-link>

          <!-- Professional Album -->
          <router-link to="/misc/professional" class="album-card">
            <div class="album-cover">
              <img src="/assets/photos/professional/professional_1.jpg" alt="Professional" />
              <div class="album-overlay">
                <span class="view-album">View Album →</span>
              </div>
            </div>
            <div class="album-info">
              <h3>💼 Professional</h3>
              <p class="album-description">Work events and milestones</p>
              <span class="photo-count">Graduation • Headshots • Work Events</span>
            </div>
          </router-link>

          <!-- Sports Album -->
          <router-link to="/misc/sports" class="album-card">
            <div class="album-cover">
              <div class="album-placeholder">
                <span class="placeholder-icon">💪</span>
                <span class="placeholder-text">Coming Soon</span>
              </div>
            </div>
            <div class="album-info">
              <h3>🏐 Sports</h3>
              <p class="album-description">Volleyball and powerlifting adventures</p>
              <span class="photo-count">Volleyball • Powerlifting</span>
            </div>
          </router-link>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.misc {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  text-align: center;
}

.page-intro {
  text-align: center;
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 4rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.albums-section,
.blog-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.view-all-link {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.view-all-link:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.section-description {
  color: var(--text-secondary);
  font-size: 1.05rem;
  margin-bottom: 2rem;
}

/* Photo Albums */
.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.album-card {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  text-decoration: none;
  display: block;
}

.album-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.album-cover {
  position: relative;
  width: 100%;
  height: 250px;
  overflow: hidden;
  background: var(--bg-secondary);
}

.album-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.album-card:hover .album-cover img {
  transform: scale(1.05);
}

/* Hover overlay with "View Album" text */
.album-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.album-card:hover .album-overlay {
  opacity: 1;
}

.view-album {
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
}

.album-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.placeholder-text {
  color: var(--text-secondary);
  font-size: 1.2rem;
  font-weight: 600;
}

.album-info {
  padding: 1.5rem;
}

.album-info h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.album-description {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.photo-count {
  display: inline-block;
  color: var(--text-tertiary);
  font-size: 0.9rem;
  padding: 0.25rem 0;
}

/* Blog Section */
.blog-preview {
  display: flex;
  justify-content: center;
}

.blog-cta {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-decoration: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  max-width: 600px;
  width: 100%;
}

.blog-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.blog-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.blog-cta h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.blog-cta p {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 768px) {
  .misc {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .albums-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .blog-cta {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
</style>
