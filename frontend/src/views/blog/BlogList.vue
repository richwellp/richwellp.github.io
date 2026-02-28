<template>
  <div class="blog-list">
    <div class="container">
      <!-- Header -->
      <div class="blog-header">
        <router-link to="/misc" class="back-link">← Back to Misc</router-link>
        <h1>Blog</h1>
        <p class="blog-subtitle">
          Thoughts, reflections, and technical write-ups about AI, software engineering, and
          personal experiences
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading posts...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>Error loading posts: {{ error }}</p>
      </div>

      <!-- Empty State (No Posts Yet) -->
      <div v-if="!loading && !error && posts.length === 0" class="empty-state">
        <div class="empty-icon">✍️</div>
        <h2>Error loading posts</h2>
        <p>There was an issue loading blog posts. Please check the browser console for details.</p>
      </div>

      <!-- Posts Grid -->
      <div v-if="posts.length > 0" class="posts-grid">
        <router-link
          v-for="post in posts"
          :key="post.slug"
          :to="`/misc/blog/${post.slug}`"
          class="post-card"
        >
          <div class="post-card-header">
            <div class="post-date">{{ formatDate(post.published_at || post.created_at) }}</div>
            <div v-if="post.reading_time" class="reading-time">{{ post.reading_time }} min</div>
          </div>
          <h2>{{ post.title }}</h2>
          <p class="post-excerpt">{{ post.excerpt }}</p>
          <div v-if="post.tags && post.tags.length > 0" class="post-tags">
            <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
          <span class="read-more">Read more →</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch, nextTick } from 'vue'
import { RouterLink } from 'vue-router'
import { useBlog } from '../../composables/useBlog'
import { injectStructuredData, generateBlogListSchema } from '../../composables/useStructuredData'

const { posts, loading, error, fetchPosts } = useBlog()

let cardObserver = null

const setupCardObserver = () => {
  if (cardObserver) cardObserver.disconnect()
  cardObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.dataset.idx || 0)
          entry.target.style.transitionDelay = `${idx * 0.12}s`
          entry.target.classList.add('visible')
          entry.target.addEventListener('transitionend', () => {
            entry.target.style.transitionDelay = '0s'
          }, { once: true })
          cardObserver.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  )
  document.querySelectorAll('.post-card').forEach((el, i) => {
    el.dataset.idx = i
    cardObserver.observe(el)
  })
}

onMounted(() => {
  fetchPosts()
})

// Inject schema + set up scroll-triggered reveals when posts load
watch(
  () => posts.value,
  async (newPosts) => {
    if (newPosts && newPosts.length > 0) {
      const blogListSchema = generateBlogListSchema(newPosts)
      injectStructuredData(blogListSchema, 'blog-list-schema')

      await nextTick()
      await nextTick()
      setupCardObserver()
    }
  }
)

onUnmounted(() => {
  cardObserver?.disconnect()
})

const formatDate = (date) => {
  if (!date) return 'No date'
  const d = new Date(date)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.blog-list {
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
.blog-header {
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
  margin-bottom: 2rem;
  font-weight: 800;
  letter-spacing: -0.035em;
  position: relative;
  padding-bottom: 1.25rem;
}

h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent-primary) 50%, transparent);
}

.blog-subtitle {
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 720px;
  font-weight: 400;
}

/* Loading & Error States */
.loading,
.error {
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 2rem;
  opacity: 0.7;
}

.empty-state h2 {
  font-size: clamp(1.75rem, 2.5vw, 2.125rem);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.empty-state > p {
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.info-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.25rem;
  max-width: 680px;
  margin: 0 auto;
  text-align: left;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3),
              0 1px 4px rgba(0, 0, 0, 0.18),
              0 0 0 1px rgba(129, 140, 248, 0.04);
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.info-card h3 {
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  font-size: clamp(1.25rem, 1.6vw, 1.375rem);
  font-weight: 700;
  letter-spacing: -0.02em;
}

.info-card ul {
  color: var(--text-secondary);
  margin-bottom: 1.75rem;
  padding-left: 1.75rem;
  line-height: 1.7;
}

.info-card li {
  margin-bottom: 0.75rem;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
}

.hint {
  background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
  padding: 1.25rem;
  border-radius: 8px;
  border-left: 4px solid var(--accent-primary);
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.65;
}

.hint code {
  background: var(--bg-primary);
  padding: 0.25rem 0.625rem;
  border-radius: 5px;
  font-family: 'Monaco', 'Menlo', monospace;
  color: var(--accent-primary);
  font-size: 0.9em;
  font-weight: 600;
  border: 1px solid var(--border-color);
}

/* Posts Grid */
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.post-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.25rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3),
              0 1px 4px rgba(0, 0, 0, 0.18);
  border: 1px solid var(--border-color);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(36px) scale(0.965);
  transition: opacity 0.65s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.65s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.post-card.visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.post-card::before {
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

.post-card.visible:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 56px rgba(0, 0, 0, 0.55),
              0 8px 20px rgba(0, 0, 0, 0.3),
              0 0 0 1px rgba(129, 140, 248, 0.08),
              0 0 40px rgba(129, 140, 248, 0.06);
  border-color: color-mix(in srgb, var(--accent-primary) 38%, transparent);
}

.post-card.visible:hover::before {
  opacity: 1;
}

.post-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.post-date {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--accent-secondary);
  font-weight: 500;
  letter-spacing: 0.01em;
  opacity: 0.9;
}

.reading-time {
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

.post-card h2 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin-bottom: 1.125rem;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.02em;
  transition: color 0.3s ease;
}

.post-card:hover h2 {
  color: var(--accent-primary);
}

.post-excerpt {
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.65;
  margin-bottom: 1.25rem;
  flex: 1;
  font-weight: 400;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-bottom: 1.25rem;
}

.tag {
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
  color: #05060f;
  border-color: var(--accent-primary);
}

.read-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  letter-spacing: -0.01em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.post-card:hover .read-more {
  color: var(--accent-hover);
  transform: translateX(3px);
}

/* Responsive */
@media (max-width: 768px) {
  .blog-list {
    padding: 3.5rem 1.5rem;
  }

  .blog-header {
    margin-bottom: 3rem;
  }

  .posts-grid {
    grid-template-columns: 1fr;
    gap: 1.75rem;
  }

  .post-card {
    padding: 1.875rem;
  }

  .info-card {
    padding: 1.875rem;
  }
}

@media (max-width: 480px) {
  .blog-list {
    padding: 3rem 1.25rem;
  }

  .blog-header {
    margin-bottom: 2.5rem;
  }

  .post-card {
    padding: 1.5rem;
  }

  .info-card {
    padding: 1.5rem;
  }

  .empty-state {
    padding: 3rem 1rem;
  }
}
</style>
