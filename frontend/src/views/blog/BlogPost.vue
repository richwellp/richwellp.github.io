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
      <article v-if="post && !loading" class="article-wrapper">
        <div class="article-main">
          <div class="post-header">
            <router-link to="/misc/blog" class="back-link">← Back to Blog</router-link>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.published_at || post.created_at) }}</span>
              <span v-if="post.author" class="post-author">by {{ post.author }}</span>
              <span v-if="post.reading_time" class="reading-time">{{ post.reading_time }} min read</span>
            </div>
            <h1>{{ post.title }}</h1>
            <div v-if="post.tags && post.tags.length > 0" class="post-tags">
              <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>

          <TableOfContents
            v-if="post.headings && post.headings.length > 0"
            :headings="post.headings"
            :post-content="post.content"
          />

          <div class="post-content" v-html="renderedContent"></div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useBlog } from '../../composables/useBlog'
import { injectStructuredData, generateBlogPostSchema } from '../../composables/useStructuredData'
import { sanitizeHtml } from '../../composables/useSanitizer'
import TableOfContents from '../../components/TableOfContents.vue'
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

// Custom renderer: Convert video files from <img> to <video>
const defaultImageRenderer = md.renderer.rules.image
md.renderer.rules.image = (tokens, idx, options, env, self) => {
  const token = tokens[idx]
  const src = token.attrGet('src')
  const alt = token.content

  // Check if source is a video file
  if (src && /\.(mp4|webm|ogg|mov)$/i.test(src)) {
    return `<video controls style="max-width: 100%; border-radius: 8px; margin: 2rem 0;">
      <source src="${src}" type="video/${src.split('.').pop().toLowerCase()}">
      ${alt}
    </video>`
  }

  // Default image rendering
  return defaultImageRenderer(tokens, idx, options, env, self)
}

const renderedContent = computed(() => {
  if (!post.value || !post.value.content) return ''
  const rendered = md.render(post.value.content)
  // Sanitize markdown output to prevent XSS attacks
  return sanitizeHtml(rendered, {
    // Allow video attributes and safe inline styles
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'id', 'controls', 'type', 'style'],
    FORBID_ATTR: ['onerror', 'onclick']
  })
})

onMounted(async () => {
  try {
    const slug = route.params.slug
    post.value = await getPostBySlug(slug)

    // Inject BlogPosting schema when post is loaded
    if (post.value) {
      const blogPostSchema = generateBlogPostSchema(post.value)
      injectStructuredData(blogPostSchema, 'blog-post-schema')
    }

    loading.value = false
  } catch (err) {
    error.value = err.message
    loading.value = false
  }
})

