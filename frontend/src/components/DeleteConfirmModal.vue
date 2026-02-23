<template>
  <div>
    <!-- Backdrop -->
    <Transition name="fade">
      <div v-if="isOpen" class="delete-modal-backdrop" @click="handleCancel"></div>
    </Transition>

    <!-- Modal -->
    <Transition name="slide-fade">
      <div v-if="isOpen" class="delete-modal">
        <div class="delete-modal-content">
          <!-- Header -->
          <div class="delete-header">
            <span class="delete-icon">⚠️</span>
            <h2>Confirm Delete</h2>
          </div>

          <!-- Body -->
          <div class="delete-body">
            <p class="delete-message">
              Are you sure you want to delete <strong>{{ itemName }}</strong>?
            </p>
            <p class="delete-warning">
              This action cannot be undone.
            </p>
          </div>

          <!-- Actions -->
          <div class="delete-actions">
            <button
              type="button"
              class="btn btn-secondary"
              @click="handleCancel"
              :disabled="isDeleting"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="handleConfirm"
              :disabled="isDeleting"
            >
              <span v-if="isDeleting">Deleting...</span>
              <span v-else>Delete</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  itemName: {
    type: String,
    required: true
  },
  isDeleting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
}

// Handle ESC key
import { onMounted, onUnmounted } from 'vue'

const handleKeyDown = (event) => {
  if (event.key === 'Escape' && props.isOpen) {
    handleCancel()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}

.slide-fade-leave-active {
  transition: all 0.25s ease;
}

.slide-fade-enter-from {
  transform: translateY(-20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Backdrop */
.delete-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1000;
}

/* Modal */
.delete-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1001;
  width: min(420px, calc(100vw - 2rem));
}

.delete-modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* Header */
.delete-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: rgba(220, 38, 38, 0.05);
}

.delete-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.delete-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Body */
.delete-body {
  padding: 1.5rem;
}

.delete-message {
  margin: 0 0 1rem;
  color: var(--text-primary);
  line-height: 1.5;
}

.delete-message strong {
  color: var(--text-primary);
  font-weight: 600;
}

.delete-warning {
  margin: 0;
  padding: 0.75rem;
  background: rgba(220, 38, 38, 0.1);
  border-left: 3px solid #dc2626;
  color: #dc2626;
  font-size: 0.875rem;
  border-radius: 4px;
}

/* Actions */
.delete-actions {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-tertiary);
  justify-content: flex-end;
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
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-hover);
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.btn-danger:active:not(:disabled) {
  transform: translateY(0);
}

/* Mobile adjustments */
@media (max-width: 480px) {
  .delete-modal {
    width: calc(100vw - 1rem);
  }

  .delete-header,
  .delete-body,
  .delete-actions {
    padding: 1.25rem;
  }

  .delete-actions {
    flex-direction: column-reverse;
  }

  .btn {
    width: 100%;
  }
}
</style>
