import { ref } from 'vue'
import { useBlog } from './useBlog'
import { useProfessionalInfo } from './useProfessionalInfo'
import { useAnalytics } from './useAnalytics'
import { CONTACT } from '../config/contact'
import { API_ENDPOINTS, API_CONFIG } from '../config/api'

// Shared state across all instances
const messages = ref([])
const isOpen = ref(false)
const isTyping = ref(false)
const blogPosts = ref([])
const contextLoaded = ref(false)
// Global abort controller for canceling requests
let currentAbortController = null
// Module-level cache for dynamic responses
let _dynamicCache = null
let _cacheGenerated = false

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

// Load context (blog posts + professional info) once on first chat open
const loadContext = async () => {
  if (!contextLoaded.value) {
    // Load blog posts from API
    const { fetchPosts } = useBlog()
    await fetchPosts()
    const { posts } = useBlog()
    blogPosts.value = posts.value

    // Load professional info from shared composable (dynamic, no rebuild needed)
    const { loadProfessionalInfo } = useProfessionalInfo()
    await loadProfessionalInfo()

    contextLoaded.value = true
  }
}

// Generate dynamic cache from live professional data
// Responses are written conversationally, like the AI would respond
const generateDynamicCache = (professionalInfo) => {
  if (!professionalInfo) return null

  const currentRole = professionalInfo.experience?.find(e => e.current)
  const skills = professionalInfo.skills || {}

  // Group skills by category for better presentation
  const skillsByCategory = []
  if (skills.languages?.length) skillsByCategory.push(`**Languages:** ${skills.languages.slice(0, 5).join(', ')}`)
  if (skills.frameworks?.length) skillsByCategory.push(`**Frameworks:** ${skills.frameworks.slice(0, 5).join(', ')}`)
  if (skills.ai_ml?.length) skillsByCategory.push(`**AI/ML:** ${skills.ai_ml.slice(0, 5).join(', ')}`)
  if (skills.databases?.length) skillsByCategory.push(`**Databases:** ${skills.databases.join(', ')}`)
  if (skills.cloud?.length) skillsByCategory.push(`**Cloud:** ${skills.cloud.slice(0, 5).join(', ')}`)

  const education = professionalInfo.education || []
  const educationText = education.length > 0
    ? education.map(e => `${e.degree} from ${e.institution} (${e.dates})`).join(', and ')
    : ''

  return {
    // Contact information - friendly and helpful
    "contact": `You can reach Richwell through:\n\n📧 **Email:** ${professionalInfo.personal?.email}\n🔗 **LinkedIn:** ${professionalInfo.personal?.linkedIn}\n\nFeel free to reach out about opportunities, collaborations, or just to connect!`,

    "email": `Richwell's email is **${professionalInfo.personal?.email}**. Feel free to reach out!`,

    // Current role - conversational and detailed
    "current role": currentRole
      ? `Richwell is currently working as an **${currentRole.title}** at **${currentRole.company}**.\n\n${currentRole.description}\n\nHe's been in this role since ${currentRole.dates}.`
      : "Richwell is currently seeking new opportunities.",

    // Skills - organized by category
    "skills": `Richwell has expertise across several areas:\n\n${skillsByCategory.join('\n')}\n\nThese skills span full-stack development, AI/ML engineering, and cloud infrastructure. Would you like to know more about any specific area?`,

    // Education - narrative style
    "education": educationText
      ? `Richwell earned his ${educationText}. His academic focus included ${education[0]?.focus?.join(', ') || 'Computer Science and AI'}${education[0]?.gpa ? `, graduating with a ${education[0].gpa} GPA` : ''}.`
      : '',

    // Location - friendly
    "location": `Richwell is based in **${professionalInfo.personal?.location}**. He's open to remote work and relocation opportunities.`,
  }
}

