<template>
  <!-- Backdrop for mobile -->
  <Transition name="backdrop">
    <div v-if="isOpen" class="chat-backdrop" @click="toggleChat"></div>
  </Transition>

  <!-- Floating Chat Button -->
  <button
    class="chat-fab"
    @click="toggleChat"
    :aria-label="isOpen ? 'Close chat' : 'Open chat assistant'"
    :class="{ 'chat-fab-active': isOpen }"
  >
    <!-- Message Circle Icon -->
    <svg v-if="!isOpen" class="chat-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    <!-- Close X Icon -->
    <svg v-else class="chat-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>

  <!-- Chat Panel -->
  <Transition name="chat-panel">
    <div
      v-if="isOpen"
      class="chat-panel"
      role="dialog"
      aria-labelledby="chat-title"
      aria-modal="true"
    >
      <!-- Header -->
      <div class="chat-header">
        <h4 id="chat-title" class="chat-title">Virtual Assistant</h4>
        <div class="chat-header-actions">
          <button @click="clearChat" class="chat-action-btn" aria-label="Clear conversation" title="Clear conversation">
            <!-- Refresh/Clear Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <polyline points="1 4 1 10 7 10"></polyline>
              <polyline points="23 20 23 14 17 14"></polyline>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
            </svg>
          </button>
          <button @click="toggleChat" class="chat-action-btn" aria-label="Close chat" title="Close chat">
            ×
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="chat-messages" ref="messagesContainer" role="log" aria-live="polite" aria-atomic="false">
        <div
          v-for="message in messages"
          :key="message.id"
          class="chat-message"
          :class="message.type"
          role="article"
          :aria-label="`${message.type === 'user' ? 'You' : 'Assistant'} message`"
        >
          <div class="message-content">{{ message.content }}</div>
          <span class="message-time">{{ formatTime(message.timestamp) }}</span>
        </div>

        <!-- Typing indicator -->
        <div v-if="isTyping" class="chat-message assistant typing" aria-label="Assistant is typing">
          <div class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="chat-quick-actions">
        <button @click="sendQuickMessage('experience')" :disabled="isTyping">
          Experience
        </button>
        <button @click="sendQuickMessage('skills')" :disabled="isTyping">
          Skills
        </button>
        <button @click="sendQuickMessage('projects')" :disabled="isTyping">
          Projects
        </button>
        <button @click="sendQuickMessage('contact')" :disabled="isTyping">
          Contact
        </button>
      </div>

      <!-- Input -->
      <div class="chat-input-area">
        <label for="chat-input" class="visually-hidden">Type your message</label>
        <input
          id="chat-input"
          v-model="userInput"
          @keyup.enter="handleSend"
          placeholder="Type your question..."
          :disabled="isTyping"
          ref="inputField"
          aria-describedby="chat-input-hint"
          autocomplete="off"
        />
        <span id="chat-input-hint" class="visually-hidden">Press Enter to send</span>
        <button
          @click="handleSend"
          :disabled="!userInput.trim() || isTyping"
          class="send-btn"
          aria-label="Send message"
        >
          <!-- Send Arrow Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatAssistant } from '../composables/useChatAssistant'

const {
  messages,
  isOpen,
  isTyping,
  sendMessage,
  toggleChat,
  clearChat,
  sendQuickMessage,
  formatTime
} = useChatAssistant()

const userInput = ref('')
const messagesContainer = ref(null)
const inputField = ref(null)

const handleSend = async () => {
  if (!userInput.value.trim() || isTyping.value) return

  const message = userInput.value
  userInput.value = ''

  await sendMessage(message)

  // Focus input after sending
  await nextTick()
  inputField.value?.focus()
}

// Auto-scroll to bottom when new messages arrive
watch(messages, async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}, { deep: true })

// Focus input when chat opens
watch(isOpen, async (newValue) => {
  if (newValue) {
    await nextTick()
    inputField.value?.focus()
  }
})
</script>

<style scoped>
/* Accessibility */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Backdrop */
.chat-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 499;
  display: none;
}

