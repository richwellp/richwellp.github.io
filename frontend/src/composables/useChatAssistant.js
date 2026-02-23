import { ref } from 'vue'
import { professionalInfo } from '../data/professionalInfo'
import { useBlog } from './useBlog'
import { useAnalytics } from './useAnalytics'
import { CONTACT } from '../config/contact'
import { API_ENDPOINTS, API_CONFIG } from '../config/api'

// Shared state across all instances
const messages = ref([])
const isOpen = ref(false)
const isTyping = ref(false)
const blogPosts = ref([])
const contextLoaded = ref(false)

// UUID generator with fallback for older browsers
const generateUUID = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  // Fallback for older browsers
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

// Load blog posts once on first chat open
const loadContext = async () => {
  if (!contextLoaded.value) {
    const { fetchPosts } = useBlog()
    await fetchPosts()
    const { posts } = useBlog()
    blogPosts.value = posts.value
    contextLoaded.value = true
  }
}

// Build site context for API
const getSiteContext = () => ({
  professional: professionalInfo,
  blogs: blogPosts.value.map(post => ({
    title: post.title,
    date: post.date,
    excerpt: post.excerpt,
    tags: post.tags
  }))
})

// Save messages to localStorage
const saveMessages = () => {
  try {
    localStorage.setItem('chatMessages', JSON.stringify(messages.value))
  } catch (e) {
    console.error('Failed to save messages:', e)
  }
}

// Load messages from localStorage
const loadMessages = () => {
  try {
    const saved = localStorage.getItem('chatMessages')
    if (saved) {
      const loadedMessages = JSON.parse(saved)
      // Clean up any streaming flags from interrupted sessions
      messages.value = loadedMessages.map(msg => ({
        ...msg,
        isStreaming: false // Reset streaming state
      }))
    }
  } catch (e) {
    console.error('Failed to load messages:', e)
  }
}

// Helper function to simulate streaming for instant messages
const simulateStreaming = (messageId, fullContent, delay = 20) => {
  return new Promise((resolve) => {
    const messageIndex = messages.value.findIndex(m => m.id === messageId)
    if (messageIndex === -1) {
      resolve()
      return
    }

    messages.value[messageIndex].isStreaming = true
    messages.value[messageIndex].content = ''

    let currentIndex = 0

    const interval = setInterval(() => {
      if (currentIndex >= fullContent.length) {
        clearInterval(interval)
        messages.value[messageIndex].isStreaming = false
        saveMessages()
        resolve()
        return
      }

      // Add next character
      currentIndex++
      messages.value[messageIndex].content = fullContent.substring(0, currentIndex)
    }, delay)
  })
}

