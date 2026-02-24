/**
 * useStructuredData - Composable for managing JSON-LD structured data
 * Generates and injects Schema.org structured data for SEO optimization
 */

/**
 * Generate Person Schema (For homepage/about page)
 */
export function generatePersonSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    'name': 'Richwell Cyrille Santos Perez',
    'url': 'https://richwellp.github.io',
    'image': 'https://richwellp.github.io/assets/photos/professional_1.jpg',
    'jobTitle': 'AI Engineer',
    'worksFor': {
      '@type': 'Organization',
      'name': 'Safran'
    },
    'sameAs': [
      'https://www.linkedin.com/in/richwell-perez',
      'https://github.com/richwellp'
    ],
    'alumniOf': {
      '@type': 'EducationalOrganization',
      'name': 'University of Illinois Urbana-Champaign'
    },
    'email': 'richwell.perez@gmail.com',
    'description': 'AI Engineer with BS/MCS in Computer Science from UIUC, specializing in Data and Artificial Intelligence. Building full-stack applications, ML models, and AI solutions.'
  }
}

/**
 * Generate Organization Schema (For website identity)
 */
export function generateOrganizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    'name': 'Richwell Perez',
    'url': 'https://richwellp.github.io',
    'logo': 'https://richwellp.github.io/assets/photos/professional_1.jpg',
    'description': 'Portfolio and blog of Richwell Perez, AI Engineer',
    'sameAs': [
      'https://www.linkedin.com/in/richwell-perez',
      'https://github.com/richwellp'
    ],
    'contact': {
      '@type': 'ContactPoint',
      'telephone': '+1-833-774-2963',
      'contactType': 'General Inquiry',
      'email': 'richwell.perez@gmail.com'
    }
  }
}

/**
 * Generate BlogPosting Schema (For individual blog posts)
 * @param {Object} post - Blog post data
 * @returns {Object} BlogPosting schema
 */
export function generateBlogPostSchema(post) {
  if (!post || !post.title) {
    console.warn('Invalid blog post data provided to generateBlogPostSchema')
    return null
  }

  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    'headline': post.title,
    'description': post.excerpt || post.title,
    'datePublished': post.date ? new Date(post.date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
    'url': `https://richwellp.github.io/misc/blog/${post.slug}`,
    'image': post.image || 'https://richwellp.github.io/assets/photos/professional_1.jpg',
    'author': {
      '@type': 'Person',
      'name': post.author || 'Richwell Perez',
      'url': 'https://richwellp.github.io'
    },
    'publisher': {
      '@type': 'Organization',
      'name': 'Richwell Perez',
      'logo': {
        '@type': 'ImageObject',
        'url': 'https://richwellp.github.io/assets/photos/professional_1.jpg'
      }
    }
  }

  // Add keywords/tags as keywords
  if (post.tags && post.tags.length > 0) {
    schema.keywords = Array.isArray(post.tags) ? post.tags.join(', ') : post.tags
  }

  // Add article body and word count if available
  if (post.content) {
    schema.articleBody = post.content
    // Calculate word count
    const wordCount = post.content.split(/\s+/).length
    schema.wordCount = Math.max(1, wordCount)
  }

  // Add reading time if available
  if (post.readingTime) {
    schema.timeRequired = `PT${post.readingTime}M`
  }

  return schema
}

/**
 * Generate BlogPosting schema for blog list page
 */
export function generateBlogListSchema(posts) {
  if (!posts || posts.length === 0) {
    return null
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    'name': 'Blog',
    'url': 'https://richwellp.github.io/misc/blog',
    'description': 'Blog posts by Richwell Perez about AI, software engineering, and technology',
    'mainEntity': {
      '@type': 'ItemList',
      'numberOfItems': posts.length,
      'itemListElement': posts.map((post, index) => ({
        '@type': 'BlogPosting',
        'position': index + 1,
        'headline': post.title,
        'description': post.excerpt || post.title,
        'url': `https://richwellp.github.io/misc/blog/${post.slug}`,
        'datePublished': post.date ? new Date(post.date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        'author': {
          '@type': 'Person',
          'name': post.author || 'Richwell Perez'
        }
      }))
    }
  }
}

/**
 * Generate BreadcrumbList Schema
 * @param {Array} breadcrumbs - Array of breadcrumb items [{name: string, path: string}]
 * @returns {Object} BreadcrumbList schema
 */
export function generateBreadcrumbSchema(breadcrumbs) {
  if (!breadcrumbs || breadcrumbs.length === 0) {
    return null
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': breadcrumbs.map((item, index) => ({
      '@type': 'ListItem',
      'position': index + 1,
      'name': item.name,
      'item': `https://richwellp.github.io${item.path}`
    }))
  }
}

/**
 * Generate schema for Experience page
 */