const formatDate = (date) => {
  if (!date) return 'No date'
  const d = new Date(date)
  if (isNaN(d.getTime())) return 'Invalid date'
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped>
.blog-post {
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1400px;
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

.article-wrapper {
  display: flex;
  gap: 3rem;
  position: relative;
}

.article-main {
  flex: 1;
  min-width: 0;
  max-width: 900px;
}

/* Loading & Error */
.loading,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading {
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  font-weight: 400;
}

.error-state h1 {
  font-size: clamp(2.25rem, 4vw, 3rem);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.025em;
}

.error-state p {
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  line-height: 1.7;
  margin-bottom: 2.5rem;
  font-weight: 400;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  padding: 1rem 2rem;
  border: 1.5px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.back-button:hover {
  color: var(--accent-hover);
  border-color: var(--accent-primary);
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Post Header */
.post-header {
  margin-bottom: 4rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid var(--border-color);
  position: relative;
}

.post-header::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100px;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  margin-bottom: 2rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
}

.back-link:hover {
  color: var(--accent-hover);
  transform: translateX(-3px);
}

.post-meta {
  display: flex;
  gap: 1.75rem;
  align-items: center;
  margin-bottom: 1.5rem;
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  flex-wrap: wrap;
}

.post-date {
  color: var(--accent-primary);
  font-weight: 600;
  letter-spacing: -0.01em;
}

.post-author {
  color: var(--text-secondary);
  font-weight: 500;
}

.reading-time {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-tertiary);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
  font-weight: 500;
  color: var(--accent-primary);
  border: 1px solid var(--border-color);
}

.post-header h1 {
  font-size: clamp(2rem, 4vw, 2.75rem);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.tag {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 16px;
  font-size: clamp(0.875rem, 1vw, 0.9375rem);
  font-weight: 500;
  letter-spacing: -0.01em;
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tag:hover {
  background: var(--accent-primary);
  color: var(--bg-card);
  border-color: var(--accent-primary);
  transform: translateY(-2px);
}

/* Post Content (Markdown Styles) */
.post-content {
  color: var(--text-secondary);
  font-size: clamp(1.0625rem, 1.3vw, 1.125rem);
  line-height: 1.8;
  font-weight: 400;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  color: var(--text-primary);
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
  line-height: 1.3;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.post-content :deep(h2) {
  font-size: clamp(1.75rem, 2.5vw, 2.125rem);
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.75rem;
  position: relative;
}

.post-content :deep(h2)::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
}

.post-content :deep(h3) {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
}

.post-content :deep(h4) {
  font-size: clamp(1.1875rem, 1.5vw, 1.3125rem);
}

.post-content :deep(p) {
  margin-bottom: 1.75rem;
}

.post-content :deep(a) {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-bottom: 1px solid transparent;
}

.post-content :deep(a:hover) {
  color: var(--accent-hover);
  border-bottom-color: var(--accent-primary);
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 1.75rem;
  padding-left: 2rem;
}

.post-content :deep(li) {
  margin-bottom: 0.75rem;
  line-height: 1.7;
}

.post-content :deep(code) {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.25rem 0.625rem;
  border-radius: 5px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9em;
  font-weight: 600;
  border: 1px solid var(--border-color);
}

.post-content :deep(pre) {
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  padding: 1.75rem;
  overflow-x: auto;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.post-content :deep(pre code) {
  background: none;
  color: var(--text-primary);
  padding: 0;
  border: none;
  font-size: 0.95em;
}

.post-content :deep(blockquote) {
  border-left: 5px solid var(--accent-primary);
  padding-left: 1.75rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  margin: 2rem 0;
  color: var(--text-secondary);
  font-style: italic;
  background: linear-gradient(90deg, rgba(200, 108, 74, 0.05), transparent);
  border-radius: 0 8px 8px 0;
  font-size: 1.05em;
}

.post-content :deep(img) {
  max-width: 100%;
  border-radius: 10px;
  margin: 2.5rem 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12),
              0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border-color);
}

.post-content :deep(hr) {
  border: none;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
  margin: 3.5rem 0;
}

/* Responsive */
@media (max-width: 1400px) {
  .article-wrapper {
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .blog-post {
    padding: 3.5rem 1.5rem;
  }

  .article-wrapper {
    flex-direction: column;
    gap: 2rem;
  }

  .article-main {
    max-width: 100%;
  }

  .post-header {
    margin-bottom: 3rem;
    padding-bottom: 1.5rem;
  }

  .back-link {
    margin-bottom: 1.5rem;
  }

  .post-content :deep(pre) {
    padding: 1.25rem;
  }

  .post-meta {
    gap: 1.25rem;
  }

  .post-content :deep(blockquote) {
    padding-left: 1.25rem;
    margin: 1.5rem 0;
  }

  .post-content :deep(img) {
    margin: 2rem 0;
  }
}

@media (max-width: 480px) {
  .blog-post {
    padding: 3rem 1.25rem;
  }

  .post-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.25rem;
  }

  .back-link {
    margin-bottom: 1.25rem;
  }

  .post-meta {
    gap: 1rem;
  }

  .post-content :deep(pre) {
    padding: 1rem;
    font-size: 0.875rem;
  }

  .post-content :deep(ul),
  .post-content :deep(ol) {
    padding-left: 1.5rem;
  }

  .post-tags {
    gap: 0.5rem;
  }

  .tag {
    padding: 0.375rem 0.875rem;
  }
}
</style>
