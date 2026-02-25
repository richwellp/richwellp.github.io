/**
 * useSanitizer - Composable for sanitizing HTML content
 * Provides XSS protection for user-generated or markdown-rendered content
 */
import DOMPurify from 'dompurify'

/**
 * Configure DOMPurify with safe defaults
 */
const defaultConfig = {
  // Allow safe HTML tags
  ALLOWED_TAGS: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'strong', 'em', 'u', 's', 'del', 'ins',
    'a', 'img',
    'ul', 'ol', 'li',
    'blockquote', 'code', 'pre',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span'
  ],

  // Allow safe attributes
  ALLOWED_ATTR: [
    'href', 'src', 'alt', 'title',
    'class', 'id',
    'target', 'rel',
    'width', 'height'
  ],

  // Ensure links are safe
  ALLOW_DATA_ATTR: false,

  // Add target="_blank" and rel="noopener noreferrer" to external links
  ADD_ATTR: ['target', 'rel']
}

/**
 * Sanitize HTML string to prevent XSS attacks
 * @param {string} dirty - Potentially unsafe HTML string
 * @param {Object} config - Optional DOMPurify configuration
 * @returns {string} Sanitized HTML string
 */
export function sanitizeHtml(dirty, config = {}) {
  if (!dirty || typeof dirty !== 'string') {
    return ''
  }

  const mergedConfig = { ...defaultConfig, ...config }
  const clean = DOMPurify.sanitize(dirty, mergedConfig)

  return clean
}

/**
 * Composable for using sanitizer in Vue components
 */
export function useSanitizer() {
  return {
    sanitizeHtml
  }
}
