<template>
  <div class="post-editor">
    <div class="editor-container">
      <!-- Header -->
      <div class="editor-header">
        <button @click="goBack" class="back-btn">← Back</button>
        <h1>{{ isEditMode ? 'Edit Post' : 'New Post' }}</h1>
      </div>

      <!-- Success Message -->
      <div v-if="saveStatus === 'success'" class="status-message success">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <p>Post saved successfully!</p>
      </div>

      <!-- Error Message -->
      <div v-if="saveStatus === 'error'" class="status-message error">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <p>{{ errorMessage }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>{{ isEditMode ? 'Loading post...' : 'Preparing editor...' }}</p>
      </div>

      <!-- Editor Form -->
      <form v-else @submit.prevent="handleSubmit" class="editor-form">
        <!-- Basic Info -->
        <div class="form-section">
          <h2>Post Details</h2>

          <div class="form-group">
            <label for="title">Title *</label>
            <input
              type="text"
              id="title"
              v-model="formData.title"
              required
              placeholder="Enter post title"
              :disabled="isSaving"
            />
          </div>

          <div class="form-group">
            <label for="slug">Slug *</label>
            <input
              type="text"
              id="slug"
              v-model="formData.slug"
              required
              placeholder="post-url-slug"
              :disabled="isSaving || isEditMode"
              pattern="[a-z0-9-]+"
              title="Only lowercase letters, numbers, and hyphens"
            />
            <small class="form-hint">
              {{ isEditMode ? 'Slug cannot be changed after creation' : 'URL-friendly identifier (lowercase, hyphens only)' }}
            </small>
          </div>

          <div class="form-group">
            <label for="excerpt">Excerpt</label>
            <textarea
              id="excerpt"
              v-model="formData.excerpt"
              rows="3"
              placeholder="Brief description of the post"
              :disabled="isSaving"
            ></textarea>
            <small class="form-hint">Shown in post listings and previews</small>
          </div>

          <div class="form-group">
            <label for="tags">Tags</label>
            <input
              type="text"
              id="tags"
              v-model="tagsInput"
              placeholder="javascript, web-development, tutorial"
              :disabled="isSaving"
            />
            <small class="form-hint">Comma-separated list of tags</small>
          </div>

          <div class="form-group">
            <label for="author">Author</label>
            <input
              type="text"
              id="author"
              v-model="formData.author"
              placeholder="Richwell Perez"
              :disabled="isSaving"
            />
          </div>

          <div class="form-group">
            <label for="created_at">Created Date</label>
            <input
              type="datetime-local"
              id="created_at"
              v-model="formData.created_at"
              :disabled="isSaving"
            />
            <small class="form-hint">When the post was created</small>
          </div>

          <div class="form-group">
            <label for="published_at">Published Date</label>
            <input
              type="datetime-local"
              id="published_at"
              v-model="formData.published_at"
              :disabled="isSaving"
            />
            <small class="form-hint">When the post was/will be published</small>
          </div>
        </div>

        <!-- Content Editor -->
        <div class="form-section">
          <h2>Content</h2>
          <MarkdownEditor v-model="formData.content" :placeholder="'Write your post content in markdown...'" />
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <div class="actions-left">
            <label class="publish-toggle">
              <input
                type="checkbox"
                v-model="formData.published"
                :disabled="isSaving"
              />
              <span>Publish immediately</span>
            </label>
          </div>

          <div class="actions-right">
            <button
              type="button"
              @click="goBack"
              class="btn btn-secondary"
              :disabled="isSaving"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isSaving || !isFormValid"
            >
              <span v-if="isSaving">Saving...</span>
              <span v-else>{{ isEditMode ? 'Update Post' : 'Create Post' }}</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminAuth } from '../../composables/useAdminAuth'
import { useAdminBlog } from '../../composables/useAdminBlog'
import MarkdownEditor from '../../components/MarkdownEditor.vue'

const router = useRouter()
const route = useRoute()
const { isAuthenticated } = useAdminAuth()
const { getAdminPost, createPost, updatePost } = useAdminBlog()

const isEditMode = computed(() => !!route.params.slug)
const isLoading = ref(false)
const isSaving = ref(false)
const saveStatus = ref(null)
const errorMessage = ref('')
const tagsInput = ref('')

const formData = reactive({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  tags: [],
  author: 'Richwell Perez',
  published: false,
  created_at: '',
  published_at: ''
})

// Check auth
if (!isAuthenticated.value) {
  router.push('/admin')
}

