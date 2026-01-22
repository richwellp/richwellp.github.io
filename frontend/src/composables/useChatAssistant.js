import { ref } from 'vue'
import { professionalInfo } from '../data/professionalInfo'
import { useBlog } from './useBlog'

// Shared state across all instances
const messages = ref([])
const isOpen = ref(false)
const isTyping = ref(false)
const blogPosts = ref([])
const contextLoaded = ref(false)

const API_BASE = import.meta.env.PROD
  ? 'https://richwellp-github-io.vercel.app'
  : 'http://localhost:5000'

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

export function useChatAssistant() {
  const sendMessage = async (userInput) => {
    if (!userInput.trim()) return

    // Add user message
    messages.value.push({
      id: Date.now(),
      type: 'user',
      content: userInput,
      timestamp: new Date()
    })

    // Show typing indicator
    isTyping.value = true

    try {
      // Get last 10 messages for context (5 exchanges)
      const conversationHistory = messages.value
        .slice(-10)
        .map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.content
        }))

      const response = await fetch(`${API_BASE}/chat`, {
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
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()

      // Add assistant response
      messages.value.push({
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response || data.message || 'Sorry, I received an empty response.',
        timestamp: new Date()
      })
    } catch (error) {
      console.error('Chat error:', error)

      // Add error message with email fallback
      messages.value.push({
        id: Date.now() + 1,
        type: 'assistant',
        content: `I'm having trouble connecting right now. You can reach Richwell directly at richwell.perez@gmail.com or via LinkedIn at linkedin.com/in/richwell-perez.`,
        timestamp: new Date()
      })
    } finally {
      isTyping.value = false
    }
  }

  const toggleChat = async () => {
    isOpen.value = !isOpen.value

    // Load context and add welcome message on first open
    if (isOpen.value && messages.value.length === 0) {
      await loadContext()
      messages.value.push({
        id: Date.now(),
        type: 'assistant',
        content: `Hi! I'm Richwell's virtual assistant. I can answer questions about his education, work experience, projects, skills, and background. What would you like to know?`,
        timestamp: new Date()
      })
    }
  }

  const clearChat = () => {
    // Keep only welcome message
    if (messages.value.length > 0) {
      messages.value = [messages.value[0]]
    }
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
