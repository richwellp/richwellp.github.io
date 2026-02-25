# Developer Guide

Complete reference for portfolio development and maintenance.

---

## Quick Commands

```bash
# Development
cd backend && flask run                     # http://localhost:5000
cd frontend && npm run dev                  # http://localhost:5173

# Testing
cd backend && python -m pytest -v           # 50 tests
cd frontend && npm test -- --run            # 47 tests

# Deploy
git push origin main                        # Auto-deploys
```

---

## Tech Stack

**Frontend:** Vue 3, Vite, Vue Router, markdown-it, DOMPurify
**Backend:** Flask, Google Gemini AI
**Database:** Supabase (PostgreSQL + Storage)
**Deploy:** GitHub Pages (frontend), Vercel (backend)
**Tests:** Vitest (47) + pytest (50)

---

## Architecture

```
User Browser (Vue 3 SPA)
    ↓
GitHub Pages (Static HTML/CSS/JS)
    ↓
Flask Backend (Vercel Serverless)
    ↓
Supabase PostgreSQL (Database)
    +
Supabase Storage (Photos/Videos)
    +
Google Gemini AI (Chatbot)
```

---

## Authentication

Admin authentication uses **Bearer tokens** stored in localStorage.

**How it works:**
1. User enters password at `/admin`
2. Frontend stores admin key in localStorage as `admin_token`
3. Every admin request includes `Authorization: Bearer <key>` header
4. Backend validates with `@require_admin` decorator using timing-safe comparison

**Security:**
- Timing-safe comparison (`secrets.compare_digest()` prevents timing attacks)
- No session management (stateless)
- Works cross-origin (no third-party cookie issues)
- Public content sanitized with DOMPurify

**Environment variable:**
Set `BLOG_ADMIN_KEY` in Vercel dashboard → Settings → Environment Variables

**Troubleshooting:**
- Login fails → Check `BLOG_ADMIN_KEY` matches your password
- Token not working → Clear localStorage: `localStorage.clear()` in console
- Still 401 → Verify admin key in Vercel is correct

**Code locations:**
- Backend: `backend/auth.py`
- Frontend: `frontend/src/composables/useAdminAuth.js`
- Component: `frontend/src/components/AdminAuthModal.vue`

---

## Adding Media to Blog Posts

Use image syntax for both images AND videos. The markdown renderer auto-detects video files.

### Images

```markdown
![Alt text](https://your-url.com/image.jpg)
```

### Videos

```markdown
![Watch: My Video](https://your-url.com/video.mp4)
```

The renderer detects `.mp4`, `.webm`, `.ogg`, `.mov` and converts to `<video>` tags automatically.

### Upload to Supabase Storage

**Step 1: Create bucket (if not exists)**
1. Go to https://app.supabase.com
2. Select project → Storage
3. Create bucket: `blog-media` (public)

**Step 2: Upload media**
1. Click bucket → Upload file
2. Copy URL after upload

**Step 3: Use in blog post**
```markdown
![Description](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/file.jpg)
```

### Best Practices

**Images:**
- Resize to max 1920px wide
- Compress (TinyPNG for PNG, JPEG Optimizer for JPG)
- Target < 500KB per image
- Use descriptive alt text for accessibility

**Videos:**
- Short clips (< 30s): Upload to Supabase as MP4, keep < 10MB
- Long videos: Use YouTube/Vimeo, link in post
- Always include alt text

---

## Project Structure

```
richwellp.github.io/
├── frontend/
│   ├── public/
│   │   ├── data/professionalInfo.json  # Experience, projects, skills
│   │   └── assets/Resume.pdf            # Your resume
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── composables/    # Business logic (useBlog, useAlbums, etc.)
│   │   ├── views/          # Page components
│   │   ├── config/
│   │   │   ├── api.js      # API endpoints
│   │   │   └── contact.js  # Contact info
│   │   └── router/         # Route definitions
│   └── tests/              # Vitest tests
│
├── backend/
│   ├── api/
│   │   ├── blog.py         # Blog CRUD endpoints
│   │   ├── admin_blog.py   # Admin blog endpoints
│   │   ├── albums.py       # Albums/Photos endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── gemini.py       # AI chatbot (SSE streaming)
│   │   └── sitemap.py      # Dynamic sitemap
│   ├── auth.py             # Authentication utilities
│   ├── config.py           # Configuration
│   └── tests/              # pytest tests
│
└── .github/workflows/      # CI/CD pipeline
```