// Find cached response using conservative matching
// Only matches very simple, direct questions - complex questions go to API
const findCachedResponse = (userMessage) => {
  if (!_cacheGenerated || !_dynamicCache) return null

  const query = userMessage.toLowerCase().trim()

  // Exclude complex questions (multiple clauses, summaries, analysis, comparisons)
  const complexPatterns = [
    /\band\b.*\band\b/,  // Multiple "and" (e.g., "skills and experience")
    /summary|summarize|tell me about|describe|explain|why|how/i,  // Requests for summaries/explanations
    /years of|how many|how long/i,  // Calculations/counts
    /professional summary|career|background/i,  // Complex career questions
    /compare|difference|versus|vs/i,  // Comparisons
    /should|would|recommend/i,  // Advice/recommendations
  ]

  for (const pattern of complexPatterns) {
    if (pattern.test(query)) {
      return null // Complex question - use API
    }
  }

  // Very specific patterns for simple, direct questions only
  // Contact info - must be asking specifically for email/contact
  if (/^(what('| i)s )?((your|his|the) )?(email|contact)(\s*(address|info))?[?]?$/i.test(query) ||
      /^how (can|do) (i|we) (contact|reach) (you|him)[?]?$/i.test(query)) {
    return _dynamicCache["contact"]
  }

  // Skills - must be asking specifically for skills/technologies
  if (/^(what('| i)s )?((your|his|the) )?(skills?|technologies|tech stack)[?]?$/i.test(query) ||
      /^what (skills?|technologies) (do|does) (you|he) (have|know|use)[?]?$/i.test(query)) {
    return _dynamicCache["skills"]
  }

  // Location - must be asking specifically for location
  if (/^(where|location)[?]?$/i.test(query) ||
      /^where (is|are) (you|he)( located| based)?[?]?$/i.test(query)) {
    return _dynamicCache["location"]
  }

  // Education - must be asking specifically for education/degree
  if (/^(what('| i)s )?((your|his|the) )?(education|degree)[?]?$/i.test(query) ||
      /^where did (you|he) (study|graduate|go to school)[?]?$/i.test(query)) {
    return _dynamicCache["education"]
  }

  // Current role - must be asking specifically about current job
  if (/^(what('| i)s )?((your|his|the) )?current (role|job|position)[?]?$/i.test(query) ||
      /^what (do|does) (you|he) do( now)?[?]?$/i.test(query)) {
    return _dynamicCache["current role"]
  }

  return null // No simple match - use API for better response
}

// Enhanced preloadContext with cache generation
const preloadContext = async () => {
  await loadContext()

  // Generate cache from loaded data
  try {
    const { professionalInfo } = useProfessionalInfo()
    _dynamicCache = generateDynamicCache(professionalInfo.value)
    _cacheGenerated = true
    console.log('[Chat] Context + cache ready')
  } catch (error) {
    console.warn('[Chat] Cache generation failed, using API only:', error)
    _cacheGenerated = false
  }
}

// Build site context for API
const getSiteContext = () => {
  const { professionalInfo } = useProfessionalInfo()
  return {
    professional: professionalInfo.value,
    blogs: blogPosts.value.map(post => ({
      title: post.title,
      date: post.date,
      tags: post.tags
      // Removed excerpt to reduce payload size (not critical for chatbot)
    }))
  }
}

// Chat storage version (increment when making breaking changes)
const CHAT_VERSION = 2

// Save messages to localStorage
const saveMessages = () => {
  try {
    const data = {
      version: CHAT_VERSION,
      messages: messages.value
    }
    localStorage.setItem('chatMessages', JSON.stringify(data))
  } catch (e) {
    console.error('Failed to save messages:', e)
  }
}

// Load messages from localStorage
const loadMessages = () => {
  try {
    const saved = localStorage.getItem('chatMessages')
    if (saved) {
      const data = JSON.parse(saved)

      // Check version - clear if outdated
      if (!data.version || data.version < CHAT_VERSION) {
        console.log('Clearing outdated chat cache')
        localStorage.removeItem('chatMessages')
        return
      }

      // Load messages
      const loadedMessages = data.messages || data // Support old format temporarily
      // Clean up any streaming flags from interrupted sessions
      messages.value = loadedMessages.map(msg => ({
        ...msg,
        isStreaming: false // Reset streaming state
      }))
    }
  } catch (e) {
    console.error('Failed to load messages:', e)
    // Clear corrupted data
    localStorage.removeItem('chatMessages')
  }
}

// Helper function to simulate streaming for instant messages
const simulateStreaming = (messageId, fullContent, delay = 2) => {
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
        // Mark as not streaming
        messages.value[messageIndex].content = fullContent
        messages.value[messageIndex].isStreaming = false
        saveMessages()
        resolve()
        return
      }

      // Add next character (cursor is rendered separately in ChatAssistant.vue)
      currentIndex++
      messages.value[messageIndex].content = fullContent.substring(0, currentIndex)
    }, delay)
  })
}

export function useChatAssistant() {
  const { trackChatInteraction } = useAnalytics()

  const sendMessage = async (userInput) => {
    if (!userInput.trim()) return

    // Defensive: Clear any stuck typing state from previous errors
    isTyping.value = false

    console.log('[Chat] Sending message:', userInput.substring(0, 50) + '...')

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
      await simulateStreaming(errorId, 'Your message is too long. Please keep it under 2000 characters.', 2)
      return
    }

    // Check cache first
    const cachedResponse = findCachedResponse(userInput)

    if (cachedResponse) {
      console.log('[Chat] ✅ Cache hit!')

      // Add user message
      messages.value.push({
        id: generateUUID(),
        type: 'user',
        content: userInput,
        timestamp: new Date()
      })

      // Add cached response with typing animation
      const responseId = generateUUID()
      messages.value.push({
        id: responseId,
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      })

      // Show typing animation (fast - 2ms per character)
      await simulateStreaming(responseId, cachedResponse, 2)

      // Ensure typing state is cleared
      isTyping.value = false

      return // Skip API call!
    }

    // Cache miss - continue with existing API logic
    console.log('[Chat] ❌ Cache miss, calling API...')

    // Add user message
    messages.value.push({
      id: generateUUID(),
      type: 'user',
      content: userInput,
      timestamp: new Date()
    })

    // Show typing indicator
    isTyping.value = true
    console.log('[Chat] Typing indicator ON')

    try {
      // Get last 10 messages for context (5 exchanges) - EXCLUDING current message
      const conversationHistory = messages.value
        .slice(0, -1)  // Exclude the message we just added
        .slice(-API_CONFIG.historyLimit)     // Get last N previous messages
        .map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.content
        }))

      console.log('[Chat] Attempting streaming...')
      // Use streaming with automatic fallback to regular mode if it fails
      await sendMessageStreaming(userInput, conversationHistory)
      console.log('[Chat] Streaming complete')

    } catch (error) {
      console.error('[Chat] ERROR in sendMessage:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      })

      // Add error message with streaming animation
      const errorId = generateUUID()
      let errorContent

      // Specific message for cancellations
      if (error.name === 'AbortError') {
        errorContent = `Request canceled. Feel free to ask another question.`
      } else {
        errorContent = `I'm having trouble right now. Please reach out to Richwell directly at ${CONTACT.getContactMessage()} for assistance.`
      }

      messages.value.push({
        id: errorId,
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true
      })

      await simulateStreaming(errorId, errorContent, 2)
    } finally {
      console.log('[Chat] Typing indicator OFF')
      isTyping.value = false
    }
  }

  // Streaming implementation using fetch + SSE with timeout
  const sendMessageStreaming = async (userInput, conversationHistory) => {
    let assistantMessageId = null

    try {
      console.log('[Chat] Creating fetch request with 30s timeout')

      // Create abort controller for manual cancel only (no automatic timeout)
      // User can manually cancel with the red X button anytime
      currentAbortController = new AbortController()

      // REMOVED: Automatic timeout
      // Reason: API can take 3-5 minutes but still gives good answers
      // User has manual cancel button if they don't want to wait

      const response = await fetch(`${API_ENDPOINTS.chatStream}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: userInput,
          history: conversationHistory,
          site_context: getSiteContext()
        }),
        signal: currentAbortController.signal
      })

      currentAbortController = null // Clear after successful request
      console.log('[Chat] Got response:', response.status)

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

      // Defensive: Explicitly clear typing state here too
      isTyping.value = false
      console.log('[Chat] Streaming completed, typing cleared')

      // Save to localStorage
      saveMessages()

    } catch (error) {
      console.error('[Chat] Streaming error:', error.name, error.message)

      // Remove placeholder message if it was created
      if (assistantMessageId) {
        const index = messages.value.findIndex(m => m.id === assistantMessageId)
        if (index !== -1) {
          messages.value.splice(index, 1)
        }
      }

      // If manually canceled, show message
      if (error.name === 'AbortError') {
        console.error('[Chat] Request manually canceled by user')

        const errorId = generateUUID()
        const errorContent = `Request canceled. Feel free to ask another question or contact Richwell at ${CONTACT.email}.`

        messages.value.push({
          id: errorId,
          type: 'assistant',
          content: '',
          timestamp: new Date(),
          isStreaming: true
        })

        await simulateStreaming(errorId, errorContent, 2)
        return
      }

      // For other errors, fallback to regular mode
      console.log('[Chat] Using fallback regular mode')
      await sendMessageRegular(userInput, conversationHistory)
    }
  }

  // Regular (non-streaming) implementation
  const sendMessageRegular = async (userInput, conversationHistory) => {
    console.log('[Chat] Regular mode: Sending request to', API_ENDPOINTS.chat)

    // Create abort controller for manual cancel only
    currentAbortController = new AbortController()

    const response = await fetch(`${API_ENDPOINTS.chat}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userInput,
        history: conversationHistory,
        site_context: getSiteContext()
      }),
      signal: currentAbortController.signal
    })

    currentAbortController = null // Clear after successful request
    console.log('[Chat] Regular mode: Got response', response.status)

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

      await simulateStreaming(errorId, errorMessage, 2)
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

    await simulateStreaming(responseId, responseContent, 2)

    // Defensive: Explicitly clear typing state
    isTyping.value = false
    console.log('[Chat] Regular mode completed, typing cleared')
  }

  const toggleChat = async () => {
    isOpen.value = !isOpen.value

    // Track chat open/close
    if (isOpen.value) {
      trackChatInteraction('chat_opened')

      // Try loading saved messages first
      if (messages.value.length === 0) {
        loadMessages()
      }

      // If still no messages, add welcome message with streaming animation IMMEDIATELY
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

        // Start streaming immediately, don't wait for context loading
        simulateStreaming(welcomeId, welcomeContent, 2)
      }

      // Load context in background (don't await - this can happen in parallel)
      loadContext()
    } else {
      trackChatInteraction('chat_closed')
    }
  }

  const clearChat = async () => {
    // Clear all messages
    messages.value = []
    // Clear localStorage
    localStorage.removeItem('chatMessages')

    // Re-add welcome message with streaming animation
    const welcomeId = generateUUID()
    const welcomeContent = `Hi! I'm Richwell's virtual assistant. I can answer questions about his education, work experience, projects, skills, and background. What would you like to know?`

    messages.value.push({
      id: welcomeId,
      type: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    })

    await simulateStreaming(welcomeId, welcomeContent, 2)
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

  const cancelRequest = () => {
    console.log('[Chat] User canceled request')
    if (currentAbortController) {
      currentAbortController.abort('User canceled request')
      currentAbortController = null
    }
    isTyping.value = false

    // Add cancelation message
    const cancelId = generateUUID()
    messages.value.push({
      id: cancelId,
      type: 'assistant',
      content: 'Request canceled.',
      timestamp: new Date(),
      isStreaming: false
    })
    saveMessages()
  }

  return {
    messages,
    isOpen,
    isTyping,
    sendMessage,
    toggleChat,
    clearChat,
    sendQuickMessage,
    formatTime,
    cancelRequest,
    preloadContext  // Expose enhanced preloadContext with cache generation
  }
}
