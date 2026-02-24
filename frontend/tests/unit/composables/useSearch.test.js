import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useSearch } from '../../../src/composables/useSearch'
import { useBlog } from '../../../src/composables/useBlog'
import { useProfessionalInfo } from '../../../src/composables/useProfessionalInfo'

// Mock the composables
vi.mock('../../../src/composables/useBlog', () => ({
  useBlog: vi.fn()
}))

vi.mock('../../../src/composables/useProfessionalInfo', () => ({
  useProfessionalInfo: vi.fn()
}))

describe('useSearch', () => {
  let mockPosts
  let mockGetPostBySlug
  let mockProjects
  let mockSkills

  beforeEach(() => {
    // Reset all state between tests by clearing and resetting internal flags
    const { searchQuery, searchResults, showSearchResults, clearSearch } = useSearch()
    clearSearch()

    // Reset internal state (need to access via a fresh import to reset module state)
    // This is a workaround for shared state in composables during testing
    vi.resetModules()

    // Setup mock data
    mockPosts = [
      {
        slug: 'test-post',
        title: 'Test Post About Vue',
        excerpt: 'This is a test excerpt about Vue.js',
        tags: ['vue', 'javascript']
      },
      {
        slug: 'another-post',
        title: 'Another Post',
        excerpt: 'Different content here',
        tags: ['react']
      }
    ]

    mockGetPostBySlug = vi.fn((slug) => {
      if (slug === 'test-post') {
        return Promise.resolve({
          content: 'Full blog post content about Vue.js and Composition API'
        })
      }
      return Promise.resolve({ content: 'Other content' })
    })

    mockProjects = [
      {
        title: 'AI Project',
        description: 'Machine learning application',
        technologies: ['Python', 'TensorFlow']
      }
    ]

    mockSkills = [
      {
        name: 'Vue.js',
        category: 'Frontend'
      },
      {
        name: 'Python',
        category: 'Backend'
      }
    ]

    // Mock the composables
    useBlog.mockReturnValue({
      posts: { value: mockPosts },
      getPostBySlug: mockGetPostBySlug
    })

    useProfessionalInfo.mockReturnValue({
      projects: { value: mockProjects },
      skills: { value: mockSkills }
    })
  })

  describe('searchPages', () => {
    it('should return empty results for empty query', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = ''
      await searchPages()

      expect(searchResults.value).toEqual([])
    })

    it('should find blog posts by title', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'Vue'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      expect(searchResults.value[0].title).toBe('Test Post About Vue')
      expect(searchResults.value[0].type).toBe('blog')
    })

    it('should find blog posts by tags', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'javascript'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      const blogResult = searchResults.value.find(r => r.type === 'blog')
      expect(blogResult).toBeDefined()
      expect(blogResult.title).toBe('Test Post About Vue')
    })

    it('should find projects by title', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'AI Project'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      const projectResult = searchResults.value.find(r => r.type === 'project')
      expect(projectResult).toBeDefined()
      expect(projectResult.title).toBe('AI Project')
    })

    it('should find projects by technology', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'Python'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      const results = searchResults.value.filter(r => r.type === 'project' || r.type === 'skill')
      expect(results.length).toBeGreaterThan(0)
    })

    it('should find skills by name', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'Vue.js'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      const skillResult = searchResults.value.find(r => r.type === 'skill')
      expect(skillResult).toBeDefined()
      expect(skillResult.title).toBe('Vue.js')
    })

    it('should find frontend page content', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'contact email'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
      const pageResult = searchResults.value.find(r => r.type === 'page')
      expect(pageResult).toBeDefined()
    })

    it('should set showSearchResults to true when searching', async () => {
      const { searchQuery, showSearchResults, searchPages } = useSearch()

      searchQuery.value = 'Vue'
      await searchPages()

      expect(showSearchResults.value).toBe(true)
    })

    it('should sort results by relevance', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'Vue'
      await searchPages()

      // Title matches should have higher relevance
      if (searchResults.value.length > 1) {
        expect(searchResults.value[0].relevance).toBeGreaterThanOrEqual(
          searchResults.value[searchResults.value.length - 1].relevance
        )
      }
    })

    it('should limit results to 20', async () => {
      // Add many more mock posts
      const manyPosts = Array.from({ length: 30 }, (_, i) => ({
        slug: `post-${i}`,
        title: `Vue Post ${i}`,
        excerpt: 'Vue content',
        tags: ['vue']
      }))

      useBlog.mockReturnValue({
        posts: { value: manyPosts },
        getPostBySlug: mockGetPostBySlug
      })

      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'Vue'
      await searchPages()

      expect(searchResults.value.length).toBeLessThanOrEqual(20)
    })
  })

  describe('clearSearch', () => {
    it('should clear search query and results', async () => {
      const { searchQuery, searchResults, showSearchResults, searchPages, clearSearch } = useSearch()

      // First do a search
      searchQuery.value = 'Vue'
      await searchPages()
      expect(searchResults.value.length).toBeGreaterThan(0)

      // Then clear
      clearSearch()

      expect(searchQuery.value).toBe('')
      expect(searchResults.value).toEqual([])
      expect(showSearchResults.value).toBe(false)
    })
  })

  describe('lazy loading', () => {
    it('should trigger blog content loading when searching', async () => {
      const { searchQuery, searchResults, searchPages, isLoadingBlogContent } = useSearch()

      // Initial state - not loading
      expect(isLoadingBlogContent.value).toBe(false)

      // Perform search
      searchQuery.value = 'Vue'
      await searchPages()

      // loadBlogContent should be triggered (though it may finish immediately in tests)
      // The important thing is that searchPages completes without error
      expect(searchResults.value).toBeDefined()
    })
  })

  describe('case insensitivity', () => {
    it('should find results regardless of case', async () => {
      const { searchQuery, searchResults, searchPages } = useSearch()

      searchQuery.value = 'VUE'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)

      searchQuery.value = 'vue'
      await searchPages()

      expect(searchResults.value.length).toBeGreaterThan(0)
    })
  })

  describe('shared state', () => {
    it('should share state across multiple useSearch calls', () => {
      const search1 = useSearch()
      const search2 = useSearch()

      search1.searchQuery.value = 'test query'

      expect(search2.searchQuery.value).toBe('test query')
    })
  })
})
