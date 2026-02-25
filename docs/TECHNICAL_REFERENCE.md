# Technical Reference

Complete file-by-file documentation of the codebase.

---

## Frontend Files

### Root Configuration

**`package.json`**
- Dependencies: Vue 3, Vite, Vue Router, markdown-it, DOMPurify, Supabase client
- Scripts: `dev` (localhost:5173), `build` (production), `test` (vitest), `preview` (test build locally)

**`vite.config.js`**
- Vite configuration: Vue plugin, path aliases (`@` → `src/`), dev server port 5173
- Build output: `dist/` folder
- Defines: Process environment variables for browser

**`index.html`**
- Entry point: Loads `src/main.js`
- Mounts Vue app to `<div id="app">`

---

### Source Files

#### `src/main.js`

Entry point for Vue app.

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

Creates Vue instance, adds router, mounts to DOM.

---

#### `src/App.vue`

Root component with layout and navigation.

**Template:**
- `<Navbar>` - Top navigation
- `<router-view>` - Page content (changes based on route)
- `<ChatAssistant>` - AI chatbot (bottom right)
- `<CommandPalette>` - Cmd/Ctrl+K quick nav

**Script:**
- `onMounted`: Loads blog posts, professional info, preloads chat context
- Theme management (dark mode)
- Search functionality
- Global keyboard shortcuts (Cmd/Ctrl+K)

**Style:**
- CSS variables (colors, spacing, fonts)
- Dark theme colors
- Global styles

---

### Router

#### `src/router/index.js`

Client-side routing with Vue Router.

**Routes:**
```javascript
'/' → Home.vue
'/experience' → Experience.vue
'/projects' → Projects.vue
'/misc' → Misc.vue (albums + blog)
'/misc/blog' → BlogList.vue
'/misc/blog/:slug' → BlogPost.vue
'/misc/albums/:slug' → AlbumView.vue
'/admin' → AdminPanel.vue
'/admin/new' → PostEditor.vue (create)
'/admin/edit/:slug' → PostEditor.vue (edit)
'/contact' → Contact.vue
```

