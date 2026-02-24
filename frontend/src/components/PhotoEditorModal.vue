<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-backdrop" @click="handleBackdropClick">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditing ? 'Edit Photo' : 'Add Photo' }}</h2>
            <button @click="$emit('close')" class="close-btn">&times;</button>
          </div>

          <form @submit.prevent="handleSubmit" class="modal-body">
            <!-- File Upload -->
            <div class="form-group">
              <label for="file">Upload File *</label>
              <div class="upload-area" :class="{ 'has-file': selectedFile, 'uploading': uploading }">
                <input
                  id="file"
                  type="file"
                  accept="image/*,video/*"
                  @change="handleFileSelect"
                  class="file-input"
                  :disabled="uploading"
                />
                <div v-if="!selectedFile && !form.url" class="upload-placeholder">
                  <span class="upload-icon">📁</span>
                  <p>Click to select image or video</p>
                  <small>Supports: JPG, PNG, MP4, MOV (max 50MB)</small>
                </div>
                <div v-else-if="selectedFile" class="file-selected">
                  <span class="file-icon">{{ selectedFile.type.startsWith('video') ? '🎥' : '🖼️' }}</span>
                  <p>{{ selectedFile.name }}</p>
                  <small>{{ formatFileSize(selectedFile.size) }}</small>
                  <button v-if="!uploading" type="button" @click="clearFile" class="clear-btn">×</button>
                </div>
                <div v-else-if="form.url" class="url-preview">
                  <p>{{ form.url }}</p>
                </div>
                <div v-if="uploading" class="upload-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
                  </div>
                  <small>Uploading... {{ uploadProgress }}%</small>
                </div>
              </div>
              <small v-if="uploadError" class="error-text">{{ uploadError }}</small>
            </div>

            <!-- Manual URL (alternative) -->
            <div v-if="!selectedFile && !uploading" class="form-group">
              <label for="url">Or paste URL manually</label>
              <input
                id="url"
                v-model="form.url"
                type="text"
                placeholder="https://example.com/photo.jpg"
              />
              <small>Direct URL to image or video file</small>
            </div>

            <div class="form-group">
              <label for="caption">Caption</label>
              <textarea
                id="caption"
                v-model="form.caption"
                rows="3"
                placeholder="Photo description"
              />
            </div>

            <div class="form-group">
              <label for="location">Location</label>
              <input
                id="location"
                v-model="form.location"
                type="text"
                placeholder="City, Country"
              />
            </div>

            <div class="form-group">
              <label for="date_taken">Date Taken</label>
              <input
                id="date_taken"
                v-model="form.date_taken"
                type="date"
              />
            </div>

            <div class="form-group">
              <label for="category">Category</label>
              <input
                id="category"
                v-model="form.category"
                type="text"
                placeholder="usa, philippines, japan, etc."
              />
              <small>Must match one of the album's categories</small>
            </div>

            <div class="form-group">
              <label for="order_index">Display Order</label>
              <input
                id="order_index"
                v-model.number="form.order_index"
                type="number"
                min="0"
              />
            </div>

            <div class="modal-footer">
              <button type="button" @click="$emit('close')" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isSaving">
                {{ isSaving ? 'Saving...' : (isEditing ? 'Update' : 'Add') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { uploadFile } from '../lib/supabase'
import { useAdminAuth } from '../composables/useAdminAuth'

const props = defineProps({
  isOpen: Boolean,
  photo: Object,
  isSaving: Boolean
})

const emit = defineEmits(['close', 'save'])
const route = useRoute()
const { adminToken } = useAdminAuth()

const isEditing = computed(() => !!props.photo)

const form = ref({
  url: '',
  caption: '',
  location: '',
  date_taken: '',
  category: null,
  order_index: 0
})

// File upload state
const selectedFile = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadError = ref('')

// Watch for photo changes (when editing)
watch(() => props.photo, (newPhoto) => {
  if (newPhoto) {
    form.value = {
      url: newPhoto.url || '',
      caption: newPhoto.caption || '',
      location: newPhoto.location || '',
      date_taken: newPhoto.date_taken || '',
      category: newPhoto.category || null,
      order_index: newPhoto.order_index || 0
    }
  } else {
    // Reset for create
    form.value = {
      url: '',
      caption: '',
      location: '',
      date_taken: '',
      category: null,
      order_index: 0
    }
  }
}, { immediate: true })

// File handling
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'video/mp4', 'video/quicktime', 'video/webm']
  if (!validTypes.includes(file.type)) {
    uploadError.value = 'Invalid file type. Supported: JPG, PNG, GIF, WEBP, MP4, MOV, WEBM'
    return
  }

  // Validate file size (50MB max)
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    uploadError.value = 'File too large. Maximum size: 50MB'
    return
  }

  selectedFile.value = file
  uploadError.value = ''
}

