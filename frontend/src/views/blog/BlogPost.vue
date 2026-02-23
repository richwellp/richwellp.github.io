<template>
  <div class="blog-post">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading post...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-state">
        <h1>Post Not Found</h1>
        <p>{{ error }}</p>
        <router-link to="/misc/blog" class="back-button">← Back to Blog</router-link>
      </div>

      <!-- Post Content -->
      <article v-if="post && !loading">
        <div class="post-header">
          <router-link to="/misc/blog" class="back-link">← Back to Blog</router-link>
          <div class="post-meta">
            <span class="post-date">{{ formatDate(post.date) }}</span>
            <span v-if="post.author" class="post-author">by {{ post.author }}</span>
          </div>
          <h1>{{ post.title }}</h1>
          <div v-if="post.tags && post.tags.length > 0" class="post-tags">
            <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>

        <div class="post-content" v-html="renderedContent"></div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useBlog } from '../../composables/useBlog'
import MarkdownIt from 'markdown-it'

const route = useRoute()
const { getPostBySlug } = useBlog()

const post = ref(null)
const loading = ref(true)
const error = ref(null)

const md = new MarkdownIt({
  html: false,  // Prevent HTML injection - blog posts are pure markdown
  linkify: true,
  typographer: true
})

const renderedContent = computed(() => {
  if (!post.value || !post.value.content) return ''
  return md.render(post.value.content)
})

onMounted(async () => {
  try {
    const slug = route.params.slug
    post.value = await getPostBySlug(slug)
    loading.value = false
  } catch (err) {
    error.value = err.message
    loading.value = false
  }
})

const formatDate = (date) => {
  const d = new Date(date)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.blog-post {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* Loading & Error */
.loading,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.error-state h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.error-state p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.back-button {
  display: inline-block;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  transition: all 0.3s ease;
}

.back-button:hover {
  color: var(--link-hover);
  border-color: var(--accent-primary);
  background: var(--bg-hover);
}

/* Post Header */
.post-header {
  margin-bottom: 3rem;
}

.back-link {
  display: inline-block;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 2rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--link-hover);
}

.post-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.post-date {
  color: var(--accent-primary);
  font-weight: 600;
}

.post-author {
  color: var(--text-secondary);
}

.post-header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.2;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tag {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Post Content (Markdown Styles) */
.post-content {
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.8;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  color: var(--text-primary);
  margin-top: 2rem;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.post-content :deep(h2) {
  font-size: 2rem;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.post-content :deep(h3) {
  font-size: 1.5rem;
}

.post-content :deep(p) {
  margin-bottom: 1.5rem;
}

.post-content :deep(a) {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 500;
}

.post-content :deep(a:hover) {
  color: var(--link-hover);
  text-decoration: underline;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 1.5rem;
  padding-left: 2rem;
}

.post-content :deep(li) {
  margin-bottom: 0.5rem;
}

.post-content :deep(code) {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.95em;
}

.post-content :deep(pre) {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.post-content :deep(pre code) {
  background: none;
  color: var(--text-primary);
  padding: 0;
}

.post-content :deep(blockquote) {
  border-left: 4px solid var(--accent-primary);
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  color: var(--text-secondary);
  font-style: italic;
}

.post-content :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 2rem 0;
  box-shadow: 0 4px 20px var(--shadow);
}

.post-content :deep(hr) {
  border: none;
  border-top: 2px solid var(--border-color);
  margin: 3rem 0;
}

/* Responsive */
@media (max-width: 768px) {
  .blog-post {
    padding: 2rem 1rem;
  }

  .post-header h1 {
    font-size: 2rem;
  }

  .post-content {
    font-size: 1rem;
  }

  .post-content :deep(h2) {
    font-size: 1.5rem;
  }

  .post-content :deep(h3) {
    font-size: 1.3rem;
  }

  .post-content :deep(pre) {
    padding: 1rem;
  }
}
</style>