.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.3s ease;
}

.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}

/* Floating Action Button */
.chat-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: var(--accent-primary);
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 16px var(--shadow);
  z-index: 501;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.chat-fab:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 24px var(--shadow);
  background: var(--accent-hover);
}

.chat-fab:active {
  transform: translateY(0) scale(0.98);
}

.chat-fab:focus-visible {
  outline: 3px solid var(--accent-primary);
  outline-offset: 2px;
}

.chat-icon {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.chat-fab-active {
  background: var(--text-secondary);
}

.chat-fab-active:hover {
  background: var(--text-primary);
}

/* Chat Panel */
.chat-panel {
  position: fixed;
  bottom: 92px;
  right: 24px;
  width: min(420px, calc(100vw - 48px));
  max-height: min(640px, calc(100vh - 140px));
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: 0 12px 48px var(--shadow), 0 0 0 1px rgba(0, 0, 0, 0.05);
  z-index: 500;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

/* Panel transitions */
.chat-panel-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-panel-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-panel-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.94);
}

.chat-panel-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.96);
}

/* Header */
.chat-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-card);
  flex-shrink: 0;
}

.chat-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  user-select: none;
}

.chat-header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.chat-action-btn {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.375rem 0.5rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--text-secondary);
  font-weight: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.chat-action-btn:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
  transform: scale(1.05);
}

.chat-action-btn:active {
  transform: scale(0.95);
}

.chat-action-btn:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

.chat-action-btn svg {
  display: block;
}

/* Messages Container */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: min(420px, calc(100vh - 400px));
  min-height: 320px;
  background: var(--bg-primary);
  scroll-behavior: smooth;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
  margin: 4px 0;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 10px;
  transition: background 0.2s ease;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
}

/* Message Bubbles */
.chat-message {
  display: flex;
  flex-direction: column;
  max-width: 85%;
  animation: messageSlide 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-message.user {
  align-self: flex-end;
}

.chat-message.assistant {
  align-self: flex-start;
}

.message-content {
  padding: 0.875rem 1.125rem;
  border-radius: 12px;
  line-height: 1.6;
  word-wrap: break-word;
  word-break: break-word;
  font-size: 0.9375rem;
  transition: transform 0.2s ease;
}

.chat-message.user .message-content {
  background: var(--accent-primary);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-message.assistant .message-content {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--border-color);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.message-content:hover {
  transform: translateY(-1px);
}

.message-time {
  font-size: 0.7rem;
  color: var(--text-tertiary);
  margin-top: 0.375rem;
  padding: 0 0.5rem;
  font-weight: 500;
}

.chat-message.user .message-time {
  text-align: right;
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  gap: 6px;
  padding: 0.875rem 1.125rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-tertiary);
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* Quick Actions */
.chat-quick-actions {
  display: flex;
  gap: 0.625rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-card);
  overflow-x: auto;
  flex-shrink: 0;
}

.chat-quick-actions::-webkit-scrollbar {
  height: 4px;
}

.chat-quick-actions::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 10px;
}

.chat-quick-actions button {
  flex-shrink: 0;
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
}

.chat-quick-actions button:hover:not(:disabled) {
  background: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--accent-primary);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-quick-actions button:active:not(:disabled) {
  transform: translateY(0);
}

.chat-quick-actions button:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

.chat-quick-actions button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Input Area */
.chat-input-area {
  display: flex;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-card);
  flex-shrink: 0;
}

.chat-input-area input {
  flex: 1;
  padding: 0.875rem 1rem;
  border: 2px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.9375rem;
  font-family: inherit;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-input-area input:focus {
  outline: none;
  border-color: var(--accent-primary);
  background: var(--bg-card);
  box-shadow: 0 0 0 3px rgba(35, 134, 54, 0.1);
}

.chat-input-area input::placeholder {
  color: var(--text-tertiary);
}

.chat-input-area input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn {
  padding: 0.875rem 1.125rem;
  background: var(--accent-primary);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  min-width: 48px;
}

.send-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
}

.send-btn:active:not(:disabled) {
  transform: translateY(0);
}

