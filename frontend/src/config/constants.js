/**
 * Application-wide constants
 */

// Chat constraints
export const MESSAGE_MAX_LENGTH = 2000  // Maximum characters in a chat message
export const CHAT_HISTORY_LIMIT = 4   // Maximum messages to send in history (reduced for speed)

// Reading time calculation
export const WORDS_PER_MINUTE = 200    // Average reading speed

// Pagination
export const DEFAULT_PAGE_SIZE = 10    // Default items per page

// Storage keys
export const STORAGE_KEYS = {
  chatMessages: 'chat_messages',
  recentSearches: 'recent_searches',
}
