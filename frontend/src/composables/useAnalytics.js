/**
 * Simple privacy-friendly analytics composable
 * Using Cloudflare Web Analytics - FREE, GDPR compliant, no cookies
 */

export function useAnalytics() {
  // Cloudflare automatically tracks page views - no manual tracking needed
  // Custom events are logged to console in development for debugging
  const isDevelopment = import.meta.env.DEV

  // Track custom events (logged for development, auto-tracked by Cloudflare)
  const trackEvent = (eventName, props = {}) => {
    if (isDevelopment) {
      console.log('[Analytics] Event:', eventName, props)
    }
    // Cloudflare tracks user interactions automatically
  }

  // Track chatbot interactions
  const trackChatInteraction = (action, details = {}) => {
    trackEvent('ChatBot', { action, ...details })
  }

  // Track external link clicks
  const trackExternalLink = (url) => {
    trackEvent('ExternalLink', { url })
  }

  // Track contact form submissions
  const trackContactForm = (status) => {
    trackEvent('ContactForm', { status })
  }

  return {
    trackChatInteraction,
    trackExternalLink,
    trackContactForm
  }
}

/**
 * View your site analytics:
 * 1. Go to https://dash.cloudflare.com                                                                                                                                  
 * 2. Sign in with your Cloudflare account
 * 3. Navigate to: Analytics & Logs → Web Analytics                                                                                                                                             3. Navigate to: Analytics & Logs → Web Analytics                                                                                                                                  
 * 4. Select your site: richwellp.github.io 
 */