.send-btn:focus-visible {
  outline: 3px solid var(--accent-primary);
  outline-offset: 2px;
}

.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ========================================
   Responsive Breakpoints
   ======================================== */

/* Tablet and below (1024px and down) */
@media (max-width: 1024px) {
  .chat-panel {
    width: min(400px, calc(100vw - 48px));
    max-height: min(600px, calc(100vh - 140px));
  }
}

/* Small Tablet (900px and down) */
@media (max-width: 900px) {
  .chat-panel {
    width: min(380px, calc(100vw - 48px));
    max-height: min(560px, calc(100vh - 140px));
  }

  .chat-messages {
    max-height: min(380px, calc(100vh - 360px));
  }
}

/* Mobile Landscape / Large Phone (768px and down) */
@media (max-width: 768px) {
  .chat-backdrop {
    display: block;
  }

  .chat-panel {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    max-width: 100%;
    max-height: 100%;
    height: 100%;
    border-radius: 0;
    border: none;
  }

  .chat-panel-enter-from {
    transform: translateY(100%);
    opacity: 1;
  }

  .chat-panel-leave-to {
    transform: translateY(100%);
    opacity: 1;
  }

  .chat-header {
    padding: 1rem 1.25rem;
    border-bottom: 2px solid var(--border-color);
  }

  .chat-messages {
    max-height: none;
    min-height: auto;
    flex: 1;
    padding: 1.25rem;
  }

  .chat-quick-actions {
    padding: 0.875rem 1.25rem;
    gap: 0.5rem;
  }

  .chat-quick-actions button {
    padding: 0.5rem 0.875rem;
    font-size: 0.8125rem;
  }

  .chat-input-area {
    padding: 1rem 1.25rem;
    gap: 0.625rem;
  }

  .chat-fab {
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
  }

  .chat-icon {
    width: 26px;
    height: 26px;
  }
}

/* Mobile Portrait / Standard Phone (480px and down) */
@media (max-width: 480px) {
  .chat-header {
    padding: 0.875rem 1rem;
  }

  .chat-title {
    font-size: 0.9375rem;
  }

  .chat-messages {
    padding: 1rem;
    gap: 0.875rem;
  }

  .message-content {
    font-size: 0.875rem;
    padding: 0.75rem 1rem;
  }

  .message-time {
    font-size: 0.65rem;
  }

  .chat-quick-actions {
    padding: 0.75rem 1rem;
    gap: 0.5rem;
  }

  .chat-quick-actions button {
    padding: 0.5rem 0.75rem;
    font-size: 0.8125rem;
  }

  .chat-input-area {
    padding: 0.875rem 1rem;
  }

  .chat-input-area input {
    padding: 0.75rem 0.875rem;
    font-size: 0.875rem;
  }

  .send-btn {
    padding: 0.75rem 1rem;
    min-width: 44px;
  }

  .chat-fab {
    bottom: 16px;
    right: 16px;
    width: 56px;
    height: 56px;
  }

  .chat-icon {
    width: 24px;
    height: 24px;
  }
}

/* Small Phone (360px and down) */
@media (max-width: 360px) {
  .chat-header {
    padding: 0.75rem 0.875rem;
  }

  .chat-title {
    font-size: 0.875rem;
  }

  .chat-messages {
    padding: 0.875rem;
  }

  .message-content {
    font-size: 0.8125rem;
    padding: 0.625rem 0.875rem;
  }

  .chat-quick-actions {
    padding: 0.625rem 0.875rem;
  }

  .chat-quick-actions button {
    padding: 0.5rem 0.625rem;
    font-size: 0.75rem;
  }

  .chat-input-area {
    padding: 0.75rem 0.875rem;
  }

  .chat-input-area input {
    font-size: 0.8125rem;
  }
}

/* Keyboard visible - reduce height on mobile */
@media (max-width: 768px) and (max-height: 500px) {
  .chat-messages {
    min-height: auto;
  }

  .chat-quick-actions {
    display: none;
  }
}

/* Accessibility - Prefers Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