export function generateWorkExperienceSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    'name': 'Richwell Cyrille Santos Perez',
    'jobTitle': 'AI Engineer',
    'url': 'https://richwellp.github.io/experience',
    'hasOccupation': [
      {
        '@type': 'Occupation',
        'name': 'AI Engineer',
        'occupationLocation': {
          '@type': 'City',
          'name': 'Remote'
        },
        'workHours': 'Full-time',
        'estimatedSalary': {
          '@type': 'PriceSpecification',
          'priceCurrency': 'USD'
        }
      },
      {
        '@type': 'Occupation',
        'name': 'Database Administrator',
        'occupationLocation': {
          '@type': 'City',
          'name': 'Remote'
        }
      }
    ]
  }
}

/**
 * Generate schema for Projects page
 */
export function generateProjectsListSchema(projects) {
  if (!projects || projects.length === 0) {
    return null
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    'name': 'Projects',
    'url': 'https://richwellp.github.io/projects',
    'description': 'Portfolio projects by Richwell Perez',
    'creator': {
      '@type': 'Person',
      'name': 'Richwell Perez'
    },
    'mainEntity': {
      '@type': 'ItemList',
      'numberOfItems': projects.length,
      'itemListElement': projects.map((project, index) => ({
        '@type': 'SoftwareApplication',
        'position': index + 1,
        'name': project.title,
        'description': project.description,
        'url': project.url,
        'applicationCategory': 'Software',
        'creator': {
          '@type': 'Person',
          'name': 'Richwell Perez'
        }
      }))
    }
  }
}

/**
 * Insert JSON-LD script into document head
 * @param {Object} schema - Schema object to insert
 * @param {string} id - Unique ID for the script tag
 */
export function injectStructuredData(schema, id = 'structured-data') {
  if (!schema) {
    return
  }

  // Remove existing structured data with same ID
  const existingScript = document.getElementById(id)
  if (existingScript) {
    existingScript.remove()
  }

  // Create and inject new script
  const script = document.createElement('script')
  script.type = 'application/ld+json'
  script.id = id
  script.textContent = JSON.stringify(schema)

  document.head.appendChild(script)
}

/**
 * Insert multiple JSON-LD schemas (e.g., Person + Organization + BreadcrumbList)
 * @param {Array<{schema: Object, id: string}>} schemas - Array of schemas with IDs
 */
export function injectMultipleStructuredData(schemas) {
  if (!Array.isArray(schemas)) {
    return
  }

  schemas.forEach(({ schema, id }) => {
    if (schema) {
      injectStructuredData(schema, id)
    }
  })
}

/**
 * Get breadcrumbs for current route
 * @param {string} routeName - Current route name
 * @param {object} routeParams - Route params (for dynamic routes)
 * @returns {Array} Breadcrumb items
 */
export function getBreadcrumbs(routeName, routeParams = {}) {
  const breadcrumbMap = {
    'about-me': [
      { name: 'Home', path: '/' }
    ],
    'experience': [
      { name: 'Home', path: '/' },
      { name: 'Experience', path: '/experience' }
    ],
    'projects': [
      { name: 'Home', path: '/' },
      { name: 'Projects', path: '/projects' }
    ],
    'cv': [
      { name: 'Home', path: '/' },
      { name: 'CV', path: '/cv' }
    ],
    'misc': [
      { name: 'Home', path: '/' },
      { name: 'Misc', path: '/misc' }
    ],
    'contact': [
      { name: 'Home', path: '/' },
      { name: 'Contact', path: '/contact' }
    ],
    'albums': [
      { name: 'Home', path: '/' },
      { name: 'Misc', path: '/misc' },
      { name: 'Albums', path: '/misc/albums' }
    ],
    'blog-list': [
      { name: 'Home', path: '/' },
      { name: 'Misc', path: '/misc' },
      { name: 'Blog', path: '/misc/blog' }
    ],
    'blog-post': [
      { name: 'Home', path: '/' },
      { name: 'Misc', path: '/misc' },
      { name: 'Blog', path: '/misc/blog' },
      { name: 'Post', path: '' } // Will be updated with actual post title
    ]
  }

  // Handle dynamic album route
  if (routeName === 'album-detail' && routeParams.slug) {
    const albumName = routeParams.slug.charAt(0).toUpperCase() + routeParams.slug.slice(1)
    return [
      { name: 'Home', path: '/' },
      { name: 'Misc', path: '/misc' },
      { name: 'Albums', path: '/misc/albums' },
      { name: albumName, path: `/misc/albums/${routeParams.slug}` }
    ]
  }

  return breadcrumbMap[routeName] || [{ name: 'Home', path: '/' }]
}

/**
 * Hook to set up structured data on route change
 * Should be called in router beforeEach guard
 */
export function useStructuredDataOnRouteChange(to) {
  const breadcrumbs = getBreadcrumbs(to.name, to.params)
  const breadcrumbSchema = generateBreadcrumbSchema(breadcrumbs)
  const personSchema = generatePersonSchema()

  // Always inject breadcrumbs and person schema
  injectMultipleStructuredData([
    { schema: breadcrumbSchema, id: 'breadcrumb-list' },
    { schema: personSchema, id: 'person-schema' }
  ])
}
