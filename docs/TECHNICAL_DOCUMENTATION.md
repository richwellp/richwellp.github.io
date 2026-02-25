# Technical Documentation

**Quick Reference:** [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
**Authentication Guide:** [AUTHENTICATION.md](./AUTHENTICATION.md)

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Frontend Deep Dive](#frontend-deep-dive)
- [Backend Deep Dive](#backend-deep-dive)
- [Database Architecture](#database-architecture)
- [Deployment Pipeline](#deployment-pipeline)
- [Development Workflow](#development-workflow)
- [Security Architecture](#security-architecture)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Vue 3 SPA (GitHub Pages)                       │ │
│  │  - Static HTML/CSS/JS                                  │ │
│  │  - Client-side routing (Vue Router)                    │ │
│  │  - State management (Composition API)                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
           │                              │
           │ REST API                     │ Direct Access
           │                              │ (Supabase Client)
           ▼                              ▼
┌──────────────────────┐      ┌─────────────────────────┐
│   Flask Backend      │      │   Supabase Storage      │
│   (Vercel)           │      │   (Photos/Videos)       │
│                      │      │                         │
│  - REST API          │      │  - Public bucket        │
│  - Gemini AI         │◄────►│  - Anon key access     │
│  - Service Role      │      └─────────────────────────┘
│    (bypasses RLS)    │
└──────────────────────┘
           │
           │ PostgreSQL
           │ (Service Role Key)
           ▼
┌─────────────────────────┐
│   Supabase PostgreSQL   │
│                         │
│  - blog_posts table     │
│  - albums table         │
│  - photos table         │
│  - Row Level Security   │
│  - Triggers & Indexes   │
└─────────────────────────┘
```

### Data Flow

**Public Content (Blog Posts, Albums):**
```
User → Vue Frontend → Flask API → Supabase DB → Response
```

**Admin Operations (Create/Edit/Delete):**
```
Admin → /admin UI → Auth Modal (BLOG_ADMIN_KEY)
  → Flask API (@require_admin) → Supabase (Service Role) → Success
```

**Photo Uploads:**
```
Admin → PhotoManager → File Upload → Flask /admin/upload
  → Supabase Storage (Service Role) → Photo URL
  → Insert to photos table → Success
```

**AI Chatbot:**
```
User → ChatAssistant.vue → Flask /chat/stream (SSE)
  → Gemini API → Streaming Response → Display
```

---

## Technology Stack

### Frontend
- **Framework:** Vue 3 (Composition API, `<script setup>`)
- **Build Tool:** Vite 5.x (fast HMR, optimized builds)
- **Routing:** Vue Router 4 (client-side routing, lazy loading)
- **HTTP Client:** Native Fetch API
- **Markdown:** markdown-it (blog post rendering)
- **Sanitization:** DOMPurify (XSS protection)
- **Storage Client:** @supabase/supabase-js
- **Testing:** Vitest + @vue/test-utils

### Backend
- **Framework:** Flask 3.x (Python web framework)
- **WSGI Server:** Gunicorn (production)
- **Database Client:** supabase-py
- **AI/LLM:** google-generativeai (Gemini 2.5 Flash)
- **CORS:** flask-cors (cross-origin requests)
- **Compression:** Flask-Compress (gzip responses)
- **Testing:** pytest

### Database & Storage
- **Database:** Supabase PostgreSQL (managed Postgres)
- **Storage:** Supabase Storage (S3-compatible)
- **ORM:** None (direct SQL via Supabase client)
- **Migrations:** Manual SQL scripts

### DevOps & CI/CD
- **Frontend Hosting:** GitHub Pages (static files)
- **Backend Hosting:** Vercel (serverless Flask)
- **CI/CD:** GitHub Actions
- **Version Control:** Git + GitHub

---

## Project Structure

```
richwellp.github.io/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                    # CI/CD pipeline
├── backend/
│   ├── api/
│   │   ├── __init__.py                  # API blueprint registration
│   │   ├── albums.py                    # Albums/Photos CRUD endpoints
│   │   ├── blog.py                      # Blog CRUD endpoints
│   │   ├── gemini.py                    # AI chatbot endpoints
│   │   └── sitemap.py                   # Dynamic sitemap generation
│   ├── database/
│   │   ├── albums_schema.sql            # Albums/Photos table schema
│   │   ├── blog_schema.sql              # Blog table schema
│   │   └── seed_initial_albums.sql      # Initial album seed data
│   ├── tests/
│   │   ├── test_albums.py               # Albums API tests (17 tests)
│   │   ├── test_blog.py                 # Blog API tests (33 tests)
│   │   └── test_gemini.py               # Gemini API tests
│   ├── app.py                           # Flask app entry point
│   ├── auth.py                          # Admin authentication
│   ├── config.py                        # Backend configuration
│   ├── requirements.txt                 # Python dependencies
│   └── vercel.json                      # Vercel deployment config
├── frontend/
│   ├── public/
│   │   ├── assets/
│   │   │   └── Resume.pdf               # Your resume (download link)
│   │   ├── data/
│   │   │   └── professionalInfo.json    # Experience, projects, skills data
│   │   ├── robots.txt                   # SEO: allow all crawlers
│   │   └── sitemap.xml                  # Static sitemap
│   ├── src/
│   │   ├── assets/                      # Static assets (CSS, images)
│   │   ├── components/
│   │   │   ├── AdminAuthModal.vue       # Admin login modal
│   │   │   ├── AlbumCoverSlideshow.vue  # Album cover with auto-cycling photos
│   │   │   ├── AlbumEditorModal.vue     # Edit album metadata modal
│   │   │   ├── AlbumViewer.vue          # Full album photo grid view
│   │   │   ├── ChatAssistant.vue        # AI chatbot UI (SSE streaming)
│   │   │   ├── CommandPalette.vue       # Cmd+K quick navigation
│   │   │   ├── DeleteConfirmModal.vue   # Reusable delete confirmation
│   │   │   ├── Header.vue               # Main navigation header
│   │   │   ├── MarkdownEditor.vue       # Blog post markdown editor
│   │   │   ├── OptimizedImage.vue       # Lazy-loading image component
│   │   │   ├── PhotoEditorModal.vue     # Edit photo metadata modal
│   │   │   └── TableOfContents.vue      # Blog post TOC (auto-generated)
│   │   ├── composables/
│   │   │   ├── useAdminAlbums.js        # Admin album CRUD operations
│   │   │   ├── useAdminAuth.js          # Admin authentication state
│   │   │   ├── useAdminBlog.js          # Admin blog CRUD operations
│   │   │   ├── useAlbums.js             # Public album fetching
│   │   │   ├── useAnalytics.js          # Page view tracking (console only)
│   │   │   ├── useAsyncRequest.js       # Shared async state management
│   │   │   ├── useBlog.js               # Public blog fetching
│   │   │   ├── useChatAssistant.js      # AI chatbot logic (828 lines)
│   │   │   ├── useCommandPalette.js     # Command palette state
│   │   │   ├── useSanitizer.js          # XSS protection (DOMPurify)
│   │   │   ├── useSearch.js             # Professional info search
│   │   │   ├── useStructuredData.js     # SEO JSON-LD schema generation
│   │   │   └── useVisitorMap.js         # Visitor geolocation map
│   │   ├── config/
│   │   │   ├── api.js                   # API endpoints configuration
│   │   │   ├── constants.js             # App-wide constants
│   │   │   ├── contact.js               # Contact info
│   │   │   └── site.js                  # Site metadata (URL, name)
│   │   ├── lib/
│   │   │   └── supabase.js              # Supabase client setup
│   │   ├── router/
│   │   │   └── index.js                 # Vue Router routes
│   │   ├── views/
│   │   │   ├── admin/
│   │   │   │   ├── AdminDashboard.vue   # Admin home (stats)
│   │   │   │   ├── AdminPanel.vue       # Blog post list (admin)
│   │   │   │   ├── AlbumsAdmin.vue      # Albums list (admin)
│   │   │   │   ├── PhotoManager.vue     # Photo upload/management
│   │   │   │   └── PostEditor.vue       # Blog post create/edit
│   │   │   ├── blog/
│   │   │   │   ├── BlogList.vue         # Blog post listing (public)
│   │   │   │   └── BlogPost.vue         # Single blog post view
│   │   │   ├── AboutMe.vue              # About/Education section
│   │   │   ├── Albums.vue               # Albums grid view (public)
│   │   │   ├── Contact.vue              # Contact form (email link)
│   │   │   ├── CV.vue                   # Resume download page
│   │   │   ├── Experience.vue           # Work experience page
│   │   │   ├── Home.vue                 # Landing page
│   │   │   ├── Misc.vue                 # Misc section (blog, albums)
│   │   │   ├── NotFound.vue             # 404 error page
│   │   │   └── Projects.vue             # Projects showcase
│   │   ├── App.vue                      # Root component (layout)
│   │   └── main.js                      # Vue app entry point
│   ├── tests/
│   │   └── unit/
│   │       ├── composables/             # Composable tests
│   │       └── components/              # Component tests
│   ├── index.html                       # HTML entry point
│   ├── package.json                     # Node dependencies
│   ├── vite.config.js                   # Vite configuration
│   └── vitest.config.js                 # Vitest test configuration
├── docs/
│   ├── plans/
│   │   └── 2025-01-19-codebase-refactoring.md  # Implementation plans
│   └── TECHNICAL_DOCUMENTATION.md       # This file
├── .gitignore                           # Git ignore patterns
├── CONTRIBUTING.md                      # Contribution guidelines
└── README.md                            # Project overview
```

---

## Frontend Deep Dive

### Entry Point & App Initialization

**`frontend/index.html`** (HTML Entry)
- Root HTML file served by Vite
- Contains `<div id="app"></div>` mount point
- Loads `main.js` via `<script type="module">`
- Meta tags for SEO, viewport, theme color

**`frontend/src/main.js`** (JavaScript Entry)
- Creates Vue 3 app: `createApp(App)`
- Registers Vue Router
- Mounts app to `#app` div
- **Key Line:** `app.use(router).mount('#app')`

**`frontend/src/App.vue`** (Root Component)
- Global layout structure
- Contains `<Header>` component
- Contains `<router-view>` for page content
- Contains `<ChatAssistant>` floating button
- Global CSS variables (dark theme)
- Responsive breakpoints

### Routing System

**`frontend/src/router/index.js`**

Routes configuration:
```javascript
{
  path: '/',                           // Home page
  path: '/experience',                 // Work history
  path: '/projects',                   // Project showcase
  path: '/about',                      // Education & bio
  path: '/contact',                    // Contact form
  path: '/cv',                         // Resume download
  path: '/misc',                       // Blog & Albums hub
  path: '/misc/blog',                  // Blog list
  path: '/misc/blog/:slug',            // Blog post detail
  path: '/misc/albums',                // Albums grid
  path: '/misc/albums/:slug',          // Album photo viewer
  path: '/admin',                      // Admin dashboard
  path: '/admin/new',                  // Create blog post
  path: '/admin/edit/:slug',           // Edit blog post
  path: '/admin/albums',               // Manage albums
  path: '/admin/albums/:slug/photos',  // Manage photos
  path: '/:pathMatch(.*)*',            // 404 Not Found
}
```

**Navigation Guards:**
- No auth guards (admin auth handled in UI via modal)
- Page title updates via `router.afterEach()`
- Scroll behavior: scroll to top on route change

### Core Components

#### **`Header.vue`** (Navigation)
- Desktop: Full navigation menu
- Mobile: Hamburger menu
- Active route highlighting
- Responsive CSS Grid layout
- Links to all main sections

#### **`ChatAssistant.vue`** (AI Chatbot)
- Floating chat button (bottom-right)
- Slide-out chat panel
- Message list with scrolling
- Streaming responses via Server-Sent Events (SSE)
- Welcome message on first open
- Persistent conversation history (localStorage)
- Clear chat functionality
- Typing indicators
- Error handling with retry

**Key Features:**
- SSE streaming: Real-time character-by-character response
- Context-aware: Sends last 10 messages for conversation continuity
- Auto-scroll to latest message
- Markdown rendering with sanitization
- Debounced input (prevents spam)

#### **`CommandPalette.vue`** (Quick Nav)
- Triggered by: `Cmd/Ctrl + K`
- Fuzzy search across all routes
- Keyboard navigation (arrow keys, enter)
- Escape to close
- Filters routes by search query
- Instant navigation

#### **`AlbumCoverSlideshow.vue`** (Album Previews)
- Auto-cycling slideshow (5 seconds per photo)
- Fade transitions between photos
- Supports photos AND videos
- Video auto-plays until end, then advances
- Falls back to cover_photo if no photos loaded
- Hover overlay with album info
- Router link to full album view

**Technical Details:**
- Uses `TransitionGroup` with fade animation
- Timer management: `setTimeout` for photos, `@ended` for videos
- Fetches album photos on mount
- Cleans up timer on unmount

#### **`AlbumViewer.vue`** (Photo Gallery)
- Masonry grid layout (responsive columns)
- Lightbox modal for full-size view
- Keyboard navigation (arrow keys, escape)
- Swipe gestures for mobile
- Lazy loading images
- Category filtering (travel: USA, Philippines, Japan)
- Photo captions and metadata

#### **`MarkdownEditor.vue`** (Blog Post Editor)
- Split view: editor (left) + preview (right)
- Toolbar: Bold, Italic, Heading, Link, List, Code
- Live preview with markdown-it
- Sanitized HTML output
- Auto-growing textarea
- Syntax highlighting in preview

#### **`TableOfContents.vue`** (Blog TOC)
- Auto-generates from blog post headings (h2, h3)
- Active section highlighting on scroll
- Smooth scroll to section on click
- Sticky positioning
- Responsive: hides on mobile

### Composables (Business Logic)

#### **`useBlog.js`** (Public Blog API)
**Exports:**
- `posts` (ref): Array of blog posts
- `loading` (ref): Loading state
- `error` (ref): Error message
- `fetchPosts()`: Fetch all published posts
- `fetchPostBySlug(slug)`: Fetch single post
- `searchPosts(query)`: Search posts by title/content

**API Calls:**
- `GET /blog/posts` → List of published posts
- `GET /blog/posts/:slug` → Single post with reading time
- `GET /blog/search?q=query` → Search results

**Features:**
- Shared state (singleton pattern)
- Reading time calculation (words ÷ 200 WPM)
- Heading extraction for TOC
- Error handling with fallback

#### **`useAlbums.js`** (Public Albums API)
**Exports:**
- `albums` (ref): Array of albums
- `loading` (ref): Loading state
- `error` (ref): Error message
- `fetchAlbums()`: Fetch all published albums
- `fetchAlbumBySlug(slug)`: Fetch single album with photos

**API Calls:**
- `GET /albums` → List of albums with cover photos
- `GET /albums/:slug` → Album with all photos

**Features:**
- Groups photos by category
- Sorts photos by order_index
- Caches album data
- Video detection (mp4, mov, webm)

#### **`useAdminAuth.js`** (Admin Authentication)
**Exports:**
- `isAuthenticated` (ref): Auth status
- `token` (ref): Admin token (legacy, for backwards compatibility)
- `showAuthModal` (ref): Modal visibility
- `login(password)`: Authenticate admin
- `logout()`: Clear auth state
- `checkAuth()`: Verify token validity

**Authentication Flow (Cookie-based):**
1. User enters password in `AdminAuthModal`
2. `POST /auth/login` with password
3. Backend validates against `BLOG_ADMIN_KEY`
4. Returns httpOnly secure cookie (`admin_session`, 24h expiry)
5. Cookie automatically sent with subsequent requests
6. Backend verifies cookie with `@require_admin` decorator

**Cross-Origin Support:**
- Production: `SameSite=None; Secure` (enables cookies across richwellp.github.io → richwellp-github-io.vercel.app)
- Development: `SameSite=Lax` (local testing)

**Cookie Management:**
- **No localStorage:** Cookies are httpOnly (not accessible to JavaScript)
- **Automatic transmission:** Browser automatically sends `admin_session` cookie with requests
- **credentials: 'include':** Frontend fetch config ensures cookies are sent cross-origin
- **Cookie expiry:** 24 hours from login (enforced by backend)

#### **`useAdminBlog.js`** (Admin Blog CRUD)
**Exports:**
- `adminPosts` (ref): All posts (including drafts)
- `createPost(postData)`: Create new post
- `updatePost(slug, postData)`: Update existing post
- `deletePost(slug)`: Delete post
- `fetchAdminPosts(status)`: Fetch posts by status

**API Calls (All require auth token):**
- `GET /blog/admin/posts?status=draft` → Draft posts
- `GET /blog/admin/posts/:slug` → Single post (any status)
- `POST /blog/posts` → Create post
- `PUT /blog/posts/:slug` → Update post
- `DELETE /blog/posts/:slug` → Delete post

**Features:**
- Automatic slug generation from title
- Draft/published status toggle
- Tag management (array of strings)
- Published timestamp auto-set on publish

#### **`useAdminAlbums.js`** (Admin Albums CRUD)
**Exports:**
- `adminAlbums` (ref): All albums
- `createAlbum(albumData)`: Create new album
- `updateAlbum(slug, albumData)`: Update album
- `deleteAlbum(slug)`: Delete album (cascades to photos)
- `uploadPhoto(file, albumSlug)`: Upload photo to Supabase Storage
- `addPhoto(albumSlug, photoData)`: Add photo record to DB
- `updatePhoto(photoId, photoData)`: Update photo metadata
- `deletePhoto(photoId)`: Delete photo and file
- `reorderPhoto(photoId, newIndex)`: Change photo order

**API Calls:**
- `GET /admin/albums` → All albums with photo counts
- `POST /admin/albums` → Create album
- `PUT /admin/albums/:slug` → Update album
- `DELETE /admin/albums/:slug` → Delete album
- `POST /admin/upload` → Upload file to storage
- `POST /admin/albums/:slug/photos` → Add photo record
- `PUT /admin/photos/:id` → Update photo
- `DELETE /admin/photos/:id` → Delete photo
- `PATCH /admin/photos/:id/reorder` → Reorder photo

**File Upload Flow:**
1. User selects file in `PhotoManager.vue`
2. File sent as `multipart/form-data` to `/admin/upload`
3. Backend generates unique filename: `timestamp-random.ext`
4. Uploads to Supabase Storage: `photos/{albumSlug}/{filename}`
5. Returns public URL
6. Frontend adds photo record to database
7. Photo appears in album

#### **`useChatAssistant.js`** (AI Chatbot Logic)
**Size:** 828 lines (largest composable)

**Exports:**
- `messages` (ref): Conversation history
- `input` (ref): User input text
- `isOpen` (ref): Chat panel open/closed
- `isStreaming` (ref): Response in progress
- `toggleChat()`: Open/close chat
- `sendMessage()`: Send user message to AI
- `clearChat()`: Delete all messages
- `handleStreamError()`: Retry failed requests

**Message Structure:**
```javascript
{
  id: UUID,                    // Unique message ID
  type: 'user' | 'assistant',  // Message sender
  content: String,             // Message text
  timestamp: Date,             // Creation time
  isStreaming: Boolean         // Currently streaming
}
```

**SSE (Server-Sent Events) Flow:**
1. User sends message
2. Frontend opens EventSource to `/chat/stream`
3. Sends POST data with message + history
4. Backend streams chunks via `text/event-stream`
5. Frontend appends chunks to assistant message
6. On complete: `isStreaming = false`
7. Save conversation to localStorage

**Error Handling:**
- Network errors: Show error message with retry
- API errors: Show fallback message
- Rate limiting: Show "too many requests" message
- Timeout: 30 second timeout per request

**Context Management:**
- Sends last 10 messages as conversation history
- Truncates to `CHAT_HISTORY_LIMIT` (10)
- Includes professional info context in system message
- Character limit: 2000 characters per message

**Persistence:**
```javascript
// localStorage keys
'chat_messages'           // Array of message objects
'chat_open'               // Boolean: chat panel state
'chat_timestamp'          // Last activity timestamp
```

#### **`useAsyncRequest.js`** (Shared Async Logic)
**Purpose:** Eliminate duplicated loading/error state management

**Exports:**
- `loading` (ref): Request in progress
- `error` (ref): Error message
- `execute(fn)`: Execute async function with state handling

**Usage Example:**
```javascript
const { loading, error, execute } = useAsyncRequest()

await execute(async () => {
  const response = await fetch('/api/data')
  const data = await response.json()
  items.value = data
})
// loading automatically set to true/false
// error automatically captured
```

**Benefits:**
- Reduces code duplication (~40 lines saved)
- Consistent error handling
- Automatic loading state management

#### **`useStructuredData.js`** (SEO Schema)
**Purpose:** Generate JSON-LD structured data for search engines

**Exports:**
- `generatePersonSchema()`: Schema.org Person
- `generateOrganizationSchema()`: Schema.org Organization
- `generateBlogPostSchema(post)`: Schema.org BlogPosting
- `generateBlogListSchema(posts)`: Schema.org ItemList
- `generateBreadcrumbSchema(items)`: Schema.org BreadcrumbList
- `generateWorkExperienceSchema(experience)`: Schema.org WorkExperience
- `generateProjectsListSchema(projects)`: Schema.org ItemList

**JSON-LD Example (Blog Post):**
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Getting Started with Vue 3",
  "author": {
    "@type": "Person",
    "name": "Richwell Perez"
  },
  "datePublished": "2025-01-15",
  "image": "https://richwellp.github.io/og-image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Richwell Perez - Portfolio"
  }
}
```

**SEO Benefits:**
- Rich snippets in Google search
- Enhanced search result appearance
- Better discoverability
- Proper attribution

#### **`useSanitizer.js`** (XSS Protection)
**Purpose:** Sanitize HTML to prevent XSS attacks

**Exports:**
- `sanitizeHtml(html, config)`: Sanitize HTML string

**DOMPurify Configuration:**
```javascript
{
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
  ALLOWED_ATTR: [
    'href', 'src', 'alt', 'title',
    'class', 'id',
    'target', 'rel',
    'width', 'height'
  ],
  ALLOW_DATA_ATTR: false,
  ADD_ATTR: ['target', 'rel']
}
```

**Usage:**
- Blog post content rendering
- Chat message rendering
- Any user-generated content

**Security:**
- Removes `<script>` tags
- Removes inline event handlers (`onclick`, etc.)
- Removes dangerous attributes (`onerror`, `onload`)
- Allows safe HTML for formatting

#### **`useSearch.js`** (Professional Info Search)
**Purpose:** Search across experience, projects, skills

**Exports:**
- `searchQuery` (ref): Current search query
- `searchResults` (ref): Filtered results
- `recentSearches` (ref): Recent search history
- `performSearch(query)`: Execute search
- `clearSearch()`: Reset search state

**Search Algorithm:**
1. Load `professionalInfo.json`
2. Search across:
   - Experience titles, companies, descriptions, technologies
   - Project names, descriptions, technologies
   - Skills names, categories
3. Rank by relevance (title match > description match)
4. Return top 20 results
5. Save to recent searches (localStorage)

**Search Indexing:**
- Lowercased for case-insensitive search
- Searches all text fields
- Highlights matching sections

#### **`useVisitorMap.js`** (Visitor Tracking)
**Purpose:** Display visitor locations on interactive map

**Exports:**
- `visitors` (ref): Array of visitor locations
- `fetchVisitors()`: Get visitor geolocation data

**Note:** Currently console-only implementation (privacy-focused)
- Can be extended with IP geolocation API
- Can be displayed on world map component
- Respects user privacy (no PII stored)

### Configuration Files

#### **`frontend/src/config/api.js`**
**Purpose:** Centralized API endpoint configuration

**Exports:**
```javascript
export const API_BASE_URL = import.meta.env.VITE_API_URL
export const API_ENDPOINTS = {
  authLogin: `${API_BASE_URL}/auth/login`,
  authLogout: `${API_BASE_URL}/auth/logout`,
  chat: `${API_BASE_URL}/chat`,
  chatStream: `${API_BASE_URL}/chat/stream`,
  blogPosts: `${API_BASE_URL}/blog/posts`,
  blogPost: (slug) => `${API_BASE_URL}/blog/posts/${slug}`,
  albums: `${API_BASE_URL}/albums`,
  album: (slug) => `${API_BASE_URL}/albums/${slug}`,
  adminAlbums: `${API_BASE_URL}/admin/albums`,
  // ... more endpoints
}
```

**Environment Variable:**
- Development: `http://localhost:5000`
- Production: `https://richwellp-github-io.vercel.app`

#### **`frontend/src/config/constants.js`**
**Purpose:** App-wide constants

**Exports:**
```javascript
export const MESSAGE_MAX_LENGTH = 2000       // Chat message limit
export const CHAT_HISTORY_LIMIT = 10         // Context messages
export const WORDS_PER_MINUTE = 200          // Reading speed
export const DEFAULT_PAGE_SIZE = 10          // Pagination
export const STORAGE_KEYS = {
  chatMessages: 'chat_messages',
  recentSearches: 'recent_searches'
}
```

#### **`frontend/src/config/contact.js`**
**Purpose:** Contact information

**Exports:**
```javascript
export const CONTACT = {
  email: 'richwell.perez@gmail.com',
  linkedin: 'https://www.linkedin.com/in/richwell-perez',
  github: 'https://github.com/richwellp',
  getContactMessage(): String,
  getEmailOnly(): String
}
```

#### **`frontend/src/config/site.js`**
**Purpose:** Site metadata

**Exports:**
```javascript
export const SITE_URL = 'https://richwellp.github.io'
export const SITE_NAME = 'Richwell Perez - Portfolio'
export const SITE_DESCRIPTION = 'Personal portfolio showcasing software engineering work...'
```

### Build Configuration

#### **`frontend/vite.config.js`**
```javascript
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router'],
          'markdown': ['markdown-it', 'dompurify']
        }
      }
    }
  }
})
```

**Features:**
- `@` alias for `src` directory
- Code splitting: vendor, markdown chunks
- Production optimizations
- No sourcemaps in production

#### **`frontend/vitest.config.js`**
```javascript
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.js',
    coverage: {
      reporter: ['text', 'html'],
      exclude: ['node_modules/', 'tests/']
    }
  }
})
```

**Testing Setup:**
- JSDOM environment (simulates browser)
- Global test functions (describe, it, expect)
- Code coverage reporting

---

## Backend Deep Dive

### Flask Application Structure

#### **`backend/app.py`** (Application Entry Point)
```python
from flask import Flask
from flask_cors import CORS
from flask_compress import Compress

app = Flask(__name__)

# Enable CORS
CORS(app, resources={
    r"/*": {
        "origins": ["https://richwellp.github.io", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Enable gzip compression
Compress(app)

# Register blueprints
from api import blog_bp, albums_bp, gemini_bp, sitemap_bp
app.register_blueprint(blog_bp)
app.register_blueprint(albums_bp)
app.register_blueprint(gemini_bp)
app.register_blueprint(sitemap_bp)

# Health check
@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Portfolio API'}

if __name__ == '__main__':
    app.run(debug=True)
```

**Key Features:**
- CORS enabled for frontend origins
- Gzip compression for smaller responses
- Blueprint architecture (modular routes)
- Health check endpoint

### Authentication System

#### **`backend/auth.py`**
```python
import os
from functools import wraps
from flask import request, jsonify, make_response

ADMIN_KEY = os.getenv('BLOG_ADMIN_KEY')
COOKIE_NAME = 'admin_session'
COOKIE_MAX_AGE = 24 * 60 * 60  # 24 hours

# Detect production environment (Vercel or FLASK_ENV=production)
IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production' or os.getenv('VERCEL_ENV') is not None

def require_admin(f):
    """Decorator to protect admin endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Try cookie-based auth first (preferred)
        cookie_token = request.cookies.get(COOKIE_NAME)
        if cookie_token and cookie_token == ADMIN_KEY:
            return f(*args, **kwargs)

        # Fall back to header-based auth (legacy)
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer ') and auth[7:] == ADMIN_KEY:
            return f(*args, **kwargs)

        return jsonify(error='Unauthorized'), 401
    return decorated

def create_admin_cookie_response(data, status=200):
    """Create response with httpOnly secure cookie"""
    response = make_response(jsonify(data), status)
    response.set_cookie(
        COOKIE_NAME,
        value=ADMIN_KEY,
        max_age=COOKIE_MAX_AGE,
        secure=IS_PRODUCTION,  # HTTPS-only in production
        httponly=True,  # Not accessible via JavaScript (XSS protection)
        samesite='None' if IS_PRODUCTION else 'Lax'  # Cross-origin support
    )
    return response
```

**Authentication Flow:**
1. Admin enters password
2. `POST /auth/login` validates password against `BLOG_ADMIN_KEY`
3. If valid: sets httpOnly secure cookie (24h expiry)
4. Browser automatically sends cookie with subsequent requests
5. Protected routes check for valid cookie
6. `@require_admin` decorator verifies cookie or Bearer token (legacy)

**Security:**
- **HttpOnly cookies** (not accessible to JavaScript, prevents XSS)
- **Secure flag** (HTTPS-only in production)
- **SameSite=None in production** (enables cross-origin between GitHub Pages → Vercel)
- **SameSite=Lax in development** (localhost testing)
- **24-hour expiry** (automatic session timeout)
- **Legacy Bearer token support** (backwards compatibility)
- **No password stored in database**
- Single admin user model

### API Blueprints

#### **`backend/api/blog.py`** (Blog Endpoints)

**Public Endpoints (No Auth):**

```python
@blog_bp.route('/blog/posts', methods=['GET'])
def list_posts():
    """
    GET /blog/posts?page=1&per_page=10
    Returns published blog posts with pagination
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    result = supabase.table('blog_posts')\
        .select('id,slug,title,excerpt,author,tags,published_at')\
        .eq('published', True)\
        .order('published_at', desc=True)\
        .range((page-1)*per_page, page*per_page-1)\
        .execute()

    return jsonify({'posts': result.data, 'page': page})

@blog_bp.route('/blog/posts/<slug>', methods=['GET'])
def get_post(slug):
    """
    GET /blog/posts/:slug
    Returns single published post with reading time
    """
    result = supabase.table('blog_posts')\
        .select('*')\
        .eq('slug', slug)\
        .eq('published', True)\
        .single()\
        .execute()

    post = result.data
    post['reading_time'] = calculate_reading_time(post['content'])
    post['headings'] = extract_headings(post['content'])

    return jsonify(post)

@blog_bp.route('/blog/search', methods=['GET'])
def search_posts():
    """
    GET /blog/search?q=vue
    Full-text search across title and content
    """
    query = request.args.get('q', '')

    # PostgreSQL full-text search
    result = supabase.rpc('search_blog_posts', {'search_query': query}).execute()

    return jsonify({'posts': result.data, 'query': query})
```

**Admin Endpoints (Require Auth):**

```python
@blog_bp.route('/blog/admin/posts', methods=['GET'])
@require_admin
def admin_list_posts():
    """
    GET /blog/admin/posts?status=draft
    Returns all posts including drafts
    """
    status = request.args.get('status')

    query = supabase.table('blog_posts').select('*')

    if status == 'published':
        query = query.eq('published', True)
    elif status == 'draft':
        query = query.eq('published', False)

    result = query.order('created_at', desc=True).execute()

    return jsonify({'posts': result.data})

@blog_bp.route('/blog/posts', methods=['POST'])
@require_admin
def create_post():
    """
    POST /blog/posts
    Create new blog post
    """
    data = request.json

    result = supabase.table('blog_posts').insert({
        'slug': data['slug'],
        'title': data['title'],
        'content': data['content'],
        'excerpt': data.get('excerpt', ''),
        'tags': data.get('tags', []),
        'published': data.get('published', False)
    }).execute()

    return jsonify({'post': result.data[0]}), 201

@blog_bp.route('/blog/posts/<slug>', methods=['PUT'])
@require_admin
def update_post(slug):
    """
    PUT /blog/posts/:slug
    Update existing post
    """
    data = request.json

    result = supabase.table('blog_posts')\
        .update(data)\
        .eq('slug', slug)\
        .execute()

    return jsonify({'post': result.data[0]})

@blog_bp.route('/blog/posts/<slug>', methods=['DELETE'])
@require_admin
def delete_post(slug):
    """
    DELETE /blog/posts/:slug
    Delete post
    """
    supabase.table('blog_posts').delete().eq('slug', slug).execute()
    return '', 204
```

**Helper Functions:**

```python
def calculate_reading_time(content):
    """Calculate reading time in minutes"""
    words = len(content.split())
    return max(1, words // 200)

def extract_headings(content):
    """Extract h2/h3 headings for TOC"""
    import re
    headings = []
    for match in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2)
        headings.append({'level': level, 'text': text})
    return headings
```

#### **`backend/api/albums.py`** (Albums Endpoints)

**Public Endpoints:**

```python
@albums_bp.route('/albums', methods=['GET'])
def list_albums():
    """
    GET /albums
    Returns published albums with cover photos
    """
    albums_result = supabase.table('albums')\
        .select('id,slug,name,subtitle,order_index')\
        .eq('published', True)\
        .order('order_index')\
        .execute()

    albums = albums_result.data

    # Get cover photo for each album (prefer videos)
    for album in albums:
        photos_result = supabase.table('photos')\
            .select('url')\
            .eq('album_id', album['id'])\
            .order('order_index')\
            .limit(1)\
            .execute()

        if photos_result.data:
            album['cover_photo'] = photos_result.data[0]['url']

    return jsonify({'albums': albums})

@albums_bp.route('/albums/<slug>', methods=['GET'])
def get_album(slug):
    """
    GET /albums/:slug
    Returns album with all photos grouped by category
    """
    album_result = supabase.table('albums')\
        .select('*')\
        .eq('slug', slug)\
        .single()\
        .execute()

    album = album_result.data

    photos_result = supabase.table('photos')\
        .select('*')\
        .eq('album_id', album['id'])\
        .order('order_index')\
        .execute()

    # Group photos by category
    photos_by_category = {}
    for photo in photos_result.data:
        category = photo.get('category', 'uncategorized')
        if category not in photos_by_category:
            photos_by_category[category] = []
        photos_by_category[category].append(photo)

    album['photos'] = photos_by_category

    return jsonify(album)
```

**Admin Endpoints:**

```python
@albums_bp.route('/admin/albums', methods=['GET'])
@require_admin
def admin_list_albums():
    """
    GET /admin/albums
    Returns all albums with photo counts
    """
    albums = supabase.table('albums').select('*').order('order_index').execute().data

    # Add photo counts
    for album in albums:
        count = supabase.table('photos')\
            .select('id', count='exact')\
            .eq('album_id', album['id'])\
            .execute()
        album['photo_count'] = count.count

    return jsonify({'albums': albums})

@albums_bp.route('/admin/upload', methods=['POST'])
@require_admin
def admin_upload_file():
    """
    POST /admin/upload
    Upload file to Supabase Storage

    Expects multipart/form-data:
    - file: File to upload
    - album: Album slug
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    album_slug = request.form.get('album')

    # Generate unique filename
    import time, random, string
    file_ext = file.filename.rsplit('.', 1)[1]
    timestamp = int(time.time() * 1000)
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    filename = f"{timestamp}-{random_str}.{file_ext}"
    filepath = f"{album_slug}/{filename}"

    # Upload to Supabase Storage
    file_content = file.read()
    supabase.storage.from_('photos').upload(
        filepath,
        file_content,
        file_options={
            "content-type": file.content_type,
            "cache-control": "2592000"  # 30 days
        }
    )

    # Get public URL
    url = supabase.storage.from_('photos').get_public_url(filepath)

    return jsonify({'url': url, 'path': filepath}), 201

@albums_bp.route('/admin/albums/<slug>/photos', methods=['POST'])
@require_admin
def admin_add_photo(slug):
    """
    POST /admin/albums/:slug/photos
    Add photo record to database
    """
    data = request.json

    # Get album ID
    album = supabase.table('albums').select('id').eq('slug', slug).single().execute()

    # Insert photo
    result = supabase.table('photos').insert({
        'album_id': album.data['id'],
        'url': data['url'],
        'caption': data.get('caption'),
        'category': data.get('category'),
        'order_index': data.get('order_index', 0)
    }).execute()

    return jsonify({'photo': result.data[0]}), 201

@albums_bp.route('/admin/photos/<photo_id>', methods=['PUT'])
@require_admin
def admin_update_photo(photo_id):
    """
    PUT /admin/photos/:id
    Update photo metadata
    """
    data = request.json

    result = supabase.table('photos')\
        .update(data)\
        .eq('id', photo_id)\
        .execute()

    return jsonify({'photo': result.data[0]})

@albums_bp.route('/admin/photos/<photo_id>', methods=['DELETE'])
@require_admin
def admin_delete_photo(photo_id):
    """
    DELETE /admin/photos/:id
    Delete photo and file from storage
    """
    # Get photo to find file path
    photo = supabase.table('photos').select('url').eq('id', photo_id).single().execute()

    # Delete from storage
    file_path = extract_file_path(photo.data['url'])
    supabase.storage.from_('photos').remove([file_path])

    # Delete from database
    supabase.table('photos').delete().eq('id', photo_id).execute()

    return '', 204

@albums_bp.route('/admin/photos/<photo_id>/reorder', methods=['PATCH'])
@require_admin
def admin_reorder_photo(photo_id):
    """
    PATCH /admin/photos/:id/reorder
    Change photo order_index
    """
    data = request.json
    new_index = data['order_index']

    result = supabase.table('photos')\
        .update({'order_index': new_index})\
        .eq('id', photo_id)\
        .execute()

    return jsonify({'photo': result.data[0]})
```

#### **`backend/api/gemini.py`** (AI Chatbot)

**Configuration:**
```python
import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config={
        'temperature': 0.7,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 2048,
    },
    safety_settings={
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_MEDIUM_AND_ABOVE',
    }
)
```

**Streaming Endpoint:**
```python
@gemini_bp.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    POST /chat/stream
    Stream AI response via Server-Sent Events (SSE)

    Request body:
    {
      "message": "What is Vue 3?",
      "history": [
        {"role": "user", "parts": ["Previous message"]},
        {"role": "model", "parts": ["Previous response"]}
      ],
      "professionalInfo": { ... }
    }
    """
    data = request.json
    user_message = data.get('message', '')
    history = data.get('history', [])
    professional_info = data.get('professionalInfo', {})

    # Build context
    system_instruction = build_system_instruction(professional_info)

    # Create chat session
    chat = model.start_chat(history=history)

    def generate():
        try:
            response = chat.send_message(
                user_message,
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    # Send SSE event
                    yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

def build_system_instruction(professional_info):
    """
    Build AI system prompt with context about Richwell
    """
    experience = professional_info.get('experience', [])
    projects = professional_info.get('projects', [])
    skills = professional_info.get('skills', [])

    prompt = f"""
    You are Richwell's AI assistant on his portfolio website.

    ABOUT RICHWELL:
    - Name: Richwell Perez
    - Email: richwell.perez@gmail.com
    - Location: Laramie, WY / Brea, CA

    CURRENT ROLE:
    {experience[0]['title']} at {experience[0]['company']}
    {experience[0]['description']}

    KEY PROJECTS:
    {format_projects(projects)}

    SKILLS:
    {format_skills(skills)}

    INSTRUCTIONS:
    - Answer questions about Richwell's background, experience, and projects
    - Be friendly, professional, and concise
    - If asked about contact: provide email and LinkedIn
    - If unsure: say you don't have that information
    - Keep responses under 200 words unless asked for more detail
    """

    return prompt
```

**SSE Format:**
```
data: {"chunk": "This"}
data: {"chunk": " is"}
data: {"chunk": " streaming"}
data: {"done": true}
```

**Rate Limiting:**
- Gemini Free Tier: 15 requests/minute, 1500 requests/day
- No backend rate limiting (relies on Gemini API limits)
- Frontend debounces input to prevent spam

**Context Window:**
- Last 10 messages sent as history
- Professional info included in every request
- Token limit: ~8000 tokens (Gemini 2.5 Flash)

#### **`backend/api/sitemap.py`** (Dynamic Sitemap)

```python
@sitemap_bp.route('/sitemap.xml', methods=['GET'])
def dynamic_sitemap():
    """
    GET /sitemap.xml
    Generate dynamic sitemap with blog posts and albums
    """
    # Static pages
    urls = [
        {'loc': 'https://richwellp.github.io/', 'priority': 1.0},
        {'loc': 'https://richwellp.github.io/experience', 'priority': 0.9},
        {'loc': 'https://richwellp.github.io/projects', 'priority': 0.9},
        {'loc': 'https://richwellp.github.io/about', 'priority': 0.8},
        {'loc': 'https://richwellp.github.io/contact', 'priority': 0.7},
        {'loc': 'https://richwellp.github.io/misc/blog', 'priority': 0.8},
        {'loc': 'https://richwellp.github.io/misc/albums', 'priority': 0.8},
    ]

    # Blog posts
    posts = supabase.table('blog_posts')\
        .select('slug,updated_at')\
        .eq('published', True)\
        .execute()

    for post in posts.data:
        urls.append({
            'loc': f'https://richwellp.github.io/misc/blog/{post["slug"]}',
            'lastmod': post['updated_at'],
            'priority': 0.7
        })

    # Albums
    albums = supabase.table('albums')\
        .select('slug,updated_at')\
        .eq('published', True)\
        .execute()

    for album in albums.data:
        urls.append({
            'loc': f'https://richwellp.github.io/misc/albums/{album["slug"]}',
            'lastmod': album['updated_at'],
            'priority': 0.7
        })

    # Generate XML
    xml = generate_sitemap_xml(urls)

    return Response(xml, mimetype='application/xml')

def generate_sitemap_xml(urls):
    """Generate sitemap XML from URL list"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        if 'lastmod' in url:
            xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>'
    return xml
```

**SEO Benefits:**
- Search engines discover new blog posts automatically
- Priority indicates page importance
- Last modified date for freshness
- Includes all public content

### Configuration

#### **`backend/config.py`**
```python
import os

# Contact Information
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'richwell.perez@gmail.com')
CONTACT_LINKEDIN = os.environ.get('CONTACT_LINKEDIN', 'linkedin.com/in/richwell-perez')

# Rate Limiting
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60  # seconds

# Message Constraints
MESSAGE_LENGTH_LIMIT = 2000
HISTORY_LIMIT = 20

# Gemini Configuration
GEMINI_MODEL = 'gemini-2.5-flash'

# Blog Configuration
DEFAULT_PAGE_SIZE = 10
WORDS_PER_MINUTE = 200
DEFAULT_READING_TIME_ESTIMATE = 5

def get_contact_message():
    return f"Please reach out directly at {CONTACT_EMAIL} or {CONTACT_LINKEDIN}."
```

### Deployment Configuration

#### **`backend/vercel.json`**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

**Vercel Deployment:**
- Serverless Flask (AWS Lambda)
- Auto-scaling
- Global CDN
- Environment variables in Vercel dashboard

---

## Database Architecture

### Supabase PostgreSQL Schema

#### **Blog Posts Table** (`blog_posts`)

```sql
CREATE TABLE blog_posts (
  id BIGSERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  excerpt TEXT DEFAULT '',
  author TEXT DEFAULT 'Richwell Perez',
  tags TEXT[] DEFAULT '{}',
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMPTZ,
  reading_time INTEGER DEFAULT 5,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes:**
```sql
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_published ON blog_posts(published);
CREATE INDEX idx_blog_posts_published_at ON blog_posts(published_at DESC);
CREATE INDEX idx_blog_posts_tags ON blog_posts USING GIN(tags);
CREATE INDEX idx_blog_posts_title_search ON blog_posts USING GIN(to_tsvector('english', title));
CREATE INDEX idx_blog_posts_content_search ON blog_posts USING GIN(to_tsvector('english', content));
```

**Triggers:**
```sql
-- Auto-update updated_at timestamp
CREATE TRIGGER update_blog_posts_updated_at
  BEFORE UPDATE ON blog_posts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Auto-set published_at when publishing
CREATE TRIGGER set_published_at_trigger
  BEFORE UPDATE ON blog_posts
  FOR EACH ROW
  EXECUTE FUNCTION set_published_at();
```

**Row Level Security (RLS):**
```sql
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- Public can read published posts
CREATE POLICY "Published posts are viewable by everyone"
ON blog_posts FOR SELECT
USING (published = TRUE);

-- Admin operations use service_role key (bypasses RLS)
```

#### **Albums Table** (`albums`)

```sql
CREATE TABLE albums (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  icon TEXT NOT NULL DEFAULT '📷',
  subtitle TEXT,
  categories TEXT[] DEFAULT NULL,
  order_index INTEGER DEFAULT 0,
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes:**
```sql
CREATE INDEX idx_albums_slug ON albums(slug);
CREATE INDEX idx_albums_order ON albums(order_index);
CREATE INDEX idx_albums_published ON albums(published);
```

**Triggers:**
```sql
CREATE TRIGGER update_albums_updated_at
  BEFORE UPDATE ON albums
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

**RLS:**
```sql
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read access to albums"
ON albums FOR SELECT
USING (true);
```

#### **Photos Table** (`photos`)

```sql
CREATE TABLE photos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  album_id UUID NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  caption TEXT,
  location TEXT,
  date_taken DATE,
  category TEXT,
  order_index INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes:**
```sql
CREATE INDEX idx_photos_album_id ON photos(album_id);
CREATE INDEX idx_photos_category ON photos(category);
CREATE INDEX idx_photos_date_taken ON photos(date_taken);
CREATE INDEX idx_photos_order ON photos(album_id, order_index);
```

**Triggers:**
```sql
CREATE TRIGGER update_photos_updated_at
  BEFORE UPDATE ON photos
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

**RLS:**
```sql
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read access to photos"
ON photos FOR SELECT
USING (true);
```

**Cascade Deletion:**
- Deleting an album automatically deletes all its photos
- Foreign key constraint: `ON DELETE CASCADE`

### Supabase Storage

**Bucket:** `photos` (public)

**Structure:**
```
photos/
├── travel/
│   ├── 1704326400000-abc123.jpg
│   ├── 1704326500000-def456.mp4
│   └── ...
├── sports/
│   ├── 1704326600000-ghi789.jpg
│   └── ...
└── me/
    ├── 1704326700000-jkl012.jpg
    └── ...
```

**File Naming:**
- Format: `{timestamp}-{random}.{ext}`
- Example: `1704326400000-abc123.jpg`
- Timestamp: milliseconds since epoch
- Random: 7-character alphanumeric
- Prevents naming conflicts

**Public URLs:**
```
https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/1704326400000-abc123.jpg
```

**Storage Policies:**
- Public read access (no auth required)
- Write access via service_role key (backend only)
- 30-day cache headers for performance

---

## Deployment Pipeline

### GitHub Actions Workflow

**`.github/workflows/ci-cd.yml`**

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest -v
        env:
          BLOG_ADMIN_KEY: test-admin-key

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: |
          cd frontend
          npm ci
          npm test -- --run

  build-frontend:
    needs: [backend-tests, frontend-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: |
          cd frontend
          npm ci
          npm run build
        env:
          VITE_API_URL: https://richwellp-github-io.vercel.app
      - uses: actions/upload-pages-artifact@v3
        with:
          path: frontend/dist

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: [build-frontend]
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

### Deployment Flow

```
git push origin main
    │
    ├─► GitHub Actions Trigger
    │
    ├─► Backend Tests (50 tests)
    │   ├─ Setup Python 3.11
    │   ├─ Install dependencies
    │   └─ Run pytest
    │
    ├─► Frontend Tests (47+ tests)
    │   ├─ Setup Node 20
    │   ├─ npm ci
    │   └─ npm test
    │
    ├─► Build Frontend
    │   ├─ npm run build
    │   ├─ Generate dist/
    │   └─ Upload artifact
    │
    └─► Deploy to GitHub Pages
        └─ Deploy dist/ to richwellp.github.io
```

**Backend Deployment (Vercel):**
```
git push origin main
    │
    └─► Vercel Git Integration
        ├─ Detects changes in backend/
        ├─ Builds Flask app
        ├─ Deploys to serverless
        └─ Live at: richwellp-github-io.vercel.app
```

### Environment Variables

**Frontend (.env):**
```
VITE_API_URL=https://richwellp-github-io.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGci...
```

**Backend (Vercel Dashboard):**
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGci... (service_role key)
BLOG_ADMIN_KEY=your-secure-password
GEMINI_API_KEY=AIza...
ALLOWED_ORIGINS=https://richwellp.github.io,http://localhost:5173
```

---

## Development Workflow

### Local Development Setup

**1. Clone Repository:**
```bash
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io
```

**2. Backend Setup:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "SUPABASE_URL=https://your-project.supabase.co" > .env
echo "SUPABASE_KEY=your_service_role_key" >> .env
echo "BLOG_ADMIN_KEY=your_admin_password" >> .env
echo "GEMINI_API_KEY=your_gemini_key" >> .env

# Run tests
python -m pytest -v

# Run development server
flask run  # http://localhost:5000
```

**3. Frontend Setup:**
```bash
cd frontend
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5000" > .env
echo "VITE_SUPABASE_URL=https://your-project.supabase.co" >> .env
echo "VITE_SUPABASE_ANON_KEY=your_anon_key" >> .env

# Run tests
npm test -- --run

# Run development server
npm run dev  # http://localhost:5173
```

**4. Database Setup:**
- Go to Supabase SQL Editor
- Run `backend/database/blog_schema.sql`
- Run `backend/database/albums_schema.sql`
- Run `backend/database/seed_initial_albums.sql`

### Development Commands

**Frontend:**
```bash
npm run dev          # Start dev server (HMR enabled)
npm run build        # Build for production
npm run preview      # Preview production build
npm test             # Run tests in watch mode
npm test -- --run    # Run tests once
npm run lint         # Lint code
```

**Backend:**
```bash
flask run            # Start dev server (debug mode)
python -m pytest     # Run all tests
python -m pytest -v  # Run with verbose output
python -m pytest backend/tests/test_blog.py  # Run specific test file
python -m pytest -k "test_create_post"       # Run tests matching pattern
```

### Code Style & Standards

**Python (Backend):**
- PEP 8 style guide
- 4-space indentation
- Docstrings for all functions
- Type hints where applicable
- Max line length: 100 characters

**JavaScript (Frontend):**
- ESLint + Prettier
- 2-space indentation
- Single quotes for strings
- Semicolons optional
- Composition API with `<script setup>`

**Vue SFC Structure:**
```vue
<template>
  <!-- HTML template -->
</template>

<script setup>
// Composition API logic
</script>

<style scoped>
/* Component-specific styles */
</style>
```

### Testing Strategy

**Frontend Tests (Vitest):**
- Composable unit tests
- Component integration tests
- Mocked API responses
- Coverage: ~70%

**Backend Tests (pytest):**
- Endpoint integration tests
- Mocked Supabase responses
- Authentication tests
- Coverage: ~80%

**Example Test:**
```python
def test_create_post_requires_auth():
    """Test that creating a post requires authentication"""
    response = client.post('/blog/posts', json={
        'title': 'Test Post',
        'content': 'Test content'
    })

    assert response.status_code == 401
    assert 'Authentication required' in response.json['error']
```

---

## Security Architecture

### Authentication & Authorization

**Admin Authentication:**
1. Single admin user model
2. Password-based login (`BLOG_ADMIN_KEY`)
3. HttpOnly secure cookies (24-hour expiry)
4. Cookies automatically sent by browser (not stored in localStorage)
5. Cross-origin support with `SameSite=None` in production
6. Backend validates with `@require_admin` decorator
7. Legacy Bearer token support for backwards compatibility

**No User Registration:**
- Portfolio is single-admin
- No multi-user support needed
- Simplifies security model

### Database Security (RLS)

**Row Level Security Policies:**

```sql
-- Blog: Public can only read published posts
CREATE POLICY "Published posts are viewable by everyone"
ON blog_posts FOR SELECT
USING (published = TRUE);

-- Albums: Public can read all albums
CREATE POLICY "Public read access to albums"
ON albums FOR SELECT
USING (true);

-- Photos: Public can read all photos
CREATE POLICY "Public read access to photos"
ON photos FOR SELECT
USING (true);
```

**Service Role Key:**
- Backend uses service_role key
- Bypasses RLS for admin operations
- Never exposed to frontend

**Anon Key:**
- Frontend uses anon key
- Respects RLS policies
- Safe to expose (public data only)

### XSS Protection

**DOMPurify Sanitization:**
- All user-generated content sanitized
- Removes `<script>` tags
- Removes inline event handlers
- Allows safe HTML formatting

**Content Security Policy (CSP):**
- Could be added for additional protection
- Not currently implemented

### CORS Configuration

```python
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://richwellp.github.io",
            "http://localhost:5173"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Environment Variables

**Never Committed:**
- API keys
- Database credentials
- Admin passwords

**Stored in:**
- Local: `.env` files (gitignored)
- Production: Vercel dashboard

### Rate Limiting

**Gemini API:**
- Free tier: 15 RPM, 1500 RPD
- Enforced by Google
- No backend rate limiting

**Potential Additions:**
- Flask-Limiter for API endpoints
- IP-based rate limiting
- CAPTCHA for public forms

---

## Performance Optimizations

### Frontend Optimizations

**Code Splitting:**
- Vue Router lazy loading: `component: () => import('./views/Home.vue')`
- Vendor chunks: Vue, Vue Router, markdown-it
- Reduces initial bundle size

**Image Optimization:**
- Lazy loading with `loading="lazy"`
- Responsive images with `srcset`
- WebP format where supported
- Supabase Storage CDN

**Caching:**
- Service Worker (could be added)
- localStorage for chat history
- 30-day cache headers on photos

**Build Optimizations:**
- Vite production build (minification, tree-shaking)
- Asset hashing for cache busting
- Gzip compression via Vercel

### Backend Optimizations

**Database Indexing:**
- Indexes on frequently queried columns
- GIN indexes for full-text search
- Composite indexes for complex queries

**Response Compression:**
- Flask-Compress (gzip)
- Reduces response size by ~70%

**Caching:**
- Could add Redis for query caching
- Not currently implemented (serverless constraints)

**Serverless Benefits:**
- Auto-scaling
- Global CDN
- No cold start issues (Flask is fast)

---

## Future Enhancements

### Planned Features
1. **Blog Comments:** Supabase-powered comments system
2. **Analytics Dashboard:** Page views, popular posts
3. **Newsletter:** Email subscription via Supabase Edge Functions
4. **Dark/Light Theme Toggle:** User preference persistence
5. **Advanced Search:** Elasticsearch integration
6. **RSS Feed:** Auto-generated blog RSS
7. **Sitemap Automation:** Update on blog post creation

### Technical Debt
1. **Frontend Test Coverage:** Increase from 70% to 90%
2. **Backend Error Handling:** Standardize error responses
3. **API Versioning:** `/api/v1/` prefix
4. **Rate Limiting:** Add Flask-Limiter
5. **Monitoring:** Add Sentry for error tracking
6. **CI/CD:** Add Lighthouse performance tests

---

## Troubleshooting Guide

### Common Issues

**Frontend Build Fails:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check environment variables
cat .env

# Rebuild
npm run build
```

**Backend Tests Fail:**
```bash
# Check Python version (must be 3.11+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check environment variables
cat .env

# Rerun tests
python -m pytest -v
```

**Database Connection Error:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check Supabase project status
- Verify RLS policies don't block queries

**Chatbot Not Working:**
- Check `GEMINI_API_KEY` in Vercel dashboard
- Verify Gemini API quota (15 RPM limit)
- Check browser console for errors

**Photos Not Uploading:**
- Verify admin authentication token
- Check Supabase Storage bucket exists
- Verify `photos` bucket is public
- Check file size (max 50MB)

---

## Glossary

**SSE (Server-Sent Events):** HTTP standard for server-to-client streaming
**RLS (Row Level Security):** PostgreSQL feature for data access control
**SPA (Single Page Application):** Frontend that loads once, updates dynamically
**HMR (Hot Module Replacement):** Live code updates without page refresh
**TDD (Test-Driven Development):** Write tests before code
**CORS (Cross-Origin Resource Sharing):** Browser security for API requests
**XSS (Cross-Site Scripting):** Security vulnerability via injected scripts
**SEO (Search Engine Optimization):** Improving search engine visibility
**CDN (Content Delivery Network):** Distributed file hosting

---

**Last Updated:** 2025-01-26
**Version:** 1.0
**Maintainer:** Richwell Perez (richwell.perez@gmail.com)
