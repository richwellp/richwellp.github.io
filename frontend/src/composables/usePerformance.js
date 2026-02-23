// Performance monitoring composable
export function usePerformance() {
  const trackPageLoad = () => {
    if (typeof window !== 'undefined' && window.performance) {
      window.addEventListener('load', () => {
        const perfData = window.performance.timing
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart
        const connectTime = perfData.responseEnd - perfData.requestStart

        console.log('Performance Metrics:', {
          pageLoadTime: `${pageLoadTime}ms`,
          connectTime: `${connectTime}ms`,
          domContentLoaded: `${perfData.domContentLoadedEventEnd - perfData.navigationStart}ms`
        })

        // Optional: Send to analytics
        // trackAnalytics('performance', { pageLoadTime, connectTime })
      })
    }
  }

  return {
    trackPageLoad
  }
}
