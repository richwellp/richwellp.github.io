# Chatbot Speed Optimization - Design Document

**Date:** February 24, 2026
**Goal:** Make chatbot give fast AND correct answers (currently: correct but 5 minutes)
**Constraint:** Free solutions only (no monthly costs)

---

## Problem Analysis

**Current State:**
- ✅ Answers are correct and high quality
- ❌ ALL questions take 5 minutes (even simple ones like "What's your email?")
- ❌ Happens on first use of the day (cold start)
- ❌ Context loads only when chat opens (lazy loading)

**Root Causes:**
1. **No pre-warming**: Context loads on-demand when first message sent
2. **No caching**: Gemini API called for every question (context caching requires paid tier)
3. **Cold start**: First API call of the day is slowest
4. **Sequential loading**: Context → API call → Wait → Response

**Measurements:**
- Resume PDF: 148KB (6,198 characters, ~1,549 tokens)
- Professional JSON: 11KB (185 lines)
- Total context sent: ~3,000-4,000 tokens per request
- Gemini free tier: 15 RPM, 1,500 RPD, no context caching support

---

## Solution: Pre-Warming + Dynamic Response Caching

### Architecture Overview

**Before:**
```
User opens page → ... → User opens chat → Load context → Send message → Wait 5 min → Response
```

**After:**
```
User opens page → Pre-load context + Generate cache (background)
                                                 ↓
User opens chat → Show welcome (instant typing animation)
                                                 ↓
User sends message → Check cache first → If hit: Instant (<1s)
                                       → If miss: API (~30-90s with pre-warmed context)
```

**Expected Performance:**
- Welcome message: Instant with typing animation ✨
- Contact/Email/Skills: <1 second (cache hit) ⚡
- Complex questions: 30-90 seconds (API, pre-warmed) 🚀
- Cache hit rate: ~50% of questions

---

## Component 1: Pre-Warming Context

### Current Implementation
Already exists but needs enhancement:

**App.vue (line 21-26):**
```javascript
onMounted(async () => {
  fetchPosts()
  await loadProfessionalInfo()
  preloadContext().catch(err => console.warn('Failed to preload chat context:', err))
})
```

**useChatAssistant.js (line 30-45):**
```javascript
const loadContext = async () => {
  if (!contextLoaded.value) {
    const { fetchPosts } = useBlog()
    await fetchPosts()
    const { posts } = useBlog()
    blogPosts.value = posts.value

    const { loadProfessionalInfo } = useProfessionalInfo()
    await loadProfessionalInfo()

    contextLoaded.value = true
  }
}
```

### Enhancement Needed
Add cache generation after loading context:

```javascript
// Add module-level cache state
let _dynamicCache = null
let _cacheGenerated = false

// Enhanced preloadContext
const preloadContext = async () => {
  await loadContext() // Load blog + professional data

  // NEW: Generate cache from loaded data
  const { professionalInfo } = useProfessionalInfo()
  _dynamicCache = generateDynamicCache(professionalInfo.value)
  _cacheGenerated = true

  console.log('[Chat] Context + cache ready')
}
```

---

## Component 2: Dynamic Cache Generation

### Cache Generation Function

```javascript
// Generate cache from live data (always accurate)
function generateDynamicCache(professionalInfo) {
  if (!professionalInfo) return null

  const currentRole = professionalInfo.experience?.find(e => e.current)
  const allSkills = professionalInfo.skills ? Object.values(professionalInfo.skills).flat() : []

  return {
    // Contact information
    "contact": `You can reach Richwell at ${professionalInfo.personal?.email} or ${professionalInfo.personal?.linkedIn}`,
    "email": professionalInfo.personal?.email || "",

    // Current role
    "current role": currentRole ?
      `${currentRole.title} at ${currentRole.company}. ${currentRole.description}` : "",
    "what does he do": currentRole?.description || "",

    // Skills (top 15)
    "skills": allSkills.slice(0, 15).join(', '),

    // Education
    "education": professionalInfo.education?.map(e =>
      `${e.degree} from ${e.shortName} (${e.dates})`
    ).join('; ') || "",

    // Location
    "location": professionalInfo.personal?.location || "",

    // Experience summary
    "experience": professionalInfo.experience?.slice(0, 2).map(e =>
      `${e.title} at ${e.company} (${e.dates})`
    ).join('; ') || "",
  }
}
```

