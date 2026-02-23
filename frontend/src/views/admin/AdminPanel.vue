<template>
  <div class="admin-panel">
    <!-- Auth Modal -->
    <AdminAuthModal
      :is-open="showAuthModal"
      @close="handleAuthCancel"
      @authenticated="handleAuthenticated"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal
      :is-open="showDeleteModal"
      :item-name="postToDelete?.title || ''"
      :is-deleting="isDeleting"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <!-- Main Content -->
    <div v-if="isAuthenticated" class="admin-content">
      <!-- Header -->
      <div class="admin-header">
        <div class="header-left">
          <h1>Blog Admin</h1>
          <p class="subtitle">Manage your blog posts</p>
        </div>
        <div class="header-actions">
          <button @click="handleLogout" class="btn btn-secondary">
            Logout
          </button>
          <button @click="createNewPost" class="btn btn-primary">
            + New Post
          </button>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters">
        <button
          v-for="filter in filters"
          :key="filter.value"
          @click="currentFilter = filter.value"
          class="filter-btn"
          :class="{ active: currentFilter === filter.value }"
        >
          {{ filter.label }}
          <span v-if="filter.count !== undefined" class="count">{{ filter.count }}</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading posts...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <p class="error-message">{{ error }}</p>
        <button @click="loadPosts" class="btn btn-secondary">Retry</button>
      </div>

      <!-- Posts List -->
      <div v-else-if="filteredPosts.length > 0" class="posts-list">
        <div
          v-for="post in filteredPosts"
          :key="post.slug"
          class="post-card"
        >
          <div class="post-info">
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-meta">
              <span class="status-badge" :class="{ published: post.published, draft: !post.published }">
                {{ post.published ? 'Published' : 'Draft' }}
              </span>
              <span>{{ formatDate(post.created_at || post.published_at) }}</span>
              <span v-if="post.tags && post.tags.length > 0">
                {{ post.tags.join(', ') }}
              </span>
            </p>
            <p v-if="post.excerpt" class="post-excerpt">{{ post.excerpt }}</p>
          </div>

          <div class="post-actions">
            <button
              @click="editPost(post)"
              class="action-btn"
              title="Edit"
            >
              Edit
            </button>
            <button
              @click="togglePublish(post)"
              class="action-btn"
              :title="post.published ? 'Unpublish' : 'Publish'"
              :disabled="isTogglingPublish[post.slug]"
            >
              {{ post.published ? 'Unpublish' : 'Publish' }}
            </button>
            <button
              @click="initiateDelete(post)"
              class="action-btn danger"
              title="Delete"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <p class="empty-icon">📝</p>
        <p class="empty-message">No posts found</p>
        <button @click="createNewPost" class="btn btn-primary">
          Create Your First Post
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuth } from '../../composables/useAdminAuth'
import { useAdminBlog } from '../../composables/useAdminBlog'
import AdminAuthModal from '../../components/AdminAuthModal.vue'
import DeleteConfirmModal from '../../components/DeleteConfirmModal.vue'

const router = useRouter()
const { isAuthenticated, logout } = useAdminAuth()
const { posts, loading, error, fetchAdminPosts, updatePost, deletePost } = useAdminBlog()

const showAuthModal = ref(!isAuthenticated.value)
const currentFilter = ref('all')
const showDeleteModal = ref(false)
const postToDelete = ref(null)
const isDeleting = ref(false)
const isTogglingPublish = ref({})

// Filters
const filters = computed(() => {
  const allCount = posts.value.length
  const publishedCount = posts.value.filter(p => p.published).length
  const draftCount = posts.value.filter(p => !p.published).length

  return [
    { label: 'All', value: 'all', count: allCount },
    { label: 'Published', value: 'published', count: publishedCount },
    { label: 'Drafts', value: 'draft', count: draftCount }
  ]
})

