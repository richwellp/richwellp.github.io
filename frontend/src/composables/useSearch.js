/**
 * useSearch - Composable for site-wide search functionality
 * Searches blog posts, pages, projects, and skills
 * Implements lazy loading of blog content on first search
 */
import { ref } from 'vue'
import { useBlog } from './useBlog'
import { useProfessionalInfo } from './useProfessionalInfo'
import { CONTACT } from '../config/contact'

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
    content: `Richwell Cyrille Santos Perez AI Engineer RAVE Aerospace multi-agent RAG systems LangGraph hierarchical chatbot
    aerospace IFEC in-flight entertainment connectivity full-stack development Vue.js Python Quart Azure OpenAI PostgreSQL
    University of Illinois Urbana-Champaign UIUC Master of Computer Science MCS Bachelor BS Computer Science with Honors
    Intelligence Data specialization GPA 3.81 3.52
    mainframe database administrator Illinois Secretary of State DB2 z/OS billion records query optimization
    Ashby Prize NCSA AI Innovation Hackathon deep learning aerosol climate model
    teaching assistant software design database systems 800 students object-oriented design patterns
    PySpark Delta Lake Microsoft Fabric distributed ETL predictive maintenance scikit-learn
    LangChain LangGraph multi-agent orchestration RAG production infrastructure`,
    path: '/',
    icon: '👤'
  },
  experience: {
    title: 'Experience',
    content: `AI Engineer RAVE Aerospace Database Administrator Illinois Secretary of State Teaching Assistant UIUC Software Engineer
    full-stack development RAG systems predictive maintenance multi-agent architectures LangGraph chatbot 600 users
    Azure OpenAI PostgreSQL Python Quart Vue.js machine learning clustering analytics dashboard UMAP HDBSCAN K-Means DBSCAN
    in-flight entertainment connectivity IFEC systems aviation aerospace Kingswood Capital Management
    DB2 mainframe z/OS SQL optimization ETL pipelines Azure cloud services statewide digital initiatives REAL ID mobile driver license
    5 billion records query performance 20 seconds instantaneous
    software design database systems object-oriented design patterns performance optimization 800 students Java
    LabWindows CVI embedded systems magnet mapping hardware C
    50 percent latency reduction 30x log compression 500x searchable volume reduction`,
    path: '/experience',
    icon: '💼'
  },
  projects: {
    title: 'Projects',
    content: `UIUC Letter Grades full-stack analytics Node.js MongoDB Python TensorFlow GPA prediction machine learning linear logistic regression
    Video Anomaly Detection Model crime surveillance YOLO Faster R-CNN PyTorch UCF-Crime Multi-Instance Learning MIL weapon recognition
    Deep Learning Aerosol Model climate NCSA AI Innovation Hackathon Ashby Prize 3rd place transformers encoder decoder HPC HAL 9000 supercomputer
    COVID Logging System database relational schema SQL Python web development contact tracing CRUD
    Not Geoff facial recognition OpenCV computer vision deep learning real-time video face detection
    Rocket Rollers Unity C# game development physics collision detection level progression
    Open Flights flight data analysis Python Pandas visualization route optimization global airport data`,
    path: '/projects',
    icon: '🚀'
  },
  cv: {
    title: 'CV / Resume',
    content: `Resume curriculum vitae qualifications education experience skills achievements download PDF
    Computer Science BS MS Master UIUC University of Illinois Urbana-Champaign GPA 3.81 3.52
    Python JavaScript TypeScript SQL Vue.js Flask Quart LangChain LangGraph
    Machine Learning Deep Learning Computer Vision RAG LLM Azure OpenAI
    PySpark Delta Lake PostgreSQL MongoDB DB2`,
    path: '/cv',
    icon: '📄'
  },
  contact: {
    title: 'Contact',
    content: `contact email ${CONTACT.email} get in touch message collaboration opportunities freelance
    LinkedIn GitHub social media professional networking connect reach out
    full-time roles software AI conversations`,
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
  console.log('[Search] Called with query:', searchQuery.value)

  if (!searchQuery.value.trim()) {
    searchResults.value = []
    showSearchResults.value = false
    console.log('[Search] Empty query, clearing results')
    return
  }

  const query = searchQuery.value.toLowerCase()
  const results = []
  const { posts } = useBlog()
  const { projects, skills } = useProfessionalInfo()

  console.log('[Search] Searching in:', {
    posts: posts.value.length,
    projects: projects.value.length,
    skills: skills.value.length,
    blogContentLoaded: blogContentLoaded.value
  })

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
    const titleMatch = (project.name || project.title)?.toLowerCase().includes(query)
    const descMatch = project.description?.toLowerCase().includes(query)
    const techMatch = project.technologies?.some(tech => tech.toLowerCase().includes(query))

    if (titleMatch || descMatch || techMatch) {
      results.push({
        title: project.name || project.title,
        subtitle: project.description?.substring(0, 80) + '...' || '',
        path: '/projects',
        icon: '🚀',
        type: 'project',
        relevance: titleMatch ? 4 : 2
      })
    }
  })

  // Search skills (flatten object structure)
  if (skills.value && typeof skills.value === 'object') {
    Object.entries(skills.value).forEach(([category, skillList]) => {
      if (Array.isArray(skillList)) {
        skillList.forEach(skillName => {
          if (skillName.toLowerCase().includes(query)) {
            results.push({
              title: skillName,
              subtitle: `Skill: ${category.replace(/_/g, ' ')}`,
              path: '/',
              icon: '⚡',
              type: 'skill',
              relevance: 2
            })
          }
        })
      }
    })
  }

  // Sort by relevance
  searchResults.value = results.sort((a, b) => b.relevance - a.relevance).slice(0, 20)
  showSearchResults.value = true

  console.log('[Search] Results:', {
    found: searchResults.value.length,
    showResults: showSearchResults.value,
    results: searchResults.value.map(r => ({ title: r.title, type: r.type }))
  })
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
