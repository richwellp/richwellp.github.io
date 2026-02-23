<template>
  <div class="blog-list">
    <div class="container">
      <!-- Header -->
      <div class="blog-header">
        <router-link to="/misc" class="back-link">← Back to Misc</router-link>
        <h1>📝 Blog</h1>
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
            <div class="post-date">{{ formatDate(post.date) }}</div>
            <div v-if="post.readingTime" class="reading-time">{{ post.readingTime }} min</div>
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
import { onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useBlog } from '../../composables/useBlog'
import { injectStructuredData, generateBlogListSchema } from '../../composables/useStructuredData'

const { posts, loading, error, fetchPosts } = useBlog()

onMounted(() => {
  fetchPosts()
})

// Inject blog list schema when posts are loaded
watch(
  () => posts.value,
  (newPosts) => {
    if (newPosts && newPosts.length > 0) {
      const blogListSchema = generateBlogListSchema(newPosts)
      injectStructuredData(blogListSchema, 'blog-list-schema')
    }
  }
)

const formatDate = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.blog-list {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.blog-header {
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

.blog-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 800px;
}

/* Loading & Error States */
.loading,
.error {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.error {
  color: #ef4444;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
}

.empty-state h2 {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.empty-state > p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.info-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.info-card h3 {
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.info-card ul {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.info-card li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.hint {
  background: var(--bg-tertiary);
  padding: 1rem;
  border-radius: 6px;
  border-left: 3px solid var(--accent-primary);
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.hint code {
  background: var(--bg-secondary);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-family: monospace;
  color: var(--accent-primary);
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
  padding: 2rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-decoration: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  display: flex;
  flex-direction: column;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.post-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  gap: 1rem;
}

.post-date {
  color: var(--accent-primary);
  font-size: 0.9rem;
  font-weight: 600;
}

.reading-time {
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

.post-card h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.post-excerpt {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  flex: 1;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
}

.read-more {
  color: var(--link-color);
  font-weight: 600;
  font-size: 0.95rem;
}

.post-card:hover .read-more {
  color: var(--link-hover);
}

/* Responsive */
@media (max-width: 768px) {
  .blog-list {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .posts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
