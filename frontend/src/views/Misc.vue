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

          <!-- Album Cover Slideshow -->
          <div v-else-if="featuredAlbums.length > 0" class="album-slideshow">
            <router-link
              v-if="currentAlbum"
              :to="`/misc/albums/${currentAlbum.slug}`"
              class="slideshow-slide"
            >
              <!-- Photo Cover -->
              <img
                v-if="currentAlbum.cover_photo && !isVideoCover(currentAlbum.cover_photo)"
                :src="currentAlbum.cover_photo"
                :alt="`${currentAlbum.name} Album`"
                class="slideshow-media"
              />
              <!-- Video Cover -->
              <video
                v-else-if="currentAlbum.cover_photo && isVideoCover(currentAlbum.cover_photo)"
                ref="videoPlayer"
                :src="currentAlbum.cover_photo"
                muted
                autoplay
                playsinline
                preload="metadata"
                class="slideshow-media"
                @ended="nextSlide"
              />
              <!-- Placeholder if no cover -->
              <div v-else class="slideshow-placeholder">
                <span class="placeholder-text">{{ currentAlbum.name }}</span>
              </div>

              <!-- Album Info Overlay -->
              <div class="slideshow-overlay">
                <div class="slideshow-info">
                  <h3 class="slideshow-title">{{ currentAlbum.name }}</h3>
                  <p class="slideshow-subtitle">{{ currentAlbum.subtitle }}</p>
                  <span class="slideshow-link">View Album →</span>
                </div>
              </div>
            </router-link>

            <!-- Slideshow Controls -->
            <div class="slideshow-controls">
              <button @click="prevSlide" class="control-btn" aria-label="Previous album">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
              </button>
              <div class="slideshow-dots">
                <button
                  v-for="(album, index) in featuredAlbums"
                  :key="album.id"
                  @click="goToSlide(index)"
                  :class="['dot', { active: currentSlideIndex === index }]"
                  :aria-label="`Go to ${album.name}`"
                ></button>
              </div>
              <button @click="nextSlide" class="control-btn" aria-label="Next album">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </button>
            </div>
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
import { onMounted, onBeforeUnmount, computed, ref, watch } from 'vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import { useBlog } from '../composables/useBlog'
import { useAlbums } from '../composables/useAlbums'

const { posts, loading, fetchPosts } = useBlog()
const { albums, loading: albumsLoading, fetchAlbums } = useAlbums()

const recentPosts = computed(() => posts.value.slice(0, 3))
const featuredAlbums = computed(() => albums.value.slice(0, 3))

// Album slideshow state
const currentSlideIndex = ref(0)
const videoPlayer = ref(null)
let slideTimer = null

const PHOTO_DURATION = 5000 // 5 seconds for photos

// Current album being displayed
const currentAlbum = computed(() => {
  if (featuredAlbums.value.length === 0) return null
  return featuredAlbums.value[currentSlideIndex.value]
})

// Navigate to next slide
const nextSlide = () => {
  if (featuredAlbums.value.length === 0) return
  currentSlideIndex.value = (currentSlideIndex.value + 1) % featuredAlbums.value.length
}

// Navigate to previous slide
const prevSlide = () => {
  if (featuredAlbums.value.length === 0) return
  currentSlideIndex.value = currentSlideIndex.value === 0
    ? featuredAlbums.value.length - 1
    : currentSlideIndex.value - 1
}

// Go to specific slide
const goToSlide = (index) => {
  currentSlideIndex.value = index
}

// Start timer for photo slides (videos handle themselves with @ended)
const startPhotoTimer = () => {
  clearTimeout(slideTimer)

  const album = currentAlbum.value
  if (!album || !album.cover_photo || isVideoCover(album.cover_photo)) {
    return // Don't set timer for videos or missing covers
  }

  slideTimer = setTimeout(() => {
    nextSlide()
  }, PHOTO_DURATION)
}

// Watch for slide changes to reset timer
watch(currentSlideIndex, () => {
  startPhotoTimer()
}, { immediate: true })

// Watch for albums loading
watch(featuredAlbums, (newAlbums) => {
  if (newAlbums.length > 0) {
    startPhotoTimer()
  }
})

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

// Check if cover photo URL is a video
const isVideoCover = (url) => {
  if (!url) return false
  const urlLower = url.toLowerCase()
  // Check for video extensions or video content-type in URL
  return /\.(mp4|mov|webm|avi|mkv)(\?|#|$)/i.test(urlLower) || urlLower.includes('video/')
}

onMounted(() => {
  fetchPosts()
  fetchAlbums()
})

onBeforeUnmount(() => {
  // Clean up slideshow timer
  clearTimeout(slideTimer)
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

.section-header .subsection-title {
  margin-bottom: 0;
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

/* Album Cover Slideshow */
.album-slideshow {
  position: relative;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px var(--shadow);
}

.slideshow-slide {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
  background: var(--bg-tertiary);
}

.slideshow-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.slideshow-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-size: 2rem;
  font-weight: 600;
}

.empty-albums {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}


/* Slideshow Overlay */
.slideshow-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.7));
  display: flex;
  align-items: flex-end;
  padding: 2rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.slideshow-slide:hover .slideshow-overlay {
  opacity: 1;
}

.slideshow-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: white;
}

.slideshow-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.slideshow-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0 0 0.5rem 0;
}

.slideshow-link {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-primary);
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease 0.1s;
}

.slideshow-slide:hover .slideshow-link {
  opacity: 1;
  transform: translateY(0);
}

/* Slideshow Controls */
.slideshow-controls {
  position: absolute;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-primary);
}

.control-btn:hover {
  background: white;
  transform: scale(1.1);
}

.slideshow-dots {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.dot.active {
  background: white;
  transform: scale(1.3);
}

.dot:hover {
  background: rgba(255, 255, 255, 0.8);
}


/* Interests Section */
.interests-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: center;
}

.interest-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--bg-card);
  color: var(--text-primary);
  border-radius: 50px;
  border: 1px solid var(--border-color);
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px var(--shadow);
}

.interest-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
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
.visitor-intro {
  text-align: center;
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.map-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  width: 100%;
}

.map-container a {
  display: block;
  max-width: 100%;
  transition: opacity 0.2s ease;
}

.map-container a:hover {
  opacity: 0.95;
}

.map-container img {
  max-width: 100%;
  height: auto;
  display: block;
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
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

  .visitor-intro {
    font-size: 1rem;
    padding: 0 1rem;
  }

  .map-container a {
    max-width: 100%;
    padding: 0 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .section-intro {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .album-slideshow {
    aspect-ratio: 4 / 3;
  }

  .slideshow-overlay {
    padding: 1.5rem;
  }

  .slideshow-title {
    font-size: 1.5rem;
  }

  .slideshow-subtitle {
    font-size: 0.85rem;
  }

  .slideshow-controls {
    bottom: 1rem;
  }

  .control-btn {
    width: 35px;
    height: 35px;
  }

  .interests-tags {
    gap: 0.75rem;
  }

  .interest-tag {
    padding: 0.6rem 1.25rem;
    font-size: 0.95rem;
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
