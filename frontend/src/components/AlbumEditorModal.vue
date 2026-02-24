<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-backdrop" @click="handleBackdropClick">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditing ? 'Edit Album' : 'Create Album' }}</h2>
            <button @click="$emit('close')" class="close-btn">&times;</button>
          </div>

          <form @submit.prevent="handleSubmit" class="modal-body">
            <div class="form-group">
              <label for="slug">Slug *</label>
              <input
                id="slug"
                v-model="form.slug"
                type="text"
                required
                :disabled="isEditing"
                placeholder="travel"
              />
              <small>URL-friendly name (lowercase, no spaces)</small>
            </div>

            <div class="form-group">
              <label for="name">Name *</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                placeholder="Travel"
              />
            </div>

            <div class="form-group">
              <label for="icon">Icon *</label>
              <input
                id="icon"
                v-model="form.icon"
                type="text"
                required
                placeholder="✈️"
              />
              <small>Emoji to display for this album</small>
            </div>

            <div class="form-group">
              <label for="subtitle">Subtitle</label>
              <input
                id="subtitle"
                v-model="form.subtitle"
                type="text"
                placeholder="Exploring the world"
              />
            </div>

            <div class="form-group">
              <label for="categories">Categories (comma-separated)</label>
              <input
                id="categories"
                v-model="categoriesInput"
                type="text"
                placeholder="usa, philippines, japan"
              />
              <small>Leave empty if album doesn't use categories</small>
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

            <div class="form-group checkbox">
              <input
                id="published"
                v-model="form.published"
                type="checkbox"
              />
              <label for="published">Published</label>
            </div>

            <div class="modal-footer">
              <button type="button" @click="$emit('close')" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="isSaving">
                {{ isSaving ? 'Saving...' : (isEditing ? 'Update' : 'Create') }}
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
  album: Object,
  isSaving: Boolean
})

const emit = defineEmits(['close', 'save'])

const isEditing = computed(() => !!props.album)

const form = ref({
  slug: '',
  name: '',
  icon: '📷',
  subtitle: '',
  categories: null,
  order_index: 0,
  published: true
})

const categoriesInput = ref('')

// Watch for album changes (when editing)
watch(() => props.album, (newAlbum) => {
  if (newAlbum) {
    form.value = {
      slug: newAlbum.slug || '',
      name: newAlbum.name || '',
      icon: newAlbum.icon || '📷',
      subtitle: newAlbum.subtitle || '',
      categories: newAlbum.categories || null,
      order_index: newAlbum.order_index || 0,
      published: newAlbum.published !== false
    }
    categoriesInput.value = newAlbum.categories ? newAlbum.categories.join(', ') : ''
  } else {
    // Reset for create
    form.value = {
      slug: '',
      name: '',
      icon: '📷',
      subtitle: '',
      categories: null,
      order_index: 0,
      published: true
    }
    categoriesInput.value = ''
  }
}, { immediate: true })

const handleSubmit = () => {
  // Parse categories from comma-separated input
  const categoriesArray = categoriesInput.value
    .split(',')
    .map(c => c.trim())
    .filter(c => c.length > 0)

  const albumData = {
    ...form.value,
    categories: categoriesArray.length > 0 ? categoriesArray : null
  }

  emit('save', albumData)
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
.form-group input[type="number"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group.checkbox input {
  width: auto;
  margin: 0;
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
