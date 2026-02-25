<template>
  <div>
    <!-- Backdrop -->
    <Transition name="fade">
      <div v-if="isOpen" class="auth-modal-backdrop" @click="handleCancel"></div>
    </Transition>

    <!-- Modal -->
    <Transition name="slide-fade">
      <div v-if="isOpen" class="auth-modal">
        <div class="auth-modal-content">
          <!-- Header -->
          <div class="auth-header">
            <h2>Admin Authentication</h2>
            <button class="close-btn" @click="handleCancel" aria-label="Close">×</button>
          </div>

          <!-- Body -->
          <div class="auth-body">
            <p class="auth-description">Enter your admin key to access the blog admin panel.</p>

            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="admin-key">Admin Key</label>
                <input
                  id="admin-key"
                  ref="keyInput"
                  v-model="adminKey"
                  type="password"
                  class="form-input"
                  placeholder="Enter admin key"
                  :disabled="isAuthenticating"
                  autocomplete="off"
                />
              </div>

              <!-- Error message -->
              <div v-if="error" class="error-message">
                {{ error }}
              </div>

              <!-- Actions -->
              <div class="auth-actions">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="handleCancel"
                  :disabled="isAuthenticating"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="!adminKey.trim() || isAuthenticating"
                >
                  <span v-if="isAuthenticating">Authenticating...</span>
                  <span v-else>Continue</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useAdminAuth } from '../composables/useAdminAuth'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'authenticated'])

const { login } = useAdminAuth()
const adminKey = ref('')
const error = ref(null)
const isAuthenticating = ref(false)
const keyInput = ref(null)

// Focus input when modal opens
watch(() => props.isOpen, async (newValue) => {
  if (newValue) {
    await nextTick()
    keyInput.value?.focus()
    // Reset state
    adminKey.value = ''
    error.value = null
    isAuthenticating.value = false
  }
})

const handleSubmit = async () => {
  error.value = null

  if (!adminKey.value.trim()) {
    error.value = 'Please enter an admin key'
    return
  }

  isAuthenticating.value = true

  try {
    const success = await login(adminKey.value)

    if (success) {
      emit('authenticated')
      // Don't emit 'close' - let parent handle modal visibility
    } else {
      error.value = 'Invalid admin key'
    }
  } catch (err) {
    error.value = 'Authentication failed. Please try again.'
  } finally {
    isAuthenticating.value = false
  }
}

const handleCancel = () => {
  adminKey.value = ''
  error.value = null
  emit('close')
}

// Handle ESC key
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && props.isOpen) {
    handleCancel()
  }
}

// Lifecycle
import { onMounted, onUnmounted } from 'vue'

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
.auth-modal-backdrop {
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
.auth-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1001;
  width: min(480px, calc(100vw - 2rem));
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
}

.auth-modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Header */
.auth-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.auth-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.75rem;
  line-height: 1;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0.25rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

/* Body */
.auth-body {
  padding: 1.5rem;
}

.auth-description {
  margin: 0 0 1.5rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9375rem;
}

.form-input {
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

.form-input:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(35, 134, 54, 0.1);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Error message */
.error-message {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 6px;
  color: #dc2626;
  font-size: 0.875rem;
}

/* Actions */
.auth-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
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
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-hover);
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

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

/* Mobile adjustments */
@media (max-width: 480px) {
  .auth-modal {
    width: calc(100vw - 1rem);
  }

  .auth-header, .auth-body {
    padding: 1.25rem;
  }

  .auth-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