**Key Design Decision:**
- Pass `professionalInfo` as parameter (not call composable inside function)
- Cache generated AFTER data loads (in `preloadContext`)
- Always uses live data (never stale)

---

## Component 3: Cache Matching Logic

### Fuzzy Matching Function

```javascript
function findCachedResponse(userMessage) {
  if (!_cacheGenerated || !_dynamicCache) return null

  const query = userMessage.toLowerCase().trim()

  // Direct keyword matches
  for (const [keyword, response] of Object.entries(_dynamicCache)) {
    if (query.includes(keyword)) {
      return response
    }
  }

  // Pattern matching for common question variations
  if (/email|contact|reach/.test(query)) {
    return _dynamicCache["contact"]
  }
  if (/current (role|job|position)|what (does|do) (he|you) do/.test(query)) {
    return _dynamicCache["current role"]
  }
  if (/skills?|technologies|tech stack/.test(query)) {
    return _dynamicCache["skills"]
  }
  if (/education|degree|university|college/.test(query)) {
    return _dynamicCache["education"]
  }
  if (/where|location|based/.test(query)) {
    return _dynamicCache["location"]
  }
  if (/experience|work history|background/.test(query)) {
    return _dynamicCache["experience"]
  }

  return null // No match - use API
}
```

**Coverage:**
- Direct keyword: "contact", "email", "skills", etc.
- Variations: "what does he do", "where is he", etc.
- Estimated cache hit rate: 40-60%

---

## Component 4: Modified sendMessage Flow

### Updated Logic

```javascript
const sendMessage = async (userInput) => {
  if (!userInput.trim()) return

  // Defensive: Clear any stuck typing state
  isTyping.value = false

  console.log('[Chat] Sending message:', userInput.substring(0, 50) + '...')

  // Track message sent
  trackChatInteraction('message_sent', { messageLength: userInput.length })

  // NEW: Check cache first
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

    return // Skip API call!
  }

  // Cache miss - continue with existing API logic
  console.log('[Chat] ❌ Cache miss, calling API...')

  // Validate message length
  if (userInput.length > 2000) {
    // ... existing validation logic ...
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
  console.log('[Chat] Typing indicator ON')

  try {
    // ... existing API call logic (unchanged) ...
  } catch (error) {
    // ... existing error handling (unchanged) ...
  } finally {
    console.log('[Chat] Typing indicator OFF')
    isTyping.value = false
  }
}
```

**Flow:**
1. Check cache first (instant)
2. If cache hit: Show typing animation + cached response
3. If cache miss: Existing API flow (30-90s with pre-warmed context)

---

## Component 5: Welcome Message (Already Working)

### Current Implementation (Verified Correct)

**useChatAssistant.js (line 492-509):**
```javascript
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
```

**Status:** ✅ Already correct
- Welcome message is hardcoded (no API call)
- Shows typing animation immediately on chat open
- No changes needed

---

## Implementation Summary

### Files to Modify

1. **`frontend/src/composables/useChatAssistant.js`**
   - Add `_dynamicCache` and `_cacheGenerated` module variables
   - Add `generateDynamicCache(professionalInfo)` function
   - Add `findCachedResponse(userMessage)` function
   - Update `preloadContext()` to generate cache
   - Update `sendMessage()` to check cache first

### Files Not Modified
- ✅ `App.vue` - Already pre-loads context on mount
- ✅ `ChatAssistant.vue` - Welcome animation already works
- ✅ Backend files - No changes needed

