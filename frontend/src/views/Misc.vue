<template>
  <div class="misc">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <h1>Miscellaneous</h1>
        <p class="page-intro">
          Random things I want to share—photos, thoughts, and other stuff that doesn't quite fit
          elsewhere.
        </p>
      </div>
    </div>

    <!-- Blog Section -->
    <section class="blog-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Blog</h2>
          <router-link to="/misc/blog" class="view-all-link">View All →</router-link>
        </div>
        <p class="section-description">Thoughts, reflections, and technical write-ups</p>

        <div v-if="loading" class="loading-state">
          <p>Loading posts...</p>
        </div>

        <div v-else-if="recentPosts.length > 0" class="blog-grid">
          <router-link
            v-for="post in recentPosts"
            :key="post.slug"
            :to="`/misc/blog/${post.slug}`"
            class="blog-card"
          >
            <div class="blog-card-content">
              <div class="blog-date">{{ new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) }}</div>
              <h3>{{ post.title }}</h3>
              <p class="blog-excerpt">{{ post.excerpt }}</p>
              <div v-if="post.tags && post.tags.length" class="blog-tags">
                <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="read-more">Read More →</div>
          </router-link>
        </div>

        <div v-else class="no-posts">
          <p>No blog posts yet. Check back soon!</p>
        </div>
      </div>
    </section>

    <!-- Beyond Computer Science -->
    <section class="interests-section">
      <div class="container">
        <h2 class="section-title">Beyond Computer Science</h2>

        <!-- Photo Albums -->
        <h3 class="subsection-title">Photo Albums</h3>
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

        <!-- Interests -->
        <h3 class="subsection-title">Interests</h3>
        <div class="interests-grid">
          <div class="interest-card">
            <h3>🏐 Volleyball</h3>
            <p>I love <span class="dashed-strike">spiking</span> the strategy and teamwork that goes into every match.</p>
          </div>
          <div class="interest-card">
            <h3>💪 Powerlifting</h3>
            <p>Building strength and discipline, one rep at a time.</p>
          </div>
          <div class="interest-card">
            <h3>🎮 Gaming</h3>
            <p>Dota 2, Valorant, and some anime games: where my AI interest began.</p>
          </div>
          <div class="interest-card">
            <h3>✈️ Traveling</h3>
            <p>Exploring new places and experiencing different cultures.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Visitor Map -->
    <section class="visitor-map">
      <div class="container">
        <h2 class="section-title">Visitors</h2>
        <div class="map-container">
          <a v-if="!mapLoadError" href="https://clustrmaps.com/site/1c8ov" title="ClustrMaps" target="_blank" rel="noopener noreferrer">
            <img
              ref="mapImage"
              src="https://www.clustrmaps.com/map_v2.png?d=bUwnH32XrcZZm4BmWIy-rlCG47vK_-JRxDo71nilFs8&cl=ffffff"
              alt="Visitor Map"
              @load="handleMapLoad"
              @error="handleMapError"
            />
          </a>
          <div v-else class="map-error">
            <p>🌍 Visitor map is hidden</p>
            <p class="error-hint">If you're using an ad blocker, it may be blocking the visitor map. You can disable it to see where visitors are from!</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, onUnmounted, computed, ref, nextTick } from 'vue'
import { useBlog } from '../composables/useBlog'

const { posts, loading, fetchPosts } = useBlog()

const recentPosts = computed(() => posts.value.slice(0, 3))

// Visitor map functionality
const mapLoadError = ref(false)
const mapLoaded = ref(false)
const mapImage = ref(null)
let mapCheckTimeout = null

const handleMapLoad = () => {
  // Check if the image has valid dimensions (adblockers often replace with 1x1 pixel)
  if (mapImage.value && (mapImage.value.naturalWidth < 10 || mapImage.value.naturalHeight < 10)) {
    mapLoadError.value = true
  } else {
    mapLoaded.value = true
  }

  if (mapCheckTimeout) {
    clearTimeout(mapCheckTimeout)
  }
}

const handleMapError = () => {
  mapLoadError.value = true
  if (mapCheckTimeout) {
    clearTimeout(mapCheckTimeout)
  }
}

onMounted(() => {
  fetchPosts()

  // Fallback: Check after 2 seconds if the map loaded
  nextTick(() => {
    mapCheckTimeout = setTimeout(() => {
      if (!mapLoaded.value) {
        mapLoadError.value = true
      }
    }, 2000)
  })
})

onUnmounted(() => {
  if (mapCheckTimeout) {
    clearTimeout(mapCheckTimeout)
  }
})
</script>

<style scoped>
.misc {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  background: var(--bg-secondary);
  padding: 4rem 2rem;
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
  margin-bottom: 0;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Section Backgrounds */
.blog-section {
  background: var(--bg-primary);
  padding: 4rem 2rem;
}

.interests-section {
  background: var(--bg-secondary);
  padding: 4rem 2rem;
}

.visitor-map {
  background: var(--bg-primary);
  padding: 4rem 2rem 2rem;
}

.section-title {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent-primary);
}

.subsection-title {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-top: 2rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.subsection-title:first-of-type {
  margin-top: 0;
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
  margin-bottom: 3rem;
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
.loading-state,
.no-posts {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.blog-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  min-height: 280px;
}

.blog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.blog-card-content {
  flex: 1;
}

.blog-date {
  font-size: 0.9rem;
  color: var(--text-tertiary);
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.blog-card h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.blog-excerpt {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 500;
}

.read-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: 1rem;
  margin-top: 1rem;
  transition: color 0.3s ease;
}

.blog-card:hover .read-more {
  color: var(--link-hover);
}

/* Interests Section */
.interests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.interest-card {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashed-strike {
  text-decoration: line-through;
  text-decoration-style: dashed;
}

.interest-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.interest-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.interest-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}


/* Visitor Map Section */
.map-container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.map-container a {
  display: block;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.map-container a:hover {
  transform: scale(1.02);
  opacity: 0.9;
}

.map-container img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--border-color);
}

.map-error {
  text-align: center;
  padding: 2rem;
  background: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  max-width: 400px;
  margin: 0 auto;
}

.map-error p:first-child {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.error-hint {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section,
  .blog-section,
  .interests-section {
    padding: 2rem 1rem;
  }

  .visitor-map {
    padding: 2rem 1rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .albums-grid,
  .blog-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .interests-grid {
    grid-template-columns: 1fr;
  }

}
</style>