// Filtered posts
const filteredPosts = computed(() => {
  if (currentFilter.value === 'published') {
    return posts.value.filter(p => p.published)
  } else if (currentFilter.value === 'draft') {
    return posts.value.filter(p => !p.published)
  }
  return posts.value
})

// Auth handlers
const handleAuthenticated = async () => {
  showAuthModal.value = false
  await loadPosts()
}

const handleAuthCancel = () => {
  showAuthModal.value = false
  router.push('/misc/blog')
}

const handleLogout = () => {
  logout()
  router.push('/misc/blog')
}

// Load posts
const loadPosts = async () => {
  try {
    await fetchAdminPosts({ status: currentFilter.value === 'all' ? undefined : currentFilter.value })
  } catch (err) {
    console.error('Failed to load posts:', err)
  }
}

// Create new post
const createNewPost = () => {
  router.push('/admin/new')
}

// Edit post
const editPost = (post) => {
  router.push(`/admin/edit/${post.slug}`)
}

// Toggle publish status
const togglePublish = async (post) => {
  isTogglingPublish.value[post.slug] = true

  try {
    await updatePost(post.slug, { published: !post.published })
    // Reload posts
    await loadPosts()
  } catch (err) {
    console.error('Failed to toggle publish status:', err)
    alert('Failed to update post status')
  } finally {
    isTogglingPublish.value[post.slug] = false
  }
}

// Delete handlers
const initiateDelete = (post) => {
  postToDelete.value = post
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!postToDelete.value) return

  isDeleting.value = true

  try {
    await deletePost(postToDelete.value.slug)
    showDeleteModal.value = false
    postToDelete.value = null
    // Reload posts
    await loadPosts()
  } catch (err) {
    console.error('Failed to delete post:', err)
    alert('Failed to delete post')
  } finally {
    isDeleting.value = false
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  postToDelete.value = null
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'No date'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Load posts on mount if authenticated
onMounted(() => {
  if (isAuthenticated.value) {
    loadPosts()
  }
})
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem 1rem;
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 1rem;
}

.header-left h1 {
  margin: 0 0 0.5rem;
  font-size: 2rem;
  color: var(--text-primary);
}

.subtitle {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Buttons */
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

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
}

.btn-secondary {
  background: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--bg-hover);
}

/* Filters */
.filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.625rem 1.25rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.filter-btn.active {
  background: var(--accent-primary);
  color: white;
  border-color: var(--accent-primary);
}

.count {
  background: rgba(0, 0, 0, 0.2);
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8125rem;
}

.filter-btn.active .count {
  background: rgba(255, 255, 255, 0.2);
}

/* Loading/Error States */
.loading-state,
.error-state,
.empty-state {
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

.loading-state p,
.error-state p,
.empty-state .empty-message {
  color: var(--text-secondary);
  margin: 0;
}

.error-message {
  color: #dc2626;
  margin-bottom: 1rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

/* Posts List */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  transition: all 0.2s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px var(--shadow);
  transform: translateY(-2px);
}

.post-info {
  flex: 1;
  min-width: 0;
}

.post-title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8125rem;
  font-weight: 500;
}

.status-badge.published {
  background: rgba(35, 134, 54, 0.1);
  color: var(--accent-primary);
}

.status-badge.draft {
  background: rgba(156, 163, 175, 0.1);
  color: var(--text-tertiary);
}

.post-excerpt {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Post Actions */
.post-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.action-btn {
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.action-btn:hover {
  background: var(--bg-hover);
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.danger:hover {
  background: rgba(220, 38, 38, 0.1);
  border-color: #dc2626;
}

/* Mobile */
@media (max-width: 768px) {
  .admin-panel {
    padding: 1rem 0.5rem;
  }

  .admin-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    justify-content: space-between;
  }

  .btn {
    flex: 1;
    padding: 0.625rem 1rem;
    font-size: 0.875rem;
  }

  .post-card {
    flex-direction: column;
    gap: 1rem;
  }

  .post-actions {
    justify-content: flex-end;
  }
}
</style>