### Estimated Changes
- Lines added: ~120 lines
- Lines modified: ~15 lines
- Files changed: 1 file
- Effort: 2-3 hours development + testing

---

## Performance Impact

### Before Optimization

| Question Type | Time |
|---------------|------|
| Welcome message | Instant (hardcoded) ✅ |
| Simple (email, contact) | 5 minutes |
| Medium (skills, education) | 5 minutes |
| Complex (experience, projects) | 5 minutes |

### After Optimization

| Question Type | Time | Improvement |
|---------------|------|-------------|
| Welcome message | Instant with typing | No change ✅ |
| Simple (cached) | <1 second | **300x faster** ⚡ |
| Medium (cached) | <1 second | **300x faster** ⚡ |
| Complex (API) | 30-90 seconds | **3-6x faster** 🚀 |

**Expected cache hit rate:** 40-60%
**API quota savings:** ~50% reduction
**User satisfaction:** Significantly improved

---

## Testing Strategy

### Manual Testing

1. **Pre-warming test:**
   - Fresh page load
   - Check console for "[Chat] Context + cache ready"
   - Verify loads before opening chat

2. **Cache hit test:**
   - Ask: "What's your email?" → Should be <1s
   - Ask: "What are your skills?" → Should be <1s
   - Check console for "[Chat] ✅ Cache hit!"

3. **Cache miss test:**
   - Ask: "Why should I hire him?" (complex)
   - Should call API (30-90s)
   - Check console for "[Chat] ❌ Cache miss, calling API..."

4. **Dynamic cache test:**
   - Edit `professionalInfo.json` (change email)
   - Reload page
   - Ask for email
   - Verify response has new email (not stale)

5. **Welcome animation test:**
   - Open chat
   - Verify typing animation starts immediately
   - Verify no API call made (check console)

### Console Logs to Verify

```
# On page load
[Chat] Context + cache ready

# On cached question
[Chat] Sending message: What's your email?...
[Chat] ✅ Cache hit!

# On API question
[Chat] Sending message: Why should I hire him?...
[Chat] ❌ Cache miss, calling API...
[Chat] Attempting streaming...
[Chat] Streaming complete
```

---

## Error Handling

### Cache Generation Failure
```javascript
try {
  _dynamicCache = generateDynamicCache(professionalInfo.value)
  _cacheGenerated = true
} catch (error) {
  console.warn('[Chat] Cache generation failed, using API only:', error)
  _cacheGenerated = false // Fail gracefully to API
}
```

### Missing Data Handling
- If `professionalInfo.value` is null → Return null cache
- If fields missing → Use empty string fallbacks
- Cache always optional → API works without it

---

## Benefits

### For Users
- ✅ Instant responses for common questions
- ✅ Much faster responses for complex questions
- ✅ Welcome message feels responsive
- ✅ Always accurate (cache from live data)

### For System
- ✅ 50% reduction in API calls (quota savings)
- ✅ Lower latency for majority of queries
- ✅ Better resource utilization
- ✅ No paid services required

### For Maintenance
- ✅ Cache auto-updates from data changes
- ✅ Zero manual cache management
- ✅ Simple, maintainable code
- ✅ Easy to add more cached patterns

---

## Future Enhancements (Out of Scope)

- Cache to localStorage for persistence across sessions
- Track cache hit/miss analytics
- Add more sophisticated NLP for question matching
- Implement cache warming API endpoint
- A/B test different cache strategies

---

## Approval

**Design Status:** ✅ Validated
**Implementation Ready:** Yes
**Estimated Effort:** 2-3 hours
**Risk Level:** Low (graceful fallbacks)

---

**Next Steps:**
1. Create implementation plan with detailed code changes
2. Set up git worktree for isolated development
3. Implement in task batches with testing
4. Verify performance improvements
5. Deploy to production