export function useChatAssistant() {
  const { trackChatInteraction } = useAnalytics()

  const sendMessage = async (userInput) => {
    if (!userInput.trim()) return

    // Track message sent
    trackChatInteraction('message_sent', { messageLength: userInput.length })

    // Validate message length (prevent quota waste)
    if (userInput.length > 2000) {
      const errorId = generateUUID()
      messages.value.push({
        id: errorId,
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      })
      await simulateStreaming(errorId, 'Your message is too long. Please keep it under 2000 characters.', 15)
      return
    }

    // Add user message
    messages.value.push({
      id: generateUUID(),
      type: 'user',
      content: userInput,
      timestamp: new Date()
    })

    // Show typing indicator
    isTyping.value = true

    try {
      // Get last 10 messages for context (5 exchanges) - EXCLUDING current message
      const conversationHistory = messages.value
        .slice(0, -1)  // Exclude the message we just added
        .slice(-API_CONFIG.historyLimit)     // Get last N previous messages
        .map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.content
        }))

      // Use streaming with automatic fallback to regular mode if it fails
      await sendMessageStreaming(userInput, conversationHistory)

    } catch (error) {
      console.error('Chat error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      })

      // Add error message with streaming animation
      const errorId = generateUUID()
      const errorContent = `I'm having trouble right now. Please reach out to Richwell directly at ${CONTACT.getContactMessage()} for assistance.`

      messages.value.push({
        id: errorId,
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      })

      await simulateStreaming(errorId, errorContent, 15)
    } finally {
      isTyping.value = false
    }
  }

  // Streaming implementation using fetch + SSE
  const sendMessageStreaming = async (userInput, conversationHistory) => {
    let assistantMessageId = null

    try {
      const response = await fetch(`${API_ENDPOINTS.chatStream}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: userInput,
          history: conversationHistory,
          site_context: getSiteContext()
        })
      })

      if (!response.ok) {
        // Try to get error details
        try {
          const data = await response.json()
          throw new Error(data.error || data.message || 'Streaming failed')
        } catch {
          throw new Error('Streaming failed')
        }
      }

      // Create a placeholder message for streaming
      assistantMessageId = generateUUID()
      messages.value.push({
        id: assistantMessageId,
        type: 'assistant',
        content: '',
        sources: [],
        timestamp: new Date(),
        isStreaming: true
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        // Decode chunk and add to buffer
        buffer += decoder.decode(value, { stream: true })

        // Process complete SSE messages
        const lines = buffer.split('\n')
        buffer = lines.pop() || '' // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))

              // Find the message we're streaming to
              const messageIndex = messages.value.findIndex(m => m.id === assistantMessageId)
              if (messageIndex === -1) continue

              if (data.text) {
                // Append text chunk
                messages.value[messageIndex].content += data.text
              } else if (data.sources) {
                // Set sources
                messages.value[messageIndex].sources = data.sources
              } else if (data.error) {
                // Handle streaming error - show error message
                messages.value[messageIndex].content = data.message || 'An error occurred during streaming.'
                messages.value[messageIndex].isStreaming = false
                saveMessages()
                return
              } else if (data.done) {
                // Streaming complete
                messages.value[messageIndex].isStreaming = false
              }
            } catch (parseError) {
              console.error('Failed to parse SSE data:', parseError)
            }
          }
        }
      }

      // Mark streaming complete if not already marked
      const messageIndex = messages.value.findIndex(m => m.id === assistantMessageId)
      if (messageIndex !== -1) {
        if (messages.value[messageIndex].isStreaming) {
          messages.value[messageIndex].isStreaming = false
        }

        // If no content was received, add fallback message
        if (!messages.value[messageIndex].content || messages.value[messageIndex].content.trim() === '') {
          messages.value[messageIndex].content = `Sorry, I received an empty response. Please try again or contact Richwell at ${CONTACT.email}.`
        }
      }

      // Save to localStorage
      saveMessages()

    } catch (error) {
      console.error('Streaming error:', error)

      // Remove placeholder message if it was created
      if (assistantMessageId) {
        const index = messages.value.findIndex(m => m.id === assistantMessageId)
        if (index !== -1) {
          messages.value.splice(index, 1)
        }
      }

      // Fallback to regular mode
      await sendMessageRegular(userInput, conversationHistory)
    }
  }

  // Regular (non-streaming) implementation
  const sendMessageRegular = async (userInput, conversationHistory) => {
    const response = await fetch(`${API_ENDPOINTS.chat}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userInput,
        history: conversationHistory,
        site_context: getSiteContext()
      })
    })

    // Parse response JSON first to get error details
    let data
    try {
      data = await response.json()
    } catch (parseError) {
      console.error('Failed to parse response JSON:', {
        status: response.status,
        statusText: response.statusText,
        parseError: parseError.message
      })
      throw new Error(`Server returned invalid response (${response.status})`)
    }

    // Check for rate limit or API errors
    if (response.status === 429 || response.status === 500) {
      console.error('Chat API error:', {
        status: response.status,
        error: data.error,
        errorType: data.error_type,
        details: data.error_details
      })

      // Use error message from backend, or provide default
      const errorMessage = data.message || data.error ||
        (data.error_type === 'rate_limit'
          ? `I'm at my free API limit right now (resets daily at midnight Pacific time). Please reach out to Richwell directly at ${CONTACT.getContactMessage()} for immediate assistance.`
          : `I'm having trouble right now. Please reach out to Richwell directly at ${CONTACT.getContactMessage()}.`)

      const errorId = generateUUID()
      messages.value.push({
        id: errorId,
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      })

      await simulateStreaming(errorId, errorMessage, 15)
      return
    }

    // Check for other HTTP errors
    if (!response.ok) {
      console.error('Chat API error:', {
        status: response.status,
        statusText: response.statusText,
        error: data.error,
        errorType: data.error_type,
        details: data.error_details
      })

      throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`)
    }

    // Add successful assistant response with streaming animation
    const responseId = generateUUID()
    const responseContent = data.response || data.message || 'Sorry, I received an empty response.'

    messages.value.push({
      id: responseId,
      type: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    })

    await simulateStreaming(responseId, responseContent, 20)
  }

  const toggleChat = async () => {
    isOpen.value = !isOpen.value

    // Track chat open/close
    if (isOpen.value) {
      trackChatInteraction('chat_opened')
      await loadContext()

      // Try loading saved messages first
      if (messages.value.length === 0) {
        loadMessages()
      }

      // If still no messages, add welcome message with streaming animation
      if (messages.value.length === 0) {
        const welcomeId = generateUUID()
        const welcomeContent = `Hi! I'm Richwell's virtual assistant. I can answer questions about his education, work experience, projects, skills, and background. What would you like to know?`

        messages.value.push({
          id: welcomeId,
          type: 'assistant',
          content: '',
          timestamp: new Date(),
          isStreaming: true
        })

        await simulateStreaming(welcomeId, welcomeContent, 15)
      }
    } else {
      trackChatInteraction('chat_closed')
    }
  }

  const clearChat = () => {
    // Keep only welcome message
    if (messages.value.length > 0) {
      messages.value = [messages.value[0]]
    }
    // Clear localStorage
    saveMessages()
  }

  const sendQuickMessage = async (topic) => {
    const quickMessages = {
      experience: "What's Richwell's work experience?",
      skills: "What technical skills does Richwell have?",
      projects: "Tell me about Richwell's projects",
      contact: "How can I contact Richwell?"
    }

    const message = quickMessages[topic]
    if (message) {
      await sendMessage(message)
    }
  }

  const formatTime = (timestamp) => {
    const date = timestamp instanceof Date ? timestamp : new Date(timestamp)
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }

  return {
    messages,
    isOpen,
    isTyping,
    sendMessage,
    toggleChat,
    clearChat,
    sendQuickMessage,
    formatTime
  }
}
