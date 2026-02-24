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
              <div class="blog-card-header">
                <div class="blog-date">{{ formatDate(post.published_at || post.created_at) }}</div>
                <div v-if="post.reading_time" class="blog-reading-time">{{ post.reading_time }} min</div>
              </div>
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
    <section class="beyond-cs">
      <div class="container">
        <h2 class="section-title">Beyond Computer Science</h2>
        <p class="section-intro">When I'm not coding, you'll find me staying active by lifting or playing volleyball, playing games for fun, or exploring the world.</p>
        
        <!-- Interests - Compact Grid -->
        <div class="interests-section">
          <h3 class="subsection-title">What I Love</h3>
          <div class="interests-grid">
            <div class="interest-item">
              <span class="interest-icon">🏐</span>
              <div class="interest-text">
                <h4>Volleyball</h4>
                <p>Strategy and teamwork on the court</p>
              </div>
            </div>

            <div class="interest-item">
              <span class="interest-icon">💪</span>
              <div class="interest-text">
                <h4>Powerlifting</h4>
                <p>Building strength, one rep at a time</p>
              </div>
            </div>

            <div class="interest-item">
              <span class="interest-icon">🎮</span>
              <div class="interest-text">
                <h4>Gaming</h4>
                <p>Dota 2, Valorant, and anime games</p>
              </div>
            </div>

            <div class="interest-item">
              <span class="interest-icon">📚</span>
              <div class="interest-text">
                <h4>Learning</h4>
                <p>Always exploring new technologies</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Photo Albums - Featured Section -->
        <div class="albums-section">
          <h3 class="subsection-title">Photo Albums</h3>
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
                    <span class="album-subtitle">Some photos from Philippines, USA, Japan, and many more</span>
                    <span class="view-link">View Album →</span>
                  </div>
                </div>
              </div>
            </router-link>

            <!-- Me Album -->
            <router-link to="/misc/professional" class="album-card">
              <div class="album-image">
                <OptimizedImage
                  src="/assets/photos/professional_1.jpg"
                  alt="Personal Moments"
                  size="md"
                />
                <div class="album-overlay">
                  <div class="overlay-content">
                    <span class="album-icon">👤</span>
                    <span class="album-title">Me</span>
                    <span class="album-subtitle">Personal moments</span>
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

      </div>
    </section>

    <!-- Visitor Map -->
    <section class="visitor-map">
      <div class="container">
        <h2 class="section-title">Visitors</h2>
        <div class="map-container">
          <a href="https://clustrmaps.com/site/1c8ov" title="ClustrMaps" target="_blank" rel="noopener noreferrer">
            <img
              src="https://www.clustrmaps.com/map_v2.png?d=bUwnH32XrcZZm4BmWIy-rlCG47vK_-JRxDo71nilFs8&cl=ffffff"
              alt="Visitor Map"
            />
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, computed } from 'vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import { useBlog } from '../composables/useBlog'

const { posts, loading, fetchPosts } = useBlog()

const recentPosts = computed(() => posts.value.slice(0, 3))

const formatDate = (date) => {
  if (!date) return 'Recent'
  try {
    const d = new Date(date)
    if (isNaN(d.getTime())) return 'Recent'
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch (error) {
    return 'Recent'
  }
}

onMounted(() => {
  fetchPosts()
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

.beyond-cs {
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

.section-intro {
  text-align: center;
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 3rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.subsection-title {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  font-weight: 600;
}

/* Photo Albums Section */
.albums-section {
  margin-bottom: 4rem;
}

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
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

/* Interests Section */
.interests-section {
  margin-top: 3rem;
}

.interests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.interest-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--bg-card);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px var(--shadow);
  transition: all 0.3s ease;
}

.interest-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px var(--shadow);
  border-color: var(--accent-primary);
}

.interest-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: var(--bg-tertiary);
  border-radius: 12px;
}

.interest-text h4 {
  font-size: 1.2rem;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.interest-text p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
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

.blog-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  gap: 1rem;
}

.blog-date {
  font-size: 0.9rem;
  color: var(--text-tertiary);
  font-weight: 500;
}

.blog-reading-time {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
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

/* Responsive */
@media (max-width: 768px) {
  .hero-section,
  .blog-section,
  .beyond-cs {
    padding: 2rem 1rem;
  }

  .visitor-map {
    padding: 2rem 1rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .section-intro {
    font-size: 1rem;
    margin-bottom: 2rem;
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

  .interests-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .interest-item {
    padding: 1.25rem;
    gap: 1rem;
  }

  .interest-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
  }

  .interest-text h4 {
    font-size: 1.1rem;
  }

  .interest-text p {
    font-size: 0.9rem;
  }

  .blog-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
