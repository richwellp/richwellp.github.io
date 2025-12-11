import { ref } from 'vue'

const posts = ref([])
const loading = ref(false)
const error = ref(null)

// Simple frontmatter parser for browser (gray-matter uses Node.js Buffer which isn't available)
function parseFrontmatter(markdown) {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/
  const match = markdown.match(frontmatterRegex)

  if (!match) {
    return { data: {}, content: markdown }
  }

  const [, frontmatter, content] = match
  const data = {}

  const lines = frontmatter.split('\n')
  for (const line of lines) {
    const colonIndex = line.indexOf(':')
    if (colonIndex === -1) continue

    const key = line.substring(0, colonIndex).trim()
    let value = line.substring(colonIndex + 1).trim()

    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1)
    }

    if (value.startsWith('[') && value.endsWith(']')) {
      value = value.slice(1, -1)
        .split(',')
        .map(item => item.trim().replace(/^["']|["']$/g, ''))
    }

    data[key] = value
  }

  return { data, content }
}

export function useBlog() {
  const fetchPosts = async () => {
    loading.value = true
    error.value = null

    try {
      const blogFiles = import.meta.glob('/public/blog/*.md', { as: 'raw', eager: false })

      const postSlugs = Object.keys(blogFiles)
        .map(path => {
          const match = path.match(/\/blog\/(.+)\.md$/)
          return match ? match[1] : null
        })
        .filter(slug => slug !== null && slug !== 'README')

      const postPromises = postSlugs.map(async (slug) => {
        try {
          const url = `/blog/${slug}.md`
          const response = await fetch(url)

          if (!response.ok) {
            console.error(`Failed to fetch blog post ${slug}: ${response.status}`)
            return null
          }

          const markdown = await response.text()
          const { data } = parseFrontmatter(markdown)

          const dateMatch = slug.match(/^(\d{4}-\d{2}-\d{2})/)
          const date = dateMatch ? dateMatch[1] : data.date
          const cleanSlug = slug.replace(/^\d{4}-\d{2}-\d{2}-/, '')

          return {
            slug: cleanSlug,
            title: data.title,
            date: date,
            excerpt: data.excerpt,
            tags: data.tags || [],
            author: data.author
          }
        } catch (err) {
          console.error(`Failed to load blog post ${slug}:`, err)
          return null
        }
      })

      const loadedPosts = await Promise.all(postPromises)

      posts.value = loadedPosts
        .filter(post => post !== null)
        .sort((a, b) => new Date(b.date) - new Date(a.date))

      loading.value = false
    } catch (err) {
      console.error('Error fetching blog posts:', err)
      error.value = err.message
      loading.value = false
    }
  }

  const getPostBySlug = async (slug) => {
    try {
      const blogFiles = import.meta.glob('/public/blog/*.md', { as: 'raw', eager: false })

      let matchedFile = null
      for (const path of Object.keys(blogFiles)) {
        const match = path.match(/\/blog\/(.+)\.md$/)
        if (match) {
          const filename = match[1]
          const cleanFilename = filename.replace(/^\d{4}-\d{2}-\d{2}-/, '')
          if (filename === slug || cleanFilename === slug) {
            matchedFile = filename
            break
          }
        }
      }

      if (!matchedFile) {
        throw new Error('Post not found')
      }

      const response = await fetch(`/blog/${matchedFile}.md`)
      if (!response.ok) {
        throw new Error('Post not found')
      }

      const markdown = await response.text()
      const { data, content } = parseFrontmatter(markdown)

      return {
        ...data,
        content,
        slug
      }
    } catch (err) {
      throw new Error(err.message)
    }
  }

  const parseSlugFromFilename = (filename) => {
    const match = filename.match(/^\d{4}-\d{2}-\d{2}-(.+)\.md$/)
    return match ? match[1] : filename.replace('.md', '')
  }

  const parseDateFromFilename = (filename) => {
    const match = filename.match(/^(\d{4}-\d{2}-\d{2})/)
    return match ? match[1] : null
  }

  return {
    posts,
    loading,
    error,
    fetchPosts,
    getPostBySlug,
    parseSlugFromFilename,
    parseDateFromFilename
  }
}
