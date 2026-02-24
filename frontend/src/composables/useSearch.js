/**
 * useSearch - Composable for site-wide search functionality
 * Searches blog posts, pages, projects, and skills
 * Implements lazy loading of blog content on first search
 */
import { ref } from 'vue'
import { useBlog } from './useBlog'
import { useProfessionalInfo } from './useProfessionalInfo'

// Shared state
const searchQuery = ref('')
const searchResults = ref([])
const showSearchResults = ref(false)
const blogContent = ref({})
const isLoadingBlogContent = ref(false)
const blogContentLoaded = ref(false)

// Frontend page content for searching
const frontendContent = {
  about: {
    title: 'About Me',
    content: `Richwell Perez AI Engineer specializing in full-stack development RAG systems machine learning
    I build software data and AI systems that solve real-world problems actively seeking opportunities to learn grow
    University of Illinois UIUC Master Computer Science Bachelor Computer Science with Honors
    drawn to building technology that solves real-world problems developed full-stack applications ML deep learning models
    explored data analytics built retrieval-augmented generation RAG systems worked with cloud platforms AI-powered applications
    passionate about developing technologies that improve lives deliver meaningful impact software data insights intelligent AI systems`,
    path: '/',
    icon: '👤'
  },
  experience: {
    title: 'Experience Overview',
    content: `AI Engineer RAVE Aerospace Database Administrator Illinois Secretary of State Teaching Assistant UIUC Software Engineer
    Full-stack development RAG systems predictive maintenance multi-agent architectures LangGraph chatbot
    Azure OpenAI PostgreSQL Python Quart Vue.js machine learning clustering analytics dashboard
    In-flight entertainment connectivity IFEC systems aviation aerospace Safran Passenger Innovations
    DB2 mainframe z/OS SQL optimization ETL pipelines Azure cloud services statewide digital initiatives
    Software Design Database Systems object-oriented design patterns performance optimization`,
    path: '/experience',
    icon: '💼'
  },
  projects: {
    title: 'Projects',
    content: `AI-Powered Admission System predictive college admission machine learning neural networks decision trees
    Automated ETL Pipeline Azure Databricks PySpark cloud data engineering automation
    Personal Portfolio Website Vue.js Flask responsive design modern web development
    Retrieval Augmented Generation RAG systems embeddings vector search semantic similarity`,
    path: '/projects',
    icon: '🚀'
  },
  cv: {
    title: 'CV / Resume',
    content: `Resume curriculum vitae qualifications education experience skills achievements
    Computer Science BS MS Master UIUC University Illinois
    Python JavaScript TypeScript SQL Vue React Flask FastAPI
    Machine Learning Deep Learning Natural Language Processing Computer Vision`,
    path: '/cv',
    icon: '📄'
  },
  contact: {
    title: 'Contact',
    content: `contact email richwell.perez@gmail.com get in touch message collaboration opportunities
    LinkedIn GitHub social media professional networking connect reach out`,
    path: '/contact',
    icon: '📧'
  }
}

/**
 * Load full blog content for searching (lazy loading)
 * Only loads on first search to improve initial page load performance
 */
async function loadBlogContent() {
  if (isLoadingBlogContent.value || blogContentLoaded.value) return

  isLoadingBlogContent.value = true
  const { posts, getPostBySlug } = useBlog()

  try {
    // Load all blog posts in parallel for faster loading
    const loadPromises = posts.value.map(async (post) => {
      try {
        const fullPost = await getPostBySlug(post.slug)
        blogContent.value[post.slug] = fullPost.content
      } catch (err) {
        console.error(`Failed to load content for ${post.slug}`, err)
      }
    })

    await Promise.all(loadPromises)
    blogContentLoaded.value = true
  } catch (err) {
    console.error('Failed to load blog content:', err)
  } finally {
    isLoadingBlogContent.value = false
  }
}

/**
 * Extract snippet around the search match
 */
function extractSnippet(text, query, maxLength = 100) {
  const lowerText = text.toLowerCase()
  const lowerQuery = query.toLowerCase()
  const index = lowerText.indexOf(lowerQuery)

  if (index === -1) return text.substring(0, maxLength) + '...'

  const start = Math.max(0, index - 30)
  const end = Math.min(text.length, index + query.length + 70)
  const snippet = text.substring(start, end)

  return (start > 0 ? '...' : '') + snippet + (end < text.length ? '...' : '')
}

/**
 * Perform comprehensive site-wide search
 */
async function searchPages() {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    showSearchResults.value = false
    return
  }

  const query = searchQuery.value.toLowerCase()
  const results = []
  const { posts } = useBlog()
  const { projects, skills } = useProfessionalInfo()

  // Lazy load blog content on first search
  if (posts.value.length > 0 && !blogContentLoaded.value && !isLoadingBlogContent.value) {
    loadBlogContent()
  }

  // Search blog posts (title, excerpt, tags, and full content)
  posts.value.forEach(post => {
    const titleMatch = post.title.toLowerCase().includes(query)
    const excerptMatch = post.excerpt?.toLowerCase().includes(query)
    const tagsMatch = post.tags?.some(tag => tag.toLowerCase().includes(query))
    const contentMatch = blogContent.value[post.slug]?.toLowerCase().includes(query)

    if (titleMatch || excerptMatch || tagsMatch || contentMatch) {
      let subtitle = post.excerpt?.substring(0, 80) + '...' || ''
      let relevance = 2

      // Higher relevance for title matches
      if (titleMatch) relevance = 5
      // Show snippet from content if matched there
      else if (contentMatch && blogContent.value[post.slug]) {
        subtitle = extractSnippet(blogContent.value[post.slug], query, 100)
        relevance = 3
      } else if (excerptMatch) {
        relevance = 4
      }

      results.push({
        title: post.title,
        subtitle,
        path: `/misc/blog/${post.slug}`,
        icon: '📝',
        type: 'blog',
        relevance
      })
    }
  })

  // Search frontend page content
  Object.values(frontendContent).forEach(page => {
    if (page.content.toLowerCase().includes(query)) {
      const snippet = extractSnippet(page.content, query, 100)
      results.push({
        title: page.title,
        subtitle: snippet,
        path: page.path,
        icon: page.icon,
        type: 'page',
        relevance: 3
      })
    }
  })

  // Search projects
  projects.value.forEach(project => {
    const titleMatch = project.title?.toLowerCase().includes(query)
    const descMatch = project.description?.toLowerCase().includes(query)
    const techMatch = project.technologies?.some(tech => tech.toLowerCase().includes(query))

    if (titleMatch || descMatch || techMatch) {
      results.push({
        title: project.title,
        subtitle: project.description?.substring(0, 80) + '...' || '',
        path: '/projects',
        icon: '🚀',
        type: 'project',
        relevance: titleMatch ? 4 : 2
      })
    }
  })

  // Search skills
  skills.value.forEach(skill => {
    if (skill.name?.toLowerCase().includes(query)) {
      results.push({
        title: skill.name,
        subtitle: `Skill: ${skill.category || 'General'}`,
        path: '/',
        icon: '⚡',
        type: 'skill',
        relevance: 2
      })
    }
  })

  // Sort by relevance
  searchResults.value = results.sort((a, b) => b.relevance - a.relevance).slice(0, 20)
  showSearchResults.value = true
}

/**
 * Clear search
 */
function clearSearch() {
  searchQuery.value = ''
  searchResults.value = []
  showSearchResults.value = false
}

export function useSearch() {
  return {
    searchQuery,
    searchResults,
    showSearchResults,
    isLoadingBlogContent,
    searchPages,
    clearSearch,
    loadBlogContent
  }
}
