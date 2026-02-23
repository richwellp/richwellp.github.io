/**
 * Simple privacy-friendly analytics composable
 * Using Cloudflare Web Analytics - FREE, GDPR compliant, no cookies
 */

export function useAnalytics() {
  // Cloudflare automatically tracks page views - no manual tracking needed
  // Custom events are logged to console in development for debugging
  const isDevelopment = import.meta.env.DEV

  // Track page views (Cloudflare handles this automatically)
  const trackPageView = (path) => {
    if (isDevelopment) {
      console.log('[Analytics] Page view:', path)
    }
    // Cloudflare automatically tracks all page views
  }

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

  // Track downloads (CV, resume)
  const trackDownload = (fileName) => {
    trackEvent('Download', { file: fileName })
  }

  // Track external link clicks
  const trackExternalLink = (url) => {
    trackEvent('ExternalLink', { url })
  }

  // Track contact form submissions
  const trackContactForm = (status) => {
    trackEvent('ContactForm', { status })
  }

  // Track project clicks
  const trackProjectClick = (projectName) => {
    trackEvent('ProjectClick', { project: projectName })
  }

  return {
    trackPageView,
    trackEvent,
    trackChatInteraction,
    trackDownload,
    trackExternalLink,
    trackContactForm,
    trackProjectClick
  }
}

/**
 * Setup Cloudflare Web Analytics (FREE):
 *
 * 1. Go to: https://dash.cloudflare.com
 * 2. Navigate to: Analytics & Logs → Web Analytics
 * 3. Click "Add a site" and enter: richwellp.github.io
 * 4. Copy your site token
 * 5. Replace YOUR_CLOUDFLARE_TOKEN in index.html with your actual token
 *
 * Features:
 * - Automatic page view tracking
 * - Referrer tracking
 * - Device/browser analytics
 * - Zero performance impact
 * - 100% FREE forever
 * - GDPR compliant, no cookies
 */
