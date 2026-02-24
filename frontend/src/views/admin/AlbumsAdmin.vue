<template>
  <div class="albums-admin">
    <AdminAuthModal
      :is-open="showAuthModal"
      @close="handleAuthCancel"
      @authenticated="handleAuthenticated"
    />

    <DeleteConfirmModal
      :is-open="showDeleteModal"
      :item-name="albumToDelete?.name || ''"
      :is-deleting="isDeleting"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <AlbumEditorModal
      :is-open="showEditorModal"
      :album="editingAlbum"
      :is-saving="isSaving"
      @close="closeEditor"
      @save="saveAlbum"
    />

    <div v-if="isAuthenticated" class="admin-content">
      <!-- Header -->
      <div class="admin-header">
        <div class="header-left">
          <router-link to="/admin" class="back-link">← Dashboard</router-link>
          <h1>Albums Admin</h1>
          <p class="subtitle">Manage photo albums</p>
        </div>
        <div class="header-actions">
          <button @click="handleLogout" class="btn btn-secondary">Logout</button>
          <button @click="createNewAlbum" class="btn btn-primary">+ New Album</button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading albums...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <p class="error-message">{{ error }}</p>
        <button @click="loadAlbums" class="btn btn-secondary">Retry</button>
      </div>

      <!-- Albums Table -->
      <div v-else-if="albums.length > 0" class="albums-table">
        <table>
          <thead>
            <tr>
              <th>Icon</th>
              <th>Name</th>
              <th>Slug</th>
              <th>Photos</th>
              <th>Categories</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="album in albums" :key="album.id">
              <td class="icon-cell">{{ album.icon }}</td>
              <td class="name-cell">
                <strong>{{ album.name }}</strong>
                <small v-if="album.subtitle">{{ album.subtitle }}</small>
              </td>
              <td>{{ album.slug }}</td>
              <td class="center">{{ album.photo_count || 0 }}</td>
              <td>
                <span v-if="album.categories && album.categories.length > 0" class="categories">
                  {{ album.categories.join(', ') }}
                </span>
                <span v-else class="no-categories">None</span>
              </td>
              <td>
                <span class="status-badge" :class="{ published: album.published, draft: !album.published }">
                  {{ album.published ? 'Published' : 'Draft' }}
                </span>
              </td>
              <td class="actions-cell">
                <router-link :to="`/admin/albums/${album.slug}/photos`" class="action-btn">
                  Manage Photos
                </router-link>
                <button @click="editAlbum(album)" class="action-btn" title="Edit">Edit</button>
                <button @click="togglePublish(album)" class="action-btn" :disabled="isTogglingPublish[album.slug]">
                  {{ album.published ? 'Unpublish' : 'Publish' }}
                </button>
                <button @click="initiateDelete(album)" class="action-btn danger" title="Delete">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📸</div>
        <h2>No albums yet</h2>
        <p>Create your first album to get started</p>
        <button @click="createNewAlbum" class="btn btn-primary">+ Create Album</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminAuthModal from '../../components/AdminAuthModal.vue'
import DeleteConfirmModal from '../../components/DeleteConfirmModal.vue'
import AlbumEditorModal from '../../components/AlbumEditorModal.vue'
import { useAdminAuth } from '../../composables/useAdminAuth'
import { useAdminAlbums } from '../../composables/useAdminAlbums'

const router = useRouter()
const { isAuthenticated, logout } = useAdminAuth()
const {
  albums,
  loading,
  error,
  fetchAdminAlbums,
  createAlbum,
  updateAlbum,
  deleteAlbum
} = useAdminAlbums()

const showAuthModal = ref(!isAuthenticated.value)
const showDeleteModal = ref(false)
const showEditorModal = ref(false)
const albumToDelete = ref(null)
const editingAlbum = ref(null)
const isDeleting = ref(false)
const isSaving = ref(false)
const isTogglingPublish = reactive({})

const handleAuthenticated = async () => {
  showAuthModal.value = false
  await loadAlbums()
}

const handleAuthCancel = () => {
  router.push('/')
}

const handleLogout = () => {
  logout()
  router.push('/')
}

const loadAlbums = async () => {
  try {
    await fetchAdminAlbums()
  } catch (err) {
    console.error('Failed to load albums:', err)
  }
}

const createNewAlbum = () => {
  editingAlbum.value = null
  showEditorModal.value = true
}

const editAlbum = (album) => {
  editingAlbum.value = { ...album }
  showEditorModal.value = true
}

const closeEditor = () => {
  showEditorModal.value = false
  editingAlbum.value = null
}

const saveAlbum = async (albumData) => {
  isSaving.value = true
  try {
    if (editingAlbum.value) {
      // Update existing album
      await updateAlbum(albumData.slug, albumData)
    } else {
      // Create new album
      await createAlbum(albumData)
    }
    await loadAlbums()
    closeEditor()
  } catch (err) {
    console.error('Failed to save album:', err)
    alert('Failed to save album: ' + err.message)
  } finally {
    isSaving.value = false
  }
}

const togglePublish = async (album) => {
  isTogglingPublish[album.slug] = true
  try {
    await updateAlbum(album.slug, { published: !album.published })
    await loadAlbums()
  } catch (err) {
    console.error('Failed to toggle publish:', err)
    alert('Failed to update album')
  } finally {
    isTogglingPublish[album.slug] = false
  }
}

const initiateDelete = (album) => {
  albumToDelete.value = album
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  albumToDelete.value = null
}

const confirmDelete = async () => {
  if (!albumToDelete.value) return

  isDeleting.value = true
  try {
    await deleteAlbum(albumToDelete.value.slug)
    await loadAlbums()
    showDeleteModal.value = false
    albumToDelete.value = null
  } catch (err) {
    console.error('Failed to delete album:', err)
    alert('Failed to delete album: ' + err.message)
  } finally {
    isDeleting.value = false
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    loadAlbums()
  }
})
</script>

<style scoped>
.albums-admin {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem;
}

.admin-content {
  max-width: 1400px;
  margin: 0 auto;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-left {
  flex: 1;
}

.back-link {
  display: inline-block;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.back-link:hover {
  color: var(--link-hover);
}

.admin-header h1 {
  font-size: 2rem;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.albums-table {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--bg-tertiary);
}

th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

td {
  padding: 1rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: var(--bg-tertiary);
}

.icon-cell {
  font-size: 1.5rem;
  width: 60px;
  text-align: center;
}

.name-cell strong {
  display: block;
  margin-bottom: 0.25rem;
}

.name-cell small {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.center {
  text-align: center;
}

.categories {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.no-categories {
  color: var(--text-secondary);
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.published {
  background: rgba(34, 197, 94, 0.2);
  color: rgb(34, 197, 94);
}

.status-badge.draft {
  background: rgba(234, 179, 8, 0.2);
  color: rgb(234, 179, 8);
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  background: var(--bg-tertiary);
  border-color: var(--accent-primary);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.danger {
  color: #ef4444;
}

.action-btn.danger:hover:not(:disabled) {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #ef4444;
  margin-bottom: 1rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: var(--border-color);
}

@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .albums-table {
    overflow-x: auto;
  }

  table {
    min-width: 800px;
  }
}
</style>