const clearFile = () => {
  selectedFile.value = null
  uploadError.value = ''
  // Clear file input
  const fileInput = document.getElementById('file')
  if (fileInput) fileInput.value = ''
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const handleSubmit = async () => {
  // Store file type before uploading (in case file is cleared)
  let fileType = null
  if (selectedFile.value) {
    fileType = selectedFile.value.type
  }

  // If file is selected, upload it first
  if (selectedFile.value && !uploading.value) {
    try {
      uploading.value = true
      uploadProgress.value = 0
      uploadError.value = ''

      // Get album slug from route
      const albumSlug = route.params.slug

      // Simulate progress (since Supabase doesn't provide real progress)
      const progressInterval = setInterval(() => {
        if (uploadProgress.value < 90) {
          uploadProgress.value += 10
        }
      }, 100)

      // Upload file (using backend API with admin auth)
      const { url } = await uploadFile(selectedFile.value, albumSlug, adminToken.value)

      clearInterval(progressInterval)
      uploadProgress.value = 100

      // Set URL in form
      form.value.url = url

      // Clear file state
      setTimeout(() => {
        selectedFile.value = null
        uploading.value = false
        uploadProgress.value = 0
      }, 500)
    } catch (error) {
      console.error('Upload failed:', error)
      uploadError.value = error.message || 'Upload failed'
      uploading.value = false
      uploadProgress.value = 0
      return // Don't submit if upload fails
    }
  }

  // Validate URL exists
  if (!form.value.url) {
    uploadError.value = 'Please upload a file or enter a URL'
    return
  }

  // Detect type from saved file type, URL, or default to image
  let mediaType = 'image' // default
  if (fileType) {
    // Use the file type we saved before upload
    mediaType = fileType.startsWith('video') ? 'video' : 'image'
  } else if (form.value.url) {
    // Detect from URL extension
    const urlLower = form.value.url.toLowerCase()
    if (urlLower.match(/\.(mp4|mov|webm|avi|mkv)(\?|$)/)) {
      mediaType = 'video'
    }
  }

  const photoData = {
    ...form.value,
    // Note: type field is commented out until column is added to database
    // Uncomment after running: ALTER TABLE photos ADD COLUMN type TEXT DEFAULT 'image';
    // type: mediaType,
    category: form.value.category?.trim() || null,
    date_taken: form.value.date_taken || null
  }

  emit('save', photoData)
}

const handleBackdropClick = () => {
  emit('close')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--bg-card);
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 2rem;
  height: 2rem;
}

.close-btn:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 600;
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group input[type="number"],
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: var(--border-color);
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

/* Upload Area */
.upload-area {
  position: relative;
  border: 2px dashed var(--border-color);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  background: var(--bg-secondary);
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: var(--accent-primary);
  background: var(--bg-tertiary);
}

.upload-area.uploading {
  cursor: not-allowed;
  opacity: 0.7;
}

.file-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.file-input:disabled {
  cursor: not-allowed;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.upload-icon {
  font-size: 3rem;
}

.upload-placeholder p {
  color: var(--text-primary);
  font-weight: 600;
  margin: 0;
}

.upload-placeholder small {
  color: var(--text-secondary);
}

.file-selected,
.url-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}

.file-icon {
  font-size: 2.5rem;
}

.file-selected p,
.url-preview p {
  color: var(--text-primary);
  font-weight: 600;
  margin: 0;
  word-break: break-all;
}

.file-selected small {
  color: var(--text-secondary);
}

.clear-btn {
  position: absolute;
  top: -1rem;
  right: -1rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.upload-progress {
  margin-top: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: var(--accent-primary);
  transition: width 0.3s ease;
}

.error-text {
  color: #ef4444;
  font-weight: 600;
}
</style>