---

## API Endpoints

### Public (No Auth)

```
GET  /blog/posts              # List published posts
GET  /blog/posts/:slug        # Get single post
GET  /blog/search?q=query     # Search posts
GET  /albums                  # List albums
GET  /albums/:slug            # Get album with photos
GET  /sitemap.xml             # Dynamic sitemap
POST /chat/stream             # AI chatbot (SSE)
```

### Admin (Bearer Token Required)

```
POST   /auth/login            # Verify admin key
POST   /auth/logout           # No-op (frontend clears localStorage)
GET    /auth/status           # Check auth status
GET    /auth/verify           # Verify authenticated

GET    /admin/blog/posts      # All posts (including drafts)
GET    /admin/blog/posts/:slug
POST   /admin/blog/posts      # Create post
PUT    /admin/blog/posts/:slug
DELETE /admin/blog/posts/:slug

GET    /admin/albums
POST   /admin/albums/:slug/photos
PUT    /admin/photos/:id
DELETE /admin/photos/:id
```

---

## Database Schema

### blog_posts

```sql
id              BIGSERIAL PRIMARY KEY
slug            TEXT UNIQUE NOT NULL
title           TEXT NOT NULL
content         TEXT NOT NULL
excerpt         TEXT
author          TEXT DEFAULT 'Richwell Perez'
tags            TEXT[] DEFAULT '{}'
published       BOOLEAN DEFAULT FALSE
published_at    TIMESTAMP WITH TIME ZONE
reading_time    INTEGER
created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()

INDEX idx_blog_posts_slug
INDEX idx_blog_posts_published
INDEX idx_blog_posts_created_at
```

### albums

```sql
id              BIGSERIAL PRIMARY KEY
slug            TEXT UNIQUE NOT NULL
name            TEXT NOT NULL
icon            TEXT
subtitle        TEXT
categories      TEXT[] DEFAULT '{}'
order_index     INTEGER DEFAULT 0
published       BOOLEAN DEFAULT TRUE
created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()

INDEX idx_albums_slug
INDEX idx_albums_published
INDEX idx_albums_order
```

### photos

```sql
id              BIGSERIAL PRIMARY KEY
album_id        BIGINT REFERENCES albums(id) ON DELETE CASCADE
url             TEXT NOT NULL
caption         TEXT
location        TEXT
date_taken      DATE
category        TEXT
order_index     INTEGER DEFAULT 0
created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()

INDEX idx_photos_album
INDEX idx_photos_order
```

---

## Environment Variables

### Backend (Vercel)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
BLOG_ADMIN_KEY=your_admin_password
GEMINI_API_KEY=your_gemini_key
ALLOWED_ORIGINS=https://richwellp.github.io
```

### Frontend (Vercel)

```env
VITE_API_URL=https://your-backend.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

Set in Vercel dashboard → Settings → Environment Variables

---

## Key Files

### Frontend

**Components:**
- `ChatAssistant.vue` - AI chatbot UI
- `CommandPalette.vue` - Cmd/Ctrl+K quick nav
- `MarkdownEditor.vue` - Markdown editor with preview
- `AdminAuthModal.vue` - Login modal

**Composables:**
- `useBlog.js` - Blog CRUD operations
- `useAdminBlog.js` - Admin blog operations
- `useAlbums.js` - Albums/photos operations
- `useChatAssistant.js` - Chatbot logic (828 lines)
- `useAdminAuth.js` - Authentication

**Views:**
- `Home.vue` - Landing page
- `Experience.vue` - Work experience
- `Projects.vue` - Project showcase
- `blog/BlogList.vue` - Blog listing
- `blog/BlogPost.vue` - Single post
- `admin/AdminPanel.vue` - Admin dashboard
- `admin/PostEditor.vue` - Post create/edit

