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
            <div class="form-group">
              <label for="url">Image URL *</label>
              <input
                id="url"
                v-model="form.url"
                type="text"
                required
                placeholder="https://example.com/photo.jpg"
              />
              <small>Direct URL to the image file</small>
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

const props = defineProps({
  isOpen: Boolean,
  photo: Object,
  isSaving: Boolean
})

const emit = defineEmits(['close', 'save'])

const isEditing = computed(() => !!props.photo)

const form = ref({
  url: '',
  caption: '',
  location: '',
  date_taken: '',
  category: null,
  order_index: 0
})

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

const handleSubmit = () => {
  const photoData = {
    ...form.value,
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
</style>