**Features:**
- Lazy loading: `component: () => import('./views/Page.vue')`
- Scroll behavior: Scroll to top on route change
- History mode: Uses browser history API (no # in URLs)

---

### Views

#### `src/views/Home.vue`

Landing page.

**Sections:**
- Hero with name, title, CTA buttons
- Featured projects (from professionalInfo.json)
- Recent blog posts (from API)
- Skills showcase
- Call to action

**Data sources:**
- Professional info: `useProfessionalInfo()`
- Blog posts: `useBlog()`

---

#### `src/views/Experience.vue`

Work experience timeline.

**Data:** `frontend/public/data/professionalInfo.json`
**Display:** Timeline format with company, role, dates, highlights, technologies

---

#### `src/views/Projects.vue`

Project showcase.

**Data:** `frontend/public/data/professionalInfo.json`
**Display:** Grid of project cards with title, description, tech stack, links

---

#### `src/views/Misc.vue`

Combined albums and blog listing.

**Features:**
- Photo album grid (from Supabase)
- Blog post cards (from API)
- Category filters

---

#### `src/views/Contact.vue`

Contact form.

**Fields:** Name, email, message
**Validation:** Client-side validation before submit
**Action:** Currently displays contact info (no backend submission)

---

#### `src/views/blog/BlogList.vue`

Blog post listing with pagination.

**Features:**
- List of published posts
- Pagination (10 per page)
- Tag filtering
- Search functionality
- Reading time display

**Data:** `useBlog()` composable

---

#### `src/views/blog/BlogPost.vue`

Single blog post view.

**Features:**
- Markdown rendering (markdown-it)
- XSS sanitization (DOMPurify)
- Video support (auto-detects .mp4/.webm/.ogg)
- Table of contents (h2/h3 headings)
- Reading time
- Tags
- Share buttons

**Data:** `getPostBySlug()` from `useBlog()`

**Custom renderer:**
```javascript
md.renderer.rules.image = (tokens, idx) => {
  const src = token.attrGet('src')
  if (/\.(mp4|webm|ogg|mov)$/i.test(src)) {
    return `<video controls>...</video>`
  }
  return defaultImageRenderer(...)
}
```

Converts `![text](video.mp4)` to `<video>` tags.

---

#### `src/views/albums/AlbumView.vue`

Photo album viewer.

**Features:**
- Photo grid
- Lightbox (click to enlarge)
- Category filtering
- Photo metadata (caption, location, date)

**Data:** `useAlbums()` composable

---

#### `src/views/admin/AdminPanel.vue`

Admin dashboard.

**Features:**
- List all posts (published + drafts)
- Status filter (all/published/draft)
- Create/edit/delete actions
- Quick publish/unpublish toggle
- Authentication required (Bearer token)

**Data:** `useAdminBlog()` composable

---

#### `src/views/admin/PostEditor.vue`

Blog post create/edit form.

**Features:**
- Markdown editor with live preview
- Toolbar (bold, italic, heading, link, image, code)
- Split view / editor only / preview only
- Draft/publish toggle
- Slug auto-generation from title
- Tag input
- Form validation

**Components used:**
- `MarkdownEditor.vue`
- `AdminAuthModal.vue`

---

### Components

#### `src/components/Navbar.vue`

Top navigation bar.

**Features:**
- Logo/name (links to home)
- Navigation links (Experience, Projects, etc.)
- Theme toggle (dark mode)
- Mobile menu (hamburger on small screens)
- Active route highlighting

---

#### `src/components/ChatAssistant.vue`

AI chatbot interface.

**Features:**
- Toggle button (bottom right, fixed position)
- Chat window with message history
- Input field
- Streaming responses (SSE)
- Loading indicators
- Error handling
- Message persistence (localStorage)

**Data:** `useChatAssistant()` composable

**Message types:**
- User messages
- Assistant messages (streamed character-by-character)
- System messages (errors, rate limits)

---

#### `src/components/CommandPalette.vue`

Quick navigation (Cmd/Ctrl+K).

**Features:**
- Search all pages, blog posts, projects
- Keyboard navigation (arrow keys, enter)
- Fuzzy search
- Recent searches

**Triggered by:**
- Keyboard: Cmd/Ctrl+K
- Button: Navbar search icon

---

#### `src/components/MarkdownEditor.vue`

Markdown editor with live preview.

**Features:**
- Toolbar: bold, italic, heading, link, image, code, list, quote
- View modes: split, editor only, preview only
- Live preview (markdown-it)
- Video support (same renderer as BlogPost.vue)
- Syntax highlighting in preview
- Textarea with tab support

**Used in:** PostEditor.vue

---

#### `src/components/AdminAuthModal.vue`

Admin login modal.

**Features:**
- Password input
- Submit button
- Error display
- Loading state
- Closes on successful login

**Authentication:** Stores token in localStorage as `admin_token`

---

#### `src/components/TableOfContents.vue`

Dynamic table of contents for blog posts.

**Features:**
- Extracts h2/h3 headings from markdown
- Smooth scroll to section on click
- Active section highlighting

**Props:** `headings` array from BlogPost.vue

---

#### `src/components/DeleteConfirmModal.vue`

Confirmation dialog for delete actions.

**Features:**
- Warning message
- Confirm/cancel buttons
- Prevents accidental deletes

**Used in:** AdminPanel.vue

---

### Composables

#### `src/composables/useBlog.js`

Blog operations (public).

**Exports:**
- `posts` (ref) - Array of posts
- `loading` (ref) - Loading state
- `error` (ref) - Error message
- `fetchPosts(options)` - Get published posts
- `getPostBySlug(slug)` - Get single post
- `searchPosts(query)` - Search posts by query

**API calls:**
- `GET /blog/posts` - List posts
- `GET /blog/posts/:slug` - Single post
- `GET /blog/search?q=query` - Search

**Error handling:** Returns empty array on error, logs to console

---

#### `src/composables/useAdminBlog.js`

Blog operations (admin).

**Exports:**
- `posts` (ref) - All posts (including drafts)
- `loading` (ref)
- `error` (ref)
- `fetchAdminPosts(options)` - Get all posts
- `getAdminPost(slug)` - Get post (any status)
- `createPost(postData)` - Create new post
- `updatePost(slug, postData)` - Update post
- `deletePost(slug)` - Delete post

**Authentication:** Uses `getAuthFetchOptions()` from `useAdminAuth()`

**API calls:**
- `GET /admin/blog/posts` - All posts
- `GET /admin/blog/posts/:slug` - Single post
- `POST /admin/blog/posts` - Create
- `PUT /admin/blog/posts/:slug` - Update
- `DELETE /admin/blog/posts/:slug` - Delete

---

#### `src/composables/useAdminAuth.js`

Authentication management.

**Exports:**
- `isAuthenticated` (ref) - Auth state
- `isLoading` (ref)
- `authError` (ref)
- `login(key)` - Login with admin key
- `logout()` - Clear token
- `checkAuthStatus()` - Check if authenticated
- `getAuthHeaders()` - Get headers with Bearer token
- `getAuthFetchOptions(method, body)` - Get fetch options

**Storage:** localStorage key `admin_token`

**Login flow:**
1. User enters admin key
2. POST /auth/login with Bearer header
3. If 200, store key in localStorage
4. Set `isAuthenticated = true`

**Logout flow:**
1. Remove token from localStorage
2. Set `isAuthenticated = false`

---

#### `src/composables/useAlbums.js`

Album and photo operations.

**Exports:**
- `albums` (ref)
- `currentAlbum` (ref)
- `loading` (ref)
- `error` (ref)
- `fetchAlbums()` - Get all albums
- `getAlbum(slug)` - Get album with photos
- `uploadPhoto(albumSlug, file)` - Upload photo (admin)
- `updatePhoto(photoId, data)` - Update metadata (admin)
- `deletePhoto(photoId)` - Delete photo (admin)

**Direct Supabase access:** Uses Supabase client for photos (not through Flask API)

---

#### `src/composables/useChatAssistant.js`

AI chatbot logic (828 lines).

**Exports:**
- `isOpen` (ref) - Chat window open/closed
- `messages` (ref) - Chat history
- `isLoading` (ref)
- `toggleChat()` - Open/close chat
- `sendMessage(content)` - Send message to API
- `preloadContext()` - Load blog posts/projects for context

**Message storage:** localStorage key `chat_messages`

**Streaming:**
- Uses SSE (Server-Sent Events)
- Streams responses character-by-character
- Handles connection errors
- Rate limiting (10 requests/min)

**Context:**
- Professional info (experience, projects, skills)
- Blog posts (titles, excerpts)
- Current page

---

#### `src/composables/useProfessionalInfo.js`

Loads professional data.

**Source:** `frontend/public/data/professionalInfo.json`

**Exports:**
- `experience` (ref)
- `projects` (ref)
- `skills` (ref)
- `about` (ref)
- `loadProfessionalInfo()` - Fetch JSON file

**Format:**
```json
{
  "experience": [...],
  "projects": [...],
  "skills": [...],
  "about": { ... }
}
```

---

#### `src/composables/useTheme.js`

Theme management (dark mode).

**Exports:**
- `theme` (ref) - 'light' or 'dark'
- `toggleTheme()` - Switch theme

**Storage:** localStorage key `theme`

**Implementation:** Adds/removes `dark` class on `<html>` element

---

#### `src/composables/useSearch.js`

Global search functionality.

**Exports:**
- `searchQuery` (ref)
- `searchResults` (ref) - Pages, posts, projects
- `isLoading` (ref)
- `search(query)` - Search all content
- `clearSearch()` - Clear results

**Searches:**
- Pages (hardcoded list)
- Blog posts (API)
- Projects (professionalInfo.json)

---

#### `src/composables/useSanitizer.js`

HTML sanitization (XSS protection).

**Exports:**
- `sanitizeHtml(html, config)` - Sanitize HTML string

**Uses:** DOMPurify

**Default config:**
- Allowed tags: h1-h6, p, br, hr, strong, em, a, img, video, source, ul, ol, li, blockquote, code, pre, table, div, span
- Allowed attributes: href, src, alt, title, class, id, controls, autoplay, loop, muted, type, style
- Blocks: script, iframe, object, embed

**Used in:**
- BlogPost.vue (sanitize markdown output)
- ChatAssistant.vue (sanitize AI responses)

---

#### `src/composables/useAsyncRequest.js`

Generic async request handler.

**Exports:**
- `loading` (ref)
- `error` (ref)
- `execute(asyncFn)` - Execute async function with loading/error handling

**Used by:** useBlog, useAlbums, etc.

---

### Config

#### `src/config/api.js`

API endpoint configuration.

**Base URL:** `import.meta.env.VITE_API_URL`

**Endpoints:**
```javascript
// Auth
authLogin: '/auth/login'
authLogout: '/auth/logout'

// Blog (public)
blogPosts: '/blog/posts'
blogPost: (slug) => `/blog/posts/${slug}`
blogSearch: '/blog/search'

// Admin blog
adminPosts: '/admin/blog/posts'
adminPost: (slug) => `/admin/blog/posts/${slug}`

// Albums
albums: '/albums'
album: (slug) => `/albums/${slug}`

// Chat
chat: '/chat'
chatStream: '/chat/stream'
```

---

#### `src/config/contact.js`

Contact information.

**Exports:**
```javascript
export const CONTACT = {
  email: 'richwell.perez@gmail.com',
  linkedin: 'https://linkedin.com/in/richwell-perez',
  github: 'https://github.com/richwellp'
}
```

Used in: Contact.vue, ChatAssistant.vue, Navbar.vue

---

### Public Data

#### `frontend/public/data/professionalInfo.json`

Professional content (not in database).

**Structure:**
```json
{
  "about": {
    "name": "Richwell Perez",
    "title": "Software Engineer",
    "bio": "...",
    "location": "San Francisco, CA"
  },
  "experience": [
    {
      "company": "Company Name",
      "title": "Role",
      "location": "City, State",
      "dates": "Jan 2024 - Present",
      "current": true,
      "description": "...",
      "highlights": ["...", "..."],
      "technologies": ["Python", "React"]
    }
  ],
  "projects": [
    {
      "title": "Project Name",
      "description": "...",
      "technologies": ["Vue", "Flask"],
      "links": {
        "github": "https://...",
        "demo": "https://..."
      },
      "featured": true
    }
  ],
  "skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["Vue", "Flask"],
    "Tools": ["Git", "Docker"]
  }
}
```

**Editing:** Directly edit file, commit, push

---

## Backend Files

### Root Configuration

**`requirements.txt`**
Dependencies: Flask, Flask-CORS, supabase, google-generativeai, pytest

**`app.py`**
Flask app entry point (for local dev).
Production uses `api/index.py` (Vercel serverless).

**`vercel.json`**
Vercel deployment configuration.
Routes all requests to `api/index.py`.

---

### API

#### `api/index.py`

Main Flask app.

**Setup:**
- CORS configuration (allowed origins)
- Gzip compression
- Blueprint registration (blog, albums, auth, sitemap)
- Rate limiting (in-memory, per IP)

**Endpoints:**
- `GET /` - Health check
- `POST /chat` - AI chatbot (non-streaming, deprecated)
- `POST /chat/stream` - AI chatbot (SSE streaming)

**Rate limiting:**
- 10 requests per 60 seconds per IP
- Returns 429 Too Many Requests if exceeded

---

#### `api/blog.py`

Public blog endpoints.

**Endpoints:**

`GET /blog/posts`
- List published posts
- Pagination: `?page=1&per_page=10`
- Tag filter: `?tag=python`
- Returns: `{ posts: [...], page, per_page }`

`GET /blog/posts/:slug`
- Get single published post
- Calculates reading time
- Extracts headings (h2, h3)
- Returns: `{ slug, title, content, ... }`

`GET /blog/search?q=query`
- Search published posts
- Searches: title, content, excerpt, tags
- Returns: `{ posts: [...], total }`

**Functions:**
- `calculate_reading_time(content)` - Words / 200 WPM
- `extract_headings(content)` - Regex for ## and ###

---

#### `api/admin_blog.py`

Admin blog endpoints (authentication required).

**All routes use `@require_admin` decorator.**

**Endpoints:**

`GET /admin/blog/posts`
- List ALL posts (including drafts)
- Status filter: `?status=draft` or `?status=published`
- Pagination: `?page=1&per_page=10`

`GET /admin/blog/posts/:slug`
- Get single post (any status)

`POST /admin/blog/posts`
- Create new post
- Body: `{ slug, title, content, excerpt, tags, published }`
- Auto-generates published_at if published=true

`PUT /admin/blog/posts/:slug`
- Update post
- Body: Any fields to update
- Updates updated_at timestamp

`DELETE /admin/blog/posts/:slug`
- Delete post
- Returns 204 No Content

---

#### `api/albums.py`

Albums and photos endpoints.

**Public endpoints:**

`GET /albums`
- List all published albums
- Returns: `{ albums: [...] }`

`GET /albums/:slug`
- Get album with photos
- Sorted by order_index
- Returns: `{ album, photos: [...] }`

**Admin endpoints (require auth):**

`GET /admin/albums`
- List all albums (including unpublished)

`POST /admin/albums/:slug/photos`
- Add photo to album
- Body: `{ url, caption, location, date_taken, category }`

`PUT /admin/photos/:id`
- Update photo metadata
- Body: Any fields to update

`DELETE /admin/photos/:id`
- Delete photo

---

#### `api/auth.py`

Authentication endpoints.

**Endpoints:**

`POST /auth/login`
- Verify admin key
- Body: `{ key: "admin_password" }`
- Returns 200 if valid (frontend stores in localStorage)
- Returns 401 if invalid

`POST /auth/logout`
- No-op (frontend clears localStorage)
- Returns 200

`GET /auth/status`
- Check authentication status
- Checks Authorization: Bearer header
- Returns: `{ authenticated: true/false, method: 'bearer' }`

`GET /auth/verify`
- Protected endpoint to verify auth
- Requires valid Bearer token
- Returns 200 if authenticated, 401 if not

---

#### `api/gemini.py`

AI chatbot (Google Gemini).

**Functions:**

`call_gemini(message, history, site_context)`
- Non-streaming (deprecated)
- Returns: Full response text

`call_gemini_stream(message, history, site_context)`
- Streaming with yield
- Generator function
- Yields: `{ text: "chunk" }` or `{ done: True }`

**Context:**
- Professional info (experience, projects, skills)
- Blog posts (if provided)
- Current page
- System prompt: "You are Richwell's virtual assistant..."

**Rate limiting:** 10 requests per minute (enforced in index.py)

**Error handling:**
- Network errors
- API errors
- Timeout errors
- Returns error objects instead of raising

---

#### `api/sitemap.py`

Dynamic sitemap generation.

**Endpoint:**

`GET /sitemap.xml`
- Generates XML sitemap
- Includes: Static pages, blog posts, albums
- Updates `<lastmod>` based on updated_at

**XML format:**
```xml
<urlset>
  <url>
    <loc>https://richwellp.github.io/</loc>
    <lastmod>2024-01-01</lastmod>
    <priority>1.0</priority>
  </url>
  ...
</urlset>
```

---

### Utilities

#### `auth.py`

Authentication utilities.

**Constants:**
- `ADMIN_KEY` - From env var `BLOG_ADMIN_KEY`

**Functions:**

`require_admin(f)` - Decorator
- Checks Authorization: Bearer header
- Validates token with timing-safe comparison
- Returns 401 if invalid

`verify_admin_key(key)` - Helper
- Timing-safe comparison: `secrets.compare_digest()`
- Prevents timing attacks

`get_auth_status()` - Helper
- Checks current request authentication
- Returns: `{ authenticated, method }`

---

#### `config.py`

Configuration constants.

**Exports:**
```python
DEFAULT_PAGE_SIZE = 10
WORDS_PER_MINUTE = 200
DEFAULT_READING_TIME_ESTIMATE = 5
MESSAGE_LENGTH_LIMIT = 1000
HISTORY_LIMIT = 20
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60  # seconds
```

---

### Tests

#### `tests/test_blog.py`

Blog API tests (pytest).

**Tests:**
- List posts (pagination, filtering)
- Get single post (published only)
- Search posts
- Admin endpoints (require auth)
- Create post (validation)
- Update post
- Delete post
- Reading time calculation
- Heading extraction

**Fixtures:**
- `client` - Flask test client
- `mock_supabase` - Mocked Supabase responses

---

#### `tests/test_albums.py`

Albums API tests.

**Tests:**
- List albums
- Get album with photos
- Admin photo upload
- Photo metadata update
- Photo deletion

---

#### `tests/test_auth.py`

Authentication tests.

**Tests:**
- Login with valid key
- Login with invalid key
- Protected endpoints (401 without auth)
- Timing-safe comparison

---

#### Frontend Tests

**Location:** `frontend/tests/unit/`

**Test files:**
- `composables/useBlog.test.js` - Blog operations
- `composables/useAdminBlog.test.js` - Admin blog operations
- `composables/useAdminAuth.test.js` - Authentication
- `composables/useAlbums.test.js` - Albums operations
- `components/ChatAssistant.test.js` - Chatbot component

**Test framework:** Vitest + @vue/test-utils

**Mocking:**
- `vi.spyOn(global, 'fetch')` - Mock API calls
- `vi.mock('@supabase/supabase-js')` - Mock Supabase

---

## Database Schema

### blog_posts

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `slug` (TEXT UNIQUE NOT NULL) - URL-friendly identifier
- `title` (TEXT NOT NULL)
- `content` (TEXT NOT NULL) - Markdown
- `excerpt` (TEXT) - Short summary
- `author` (TEXT DEFAULT 'Richwell Perez')
- `tags` (TEXT[] DEFAULT '{}') - Array of tags
- `published` (BOOLEAN DEFAULT FALSE)
- `published_at` (TIMESTAMP WITH TIME ZONE)
- `reading_time` (INTEGER) - Minutes
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- `idx_blog_posts_slug` ON (slug)
- `idx_blog_posts_published` ON (published)
- `idx_blog_posts_created_at` ON (created_at)

**Triggers:**
- `update_updated_at` - Auto-update updated_at on row change

---

### albums

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `slug` (TEXT UNIQUE NOT NULL)
- `name` (TEXT NOT NULL)
- `icon` (TEXT) - Emoji or icon class
- `subtitle` (TEXT)
- `categories` (TEXT[] DEFAULT '{}')
- `order_index` (INTEGER DEFAULT 0)
- `published` (BOOLEAN DEFAULT TRUE)
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- `idx_albums_slug` ON (slug)
- `idx_albums_published` ON (published)
- `idx_albums_order` ON (order_index)

---

### photos

**Columns:**
- `id` (BIGSERIAL PRIMARY KEY)
- `album_id` (BIGINT REFERENCES albums(id) ON DELETE CASCADE)
- `url` (TEXT NOT NULL) - Supabase Storage URL
- `caption` (TEXT)
- `location` (TEXT)
- `date_taken` (DATE)
- `category` (TEXT)
- `order_index` (INTEGER DEFAULT 0)
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- `idx_photos_album` ON (album_id)
- `idx_photos_order` ON (order_index)

**Foreign key:** album_id → albums(id) (CASCADE on delete)

---

## Environment Variables

### Backend

**Required:**
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Service role key (bypasses RLS)
- `BLOG_ADMIN_KEY` - Admin password
- `GEMINI_API_KEY` - Google Gemini API key

**Optional:**
- `ALLOWED_ORIGINS` - CORS origins (comma-separated)
- `FLASK_ENV` - 'development' or 'production'

### Frontend

**Required:**
- `VITE_API_URL` - Backend API URL
- `VITE_SUPABASE_URL` - Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Supabase anon key (public)

**Access in code:**
```javascript
import.meta.env.VITE_API_URL
```

---

## CI/CD

### `.github/workflows/ci.yml`

GitHub Actions workflow.

**Triggers:**
- Push to main
- Pull request to main

**Jobs:**

1. **backend-tests**
   - Set up Python 3.11
   - Install dependencies
   - Run pytest with coverage
   - Fail if tests fail

2. **frontend-tests**
   - Set up Node.js 20
   - Install dependencies
   - Run vitest in CI mode
   - Fail if tests fail

3. **frontend-build**
   - Depends on frontend-tests
   - Build production bundle
   - Verify dist/ folder created

**Status:** Check at https://github.com/richwellp/richwellp.github.io/actions

---

## Deployment

### Frontend (GitHub Pages)

**Process:**
1. Push to main
2. GitHub Actions builds frontend
3. Deploys dist/ to gh-pages branch
4. Live at https://richwellp.github.io

**Build command:** `npm run build`
**Output:** `frontend/dist/`

### Backend (Vercel)

**Process:**
1. Push to main
2. Vercel auto-deploys
3. Serverless functions
4. Live at https://richwellp-github-io.vercel.app

**Entry point:** `api/index.py`
**Environment:** Managed in Vercel dashboard

---

## File Size Reference

**Frontend:**
- Total: ~500 files (~50,000 lines including node_modules)
- Source: ~80 files (~8,000 lines)
- Largest: useChatAssistant.js (828 lines)

**Backend:**
- Total: ~20 files (~2,000 lines)
- Source: ~10 files (~1,500 lines)
- Tests: ~10 files (~500 lines)

**Documentation:**
- README.md (80 lines)
- docs/GUIDE.md (400 lines)
- docs/TECHNICAL_REFERENCE.md (this file)

---

## Common Patterns

### API Call Pattern

```javascript
// In composable
const { loading, error, execute } = useAsyncRequest()

const fetchData = async () => {
  await execute(async () => {
    const response = await fetch(API_ENDPOINTS.something)
    if (!response.ok) throw new Error('Failed')
    const data = await response.json()
    return data
  }).catch(() => {
    // Error handled by useAsyncRequest
  })
}
```

### Admin API Call Pattern

```javascript
// With authentication
const { getAuthFetchOptions } = useAdminAuth()

const response = await fetch(
  API_ENDPOINTS.adminPost(slug),
  getAuthFetchOptions('PUT', { title: 'New Title' })
)
```

### Component Pattern

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { useComposable } from '@/composables/useComposable'

const { data, loading, fetchData } = useComposable()

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else>{{ data }}</div>
</template>

<style scoped>
/* Component-specific styles */
</style>
```

---

## Key Algorithms

### Reading Time Calculation

```python
def calculate_reading_time(content):
    words = len(re.findall(r'\w+', content))
    return max(1, round(words / 200))  # 200 WPM
```

### Heading Extraction

```python
def extract_headings(content):
    headings = []
    for match in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2)
        id = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
        headings.append({'level': level, 'text': text, 'id': id})
    return headings
```

### Video Detection in Markdown

```javascript
if (/\.(mp4|webm|ogg|mov)$/i.test(src)) {
  return `<video controls>
    <source src="${src}" type="video/${ext}">
  </video>`
}
```

---

## Security Implementation

**Authentication:**
- Timing-safe comparison: `secrets.compare_digest()`
- Bearer token in Authorization header
- Token stored in localStorage (client)

**XSS Prevention:**
- DOMPurify sanitization on all user content
- Markdown `html: false` (no raw HTML)
- CSP headers (via meta tag)

**CORS:**
- Explicit allowed origins
- Credentials support for cross-origin

**Rate Limiting:**
- 10 requests per 60 seconds per IP
- In-memory storage (resets on restart)

**SQL Injection:**
- Supabase client uses parameterized queries
- No raw SQL in application code

---

This reference covers every important file and pattern in your codebase.