// Form validation
const isFormValid = computed(() => {
  return formData.title.trim() !== '' &&
         formData.slug.trim() !== '' &&
         formData.content.trim() !== ''
})

// Auto-generate slug from title (only for new posts)
watch(() => formData.title, (newTitle) => {
  if (!isEditMode.value && newTitle) {
    formData.slug = newTitle
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim()
  }
})

// Parse tags input to array
watch(() => tagsInput.value, (newTags) => {
  formData.tags = newTags
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag !== '')
})

// Load existing post for editing
const loadPost = async () => {
  if (!isEditMode.value) return

  isLoading.value = true
  saveStatus.value = null

  try {
    const post = await getAdminPost(route.params.slug)

    formData.title = post.title || ''
    formData.slug = post.slug || ''
    formData.excerpt = post.excerpt || ''
    formData.content = post.content || ''
    formData.tags = post.tags || []
    formData.author = post.author || 'Richwell Perez'
    formData.published = post.published || false

    // Convert ISO timestamps to datetime-local format (YYYY-MM-DDTHH:mm)
    if (post.created_at) {
      formData.created_at = new Date(post.created_at).toISOString().slice(0, 16)
    }
    if (post.published_at) {
      formData.published_at = new Date(post.published_at).toISOString().slice(0, 16)
    }

    // Set tags input
    tagsInput.value = (post.tags || []).join(', ')
  } catch (err) {
    console.error('Failed to load post:', err)
    errorMessage.value = 'Failed to load post. Please try again.'
    saveStatus.value = 'error'
  } finally {
    isLoading.value = false
  }
}

// Submit handler
const handleSubmit = async () => {
  if (!isFormValid.value) return

  isSaving.value = true
  saveStatus.value = null
  errorMessage.value = ''

  try {
    const postData = {
      title: formData.title.trim(),
      slug: formData.slug.trim(),
      excerpt: formData.excerpt.trim(),
      content: formData.content.trim(),
      tags: formData.tags,
      author: formData.author.trim() || 'Richwell Perez',
      published: formData.published
    }

    // Add dates if provided (convert to ISO format)
    if (formData.created_at) {
      postData.created_at = new Date(formData.created_at).toISOString()
    }
    if (formData.published_at) {
      postData.published_at = new Date(formData.published_at).toISOString()
    }

    if (isEditMode.value) {
      await updatePost(route.params.slug, postData)
    } else {
      await createPost(postData)
    }

    saveStatus.value = 'success'

    // Redirect after success
    setTimeout(() => {
      router.push('/admin')
    }, 1500)
  } catch (err) {
    console.error('Failed to save post:', err)
    errorMessage.value = err.message || 'Failed to save post. Please try again.'
    saveStatus.value = 'error'
  } finally {
    isSaving.value = false
  }
}

// Navigation
const goBack = () => {
  router.push('/admin')
}

// Auto-fill dates for new posts
const initializeNewPost = () => {
  // Set created_at to now
  const now = new Date()
  formData.created_at = now.toISOString().slice(0, 16)
}

// Watch published checkbox to auto-fill published_at
watch(() => formData.published, (newValue, oldValue) => {
  // When toggling from unpublished to published, auto-fill published_at if empty
  if (newValue && !oldValue && !formData.published_at) {
    const now = new Date()
    formData.published_at = now.toISOString().slice(0, 16)
  }
})

// Load post on mount if editing
onMounted(() => {
  if (isEditMode.value) {
    loadPost()
  } else {
    // New post - auto-fill created_at
    initializeNewPost()
  }
})
</script>

<style scoped>
.post-editor {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem 1rem;
}

.editor-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.editor-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--bg-hover);
}

.editor-header h1 {
  margin: 0;
  font-size: 2rem;
  color: var(--text-primary);
}

/* Status Messages */
.status-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.status-message.success {
  background: rgba(35, 134, 54, 0.1);
  border: 1px solid var(--accent-primary);
  color: var(--accent-primary);
}

.status-message.error {
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid #dc2626;
  color: #dc2626;
}

.status-message p {
  margin: 0;
  flex: 1;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Form */
.editor-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
}

.form-section h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9375rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(35, 134, 54, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-tertiary);
}

/* Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  gap: 1rem;
}

.actions-left,
.actions-right {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.publish-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 0.9375rem;
}

.publish-toggle input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-hover);
}

/* Mobile */
@media (max-width: 768px) {
  .post-editor {
    padding: 1rem 0.5rem;
  }

  .editor-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .form-section {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .actions-left,
  .actions-right {
    width: 100%;
    justify-content: space-between;
  }

  .actions-right {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
