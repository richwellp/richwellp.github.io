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
        <p class="section-intro">When I'm not coding, you'll find me staying active, gaming, or exploring the world.</p>

        <!-- Interests - Simple Tags -->
        <div class="interests-tags">
          <span class="interest-tag">🏐 Volleyball</span>
          <span class="interest-tag">💪 Powerlifting</span>
          <span class="interest-tag">🎮 Gaming</span>
          <span class="interest-tag">📚 Learning</span>
        </div>

        <!-- Photo Albums - Featured Section -->
        <div class="albums-section">
          <div class="section-header">
            <h3 class="subsection-title">Photo Albums</h3>
            <router-link to="/misc/albums" class="view-all-link">View All →</router-link>
          </div>

          <!-- Loading State -->
          <div v-if="albumsLoading" class="loading-state">
            <p>Loading albums...</p>
          </div>

          <!-- Album Cards with Individual Slideshows -->
          <div v-else-if="featuredAlbums.length > 0" class="albums-grid">
            <AlbumCoverSlideshow
              v-for="album in featuredAlbums"
              :key="album.id"
              :album="album"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="empty-albums">
            <p>No albums yet</p>
          </div>
        </div>

      </div>
    </section>

    <!-- Visitor Map -->
    <section class="visitor-map">
      <div class="container">
        <h2 class="section-title">Visitors</h2>
        <p class="visitor-intro">
          Thanks for visiting! See where other visitors have connected from around the world.
        </p>
        <div class="map-container">
          <!-- Simple ClustrMaps image - large native size for crisp display -->
          <a href='https://clustrmaps.com/site/1c0c0' title='Visit tracker'>
            <img src='https://clustrmaps.com/map_v2.png?cl=ffffff&w=800&t=tt&d=bUwnH32XrcZZm4BmWIy-rlCG47vK_-JRxDo71nilFs8&co=2d78ad&ct=ffffff' alt='Visitor map' />
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
import AlbumCoverSlideshow from '../components/AlbumCoverSlideshow.vue'
import { useBlog } from '../composables/useBlog'
import { useAlbums } from '../composables/useAlbums'

const { posts, loading, fetchPosts } = useBlog()
const { albums, loading: albumsLoading, fetchAlbums } = useAlbums()

const recentPosts = computed(() => posts.value.slice(0, 3))
const featuredAlbums = computed(() => albums.value.slice(0, 3))

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
  fetchAlbums()
})
</script>

<style scoped>
.misc {
  min-height: 100vh;
  background: var(--bg-primary);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  padding: 5rem 2rem;
  position: relative;
}

.hero-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
  opacity: 0.5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: clamp(2.25rem, 4vw, 3rem);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  text-align: center;
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.025em;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.1s forwards;
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

.page-intro {
  text-align: center;
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 0;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
}

/* Section Backgrounds */
.blog-section {
  background: var(--bg-primary);
  padding: 5rem 2rem;
}

.beyond-cs {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  padding: 5rem 2rem;
  position: relative;
}

.beyond-cs::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
  opacity: 0.5;
}

.visitor-map {
  background: var(--bg-primary);
  padding: 5rem 2rem 3rem;
}

.section-title {
  font-size: clamp(1.875rem, 3vw, 2.25rem);
  color: var(--text-primary);
  margin-bottom: 2.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid var(--accent-primary);
  font-weight: 700;
  letter-spacing: -0.02em;
  position: relative;
  width: fit-content;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 40%;
  height: 3px;
  background: var(--accent-secondary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header .subsection-title {
  margin-bottom: 0;
}

.view-all-link {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
}

.view-all-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
  text-decoration-color: var(--accent-primary);
  text-decoration-thickness: 2px;
  text-underline-offset: 3px;
  transform: translateX(3px);
}

.section-description {
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  margin-bottom: 2.5rem;
  line-height: 1.65;
  font-weight: 400;
}

.section-intro {
  text-align: center;
  color: var(--text-secondary);
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  line-height: 1.7;
  margin-bottom: 3.5rem;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.subsection-title {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin-bottom: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Photo Albums Section */
.albums-section {
  margin-bottom: 4.5rem;
  margin-top: 3rem;
}

/* Album Cards Grid */
.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.3s forwards;
}

.empty-albums {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  font-weight: 400;
}

/* Interests Section */
.interests-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  margin-top: 2.5rem;
  margin-bottom: 3.5rem;
  justify-content: center;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.3s forwards;
}

.interest-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.875rem 1.75rem;
  background: var(--bg-card);
  color: var(--text-primary);
  border-radius: 50px;
  border: 1.5px solid var(--border-color);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-weight: 600;
  letter-spacing: -0.01em;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: default;
}