### Backend

**API:**
- `blog.py` - Public blog endpoints
- `admin_blog.py` - Admin blog endpoints
- `albums.py` - Albums/photos endpoints
- `auth.py` - Authentication endpoints
- `gemini.py` - AI chatbot (SSE streaming)

**Utilities:**
- `auth.py` - Auth decorator and helpers
- `config.py` - Configuration constants

---

## Development Workflow

### Adding Content

**Professional Info (Experience, Projects, Skills):**
Edit `frontend/public/data/professionalInfo.json`, commit, push

**Blog Posts:**
Use admin panel at `/admin` - markdown editor included

**Photos:**
Use admin panel at `/admin/albums` - upload interface included

**Resume:**
Replace `frontend/public/assets/Resume.pdf`, commit, push

**Contact Info:**
Edit `frontend/src/config/contact.js`, commit, push

### Testing

```bash
# Backend (50 tests)
cd backend
python -m pytest -v                        # All tests
python -m pytest tests/test_blog.py -v     # Specific file
python -m pytest -k "test_name"            # Specific test

# Frontend (47+ tests)
cd frontend
npm test                                   # Watch mode
npm test -- --run                          # Run once
npm test tests/unit/composables/useBlog.test.js  # Specific file
```

### Deployment

```bash
git push origin main
```

GitHub Actions automatically:
1. Runs backend tests (pytest)
2. Runs frontend tests (vitest)
3. Builds frontend
4. Deploys to GitHub Pages
5. Vercel auto-deploys backend

Check status: https://github.com/richwellp/richwellp.github.io/actions

---

## Troubleshooting

### Tests Failing

```bash
# Check what changed
git status && git diff

# Reinstall dependencies
cd frontend && rm -rf node_modules package-lock.json && npm install
cd backend && pip install -r requirements.txt --force-reinstall

# Rerun tests
cd backend && python -m pytest -v
cd frontend && npm test -- --run
```

### Content Not Updating

- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Validate JSON: `cat file.json | python -m json.tool`
- Check browser console (F12) for errors

### Chatbot Not Working

- Check Vercel environment variables for `GEMINI_API_KEY`
- Check browser console for errors
- Check Network tab for API responses

### Deployment Failed

- Check GitHub Actions: https://github.com/richwellp/richwellp.github.io/actions
- Look for ❌ to see what failed
- Common issues: test failures, environment variables missing

### API Errors

- Open DevTools (F12) → Network tab
- Refresh page
- Find failing request
- Check Status code and Response
- Verify environment variables in Vercel

---

## Security

**Authentication:**
- Bearer token with timing-safe comparison
- No session management (stateless)
- Solo admin model (no user registration)

**XSS Protection:**
- All public content sanitized with DOMPurify
- Markdown HTML disabled (`html: false`)
- Video tags allowed but sanitized

**CORS:**
- Configured origins: localhost + production domains
- Credentials supported for cross-origin

**Database:**
- Row Level Security (RLS) on Supabase
- Service role key for backend (bypasses RLS)
- Anon key for frontend (read-only public data)

---

## CI/CD Pipeline

**GitHub Actions workflow:** `.github/workflows/ci.yml`

On push or PR to main:
1. **Backend tests** - pytest with coverage
2. **Frontend tests** - vitest in CI mode
3. **Frontend build** - Production build with env vars
4. **Deploy** - Auto-deploy to GitHub Pages

**Vercel:**
- Backend auto-deploys on push to main
- Environment variables managed in Vercel dashboard
- Serverless functions with auto-scaling

---

## Emergency Rollback

```bash
# See recent commits
git log --oneline -10

# Rollback to working commit (e.g., abc123)
git reset --hard abc123
git push origin main --force
```

⚠️ **Warning:** Permanently removes later commits. Emergency use only.

---

## Contact

**Richwell Perez**
Email: richwell.perez@gmail.com
LinkedIn: [richwell-perez](https://linkedin.com/in/richwell-perez)
GitHub: [richwellp](https://github.com/richwellp)
