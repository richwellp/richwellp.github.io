<template>
  <div class="photo-manager">
    <AdminAuthModal
      :is-open="showAuthModal"
      @close="handleAuthCancel"
      @authenticated="handleAuthenticated"
    />

    <DeleteConfirmModal
      :is-open="showDeleteModal"
      :item-name="photoToDelete?.caption || 'this photo'"
      :is-deleting="isDeleting"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <PhotoEditorModal
      :is-open="showEditorModal"
      :photo="editingPhoto"
      :is-saving="isSaving"
      @close="closeEditor"
      @save="savePhoto"
    />

    <div v-if="isAuthenticated" class="admin-content">
      <!-- Header -->
      <div class="admin-header">
        <div class="header-left">
          <router-link to="/admin/albums" class="back-link">← Albums</router-link>
          <h1>{{ albumName }} Photos</h1>
          <p class="subtitle">Manage photos in this album</p>
        </div>
        <div class="header-actions">
          <button @click="handleLogout" class="btn btn-secondary">Logout</button>
          <button @click="createNewPhoto" class="btn btn-primary">+ Add Photo</button>
        </div>
      </div>

      <!-- Sort Controls -->
      <div class="controls">
        <div class="sort-controls">
          <label>Sort by:</label>
          <select v-model="sortBy" @change="loadPhotos" class="sort-select">
            <option value="order">Display Order</option>
            <option value="date">Date Taken</option>
            <option value="category">Category</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading photos...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <p class="error-message">{{ error }}</p>
        <button @click="loadPhotos" class="btn btn-secondary">Retry</button>
      </div>

      <!-- Photos Grid -->
      <div v-else-if="photos.length > 0" class="photos-grid">
        <div v-for="photo in photos" :key="photo.id" class="photo-card">
          <div class="photo-image">
            <img v-if="!isVideo(photo)" :src="photo.url" :alt="photo.caption || 'Photo'" />
            <video v-else :src="photo.url" controls playsinline>
              <source :src="photo.url" type="video/mp4">
              Your browser doesn't support videos.
            </video>
          </div>
          <div class="photo-info">
            <div class="photo-details">
              <p v-if="photo.caption" class="photo-caption">{{ photo.caption }}</p>
              <p v-if="photo.location" class="photo-location">📍 {{ photo.location }}</p>
              <p v-if="photo.date_taken" class="photo-date">📅 {{ formatDate(photo.date_taken) }}</p>
              <p v-if="photo.category" class="photo-category">🏷️ {{ photo.category }}</p>
              <p class="photo-order">Order: {{ photo.order_index }}</p>
            </div>
            <div class="photo-actions">
              <button @click="editPhoto(photo)" class="action-btn">Edit</button>
              <button @click="initiateDelete(photo)" class="action-btn danger">Delete</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📷</div>
        <h2>No photos yet</h2>
        <p>Add your first photo to this album</p>
        <button @click="createNewPhoto" class="btn btn-primary">+ Add Photo</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AdminAuthModal from '../../components/AdminAuthModal.vue'
import DeleteConfirmModal from '../../components/DeleteConfirmModal.vue'
import PhotoEditorModal from '../../components/PhotoEditorModal.vue'
import { useAdminAuth } from '../../composables/useAdminAuth'
import { useAdminAlbums } from '../../composables/useAdminAlbums'

const router = useRouter()
const route = useRoute()
const { isAuthenticated, logout } = useAdminAuth()
const {
  photos,
  loading,
  error,
  fetchAlbumPhotos,
  createPhoto,
  updatePhoto,
  deletePhoto
} = useAdminAlbums()

const albumSlug = computed(() => route.params.slug)
const albumName = ref('')
const sortBy = ref('order')
const showAuthModal = ref(!isAuthenticated.value)
const showDeleteModal = ref(false)
const showEditorModal = ref(false)
const photoToDelete = ref(null)
const editingPhoto = ref(null)
const isDeleting = ref(false)
const isSaving = ref(false)

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

const isVideo = (photo) => {
  // Check type field if available
  if (photo.type === 'video') return true
  if (photo.type === 'image') return false

  // Fallback: detect from URL extension if type field is missing
  if (photo.url) {
    const urlLower = photo.url.toLowerCase()
    const hasVideoExt = /\.(mp4|mov|webm|avi|mkv)(\?|#|$)/i.test(urlLower)
    if (hasVideoExt) return true

    // Check Content-Type in URL (Supabase includes it)
    if (urlLower.includes('video/') || urlLower.includes('.mp4') || urlLower.includes('.mov')) {
      return true
    }
  }

  return false
}

const handleAuthenticated = async () => {
  showAuthModal.value = false
  await loadPhotos()
}

const handleAuthCancel = () => {
  router.push('/')
}

const handleLogout = () => {
  logout()
  router.push('/')
}

const loadPhotos = async () => {
  try {
    const data = await fetchAlbumPhotos(albumSlug.value, sortBy.value)
    albumName.value = data.album?.name || albumSlug.value
  } catch (err) {
    console.error('Failed to load photos:', err)
  }
}

const createNewPhoto = () => {
  editingPhoto.value = null
  showEditorModal.value = true
}

const editPhoto = (photo) => {
  editingPhoto.value = { ...photo }
  showEditorModal.value = true
}

const closeEditor = () => {
  showEditorModal.value = false
  editingPhoto.value = null
}

const savePhoto = async (photoData) => {
  isSaving.value = true
  try {
    if (editingPhoto.value) {
      // Update existing photo
      await updatePhoto(editingPhoto.value.id, photoData)
    } else {
      // Create new photo
      await createPhoto(albumSlug.value, photoData)
    }
    await loadPhotos()
    closeEditor()
  } catch (err) {
    console.error('Failed to save photo:', err)
    alert('Failed to save photo: ' + err.message)
  } finally {
    isSaving.value = false
  }
}

const initiateDelete = (photo) => {
  photoToDelete.value = photo
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  photoToDelete.value = null
}

const confirmDelete = async () => {
  if (!photoToDelete.value) return

  isDeleting.value = true
  try {
    await deletePhoto(photoToDelete.value.id)
    await loadPhotos()
    showDeleteModal.value = false
    photoToDelete.value = null
  } catch (err) {
    console.error('Failed to delete photo:', err)
    alert('Failed to delete photo: ' + err.message)
  } finally {
    isDeleting.value = false
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    loadPhotos()
  }
})
</script>

<style scoped>
.photo-manager {
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

.controls {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-color);
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-controls label {
  color: var(--text-primary);
  font-weight: 600;
}

.sort-select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  cursor: pointer;
}

.sort-select:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.photo-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

@media (hover: hover) {
  .photo-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px var(--shadow);
  }
}

.photo-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  background: var(--bg-tertiary);
}

.photo-image img,
.photo-image video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-info {
  padding: 1rem;
}

.photo-details {
  margin-bottom: 1rem;
}

.photo-caption {
  font-size: 1rem;
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.photo-location,
.photo-date,
.photo-category,
.photo-order {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0.25rem 0;
}

.photo-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  background: var(--bg-tertiary);
  border-color: var(--accent-primary);
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

  .photos-grid {
    grid-template-columns: 1fr;
  }
}
</style>