.interest-tag:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  border-color: var(--accent-primary);
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  color: var(--bg-primary);
}

/* Blog Section */
.loading-state,
.no-posts {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  font-weight: 400;
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 2.5rem;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.3s forwards;
}

.blog-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.25rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06),
              0 1px 3px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 300px;
  position: relative;
  overflow: hidden;
}

.blog-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.blog-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12),
              0 6px 12px rgba(0, 0, 0, 0.08);
  border-color: var(--accent-primary)60;
}

.blog-card:hover::before {
  opacity: 1;
}

.blog-card-content {
  flex: 1;
}

.blog-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.blog-date {
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
  color: var(--text-tertiary);
  font-weight: 600;
  letter-spacing: -0.01em;
}

.blog-reading-time {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: clamp(0.8125rem, 1vw, 0.875rem);
  font-weight: 500;
  white-space: nowrap;
  border: 1px solid var(--border-color);
}

.blog-card h3 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin-bottom: 1.125rem;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.02em;
  transition: color 0.3s ease;
}

.blog-card:hover h3 {
  color: var(--accent-primary);
}

.blog-excerpt {
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.65;
  margin-bottom: 1.25rem;
  font-weight: 400;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-top: 1.25rem;
}

.tag {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.375rem 0.875rem;
  border-radius: 16px;
  font-size: clamp(0.8125rem, 1vw, 0.875rem);
  font-weight: 500;
  letter-spacing: -0.01em;
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tag:hover {
  background: var(--accent-primary);
  color: var(--bg-card);
  border-color: var(--accent-primary);
}

.read-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  margin-top: 1.25rem;
  letter-spacing: -0.01em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.blog-card:hover .read-more {
  color: var(--accent-hover);
  transform: translateX(3px);
}

/* Visitor Map Section */
.visitor-intro {
  text-align: center;
  color: var(--text-secondary);
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  line-height: 1.7;
  margin-bottom: 2.5rem;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.map-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2.5rem;
  width: 100%;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.3s forwards;
}

.map-container a {
  display: block;
  max-width: 100%;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.map-container a:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.map-container img {
  max-width: 100%;
  height: auto;
  display: block;
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
  border-radius: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    padding: 3.5rem 1.5rem;
  }

  .blog-section {
    padding: 3.5rem 1.5rem;
  }

  .beyond-cs {
    padding: 3.5rem 1.5rem;
  }

  .visitor-map {
    padding: 3.5rem 1.5rem 2rem;
  }

  .visitor-intro {
    margin-bottom: 2rem;
    padding: 0 1rem;
  }

  .map-container a {
    max-width: 100%;
    padding: 0 1rem;
  }

  .section-intro {
    margin-bottom: 2.5rem;
  }

  .albums-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .interests-tags {
    gap: 1rem;
  }

  .interest-tag {
    padding: 0.75rem 1.5rem;
  }

  .blog-grid {
    grid-template-columns: 1fr;
    gap: 1.75rem;
  }

  .blog-card {
    padding: 1.875rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 3rem 1.25rem;
  }

  .blog-section {
    padding: 3rem 1.25rem;
  }

  .beyond-cs {
    padding: 3rem 1.25rem;
  }

  .visitor-map {
    padding: 3rem 1.25rem 1.5rem;
  }

  .blog-card {
    padding: 1.5rem;
  }

  .interest-tag {
    padding: 0.625rem 1.25rem;
  }
}
</style>
