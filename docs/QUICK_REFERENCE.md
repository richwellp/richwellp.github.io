# Quick Reference

Essential commands and info.

## 🚀 Development Commands

### Frontend
```bash
cd frontend
npm run dev          # Start dev server → http://localhost:5173
npm run build        # Build for production → dist/
npm test             # Run tests in watch mode
npm test -- --run    # Run tests once
```

### Backend
```bash
cd backend
flask run            # Start dev server → http://localhost:5000
python -m pytest -v  # Run all tests
python -m pytest -k "test_name"  # Run specific test
```

---

## 📁 Key File Locations

### Frontend
```
frontend/src/
├── views/                      # Page components (Home, Experience, etc.)
├── components/                 # Reusable UI components
├── composables/                # Business logic (useBlog, useAlbums, etc.)
├── config/                     # Configuration (API, constants, contact)
├── router/index.js             # Route definitions
└── App.vue                     # Root component with layout

frontend/public/
├── data/professionalInfo.json  # Experience, projects, skills
└── assets/Resume.pdf           # Your resume
```

### Backend
```
backend/
├── api/
│   ├── blog.py                 # Blog CRUD endpoints
│   ├── albums.py               # Albums/Photos CRUD endpoints
│   ├── gemini.py               # AI chatbot (SSE streaming)
│   └── sitemap.py              # Dynamic sitemap
├── tests/                      # pytest tests
├── database/                   # SQL schema files
├── app.py                      # Flask entry point
├── auth.py                     # Admin authentication
└── config.py                   # Configuration
```

---

## 🔗 API Endpoints

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

### Admin (Requires Bearer Token)
```
POST   /auth/login            # Verify admin key → frontend stores in localStorage
GET    /blog/admin/posts      # All posts (including drafts)
POST   /blog/posts            # Create post
PUT    /blog/posts/:slug      # Update post
DELETE /blog/posts/:slug      # Delete post
POST   /admin/upload          # Upload photo to storage
POST   /admin/albums/:slug/photos  # Add photo to album
PUT    /admin/photos/:id      # Update photo metadata
DELETE /admin/photos/:id      # Delete photo
```

---

## 🗄️ Database Tables

### blog_posts
```sql
id, slug, title, content, excerpt, author, tags[],
published, published_at, reading_time, created_at, updated_at
```

### albums
```sql
id, slug, name, icon, subtitle, categories[],
order_index, published, created_at, updated_at
```

### photos
```sql
id, album_id, url, caption, location, date_taken,
category, order_index, created_at, updated_at
```

---

## 🔐 Environment Variables

**Backend:**
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Service role key
- `BLOG_ADMIN_KEY` - Admin password
- `GEMINI_API_KEY` - Google Gemini key
- `ALLOWED_ORIGINS` - CORS origins

**Frontend:**
- `VITE_API_URL` - Backend URL
- `VITE_SUPABASE_URL` - Supabase URL
- `VITE_SUPABASE_ANON_KEY` - Public anon key

Set in Vercel dashboard → Settings → Environment Variables

---

## 🧪 Testing

### Run All Tests
```bash
# Backend (50 tests)
cd backend && python -m pytest -v

# Frontend (47+ tests)
cd frontend && npm test -- --run
```

### Run Specific Tests
```bash
# Backend
python -m pytest tests/test_blog.py
python -m pytest -k "test_create_post"

# Frontend
npm test tests/unit/composables/useBlog.test.js
```

---

## 🚢 Deployment

### Automatic Deployment
```bash
git push origin main
# → GitHub Actions runs tests
# → Builds frontend
# → Deploys to GitHub Pages
# → Vercel auto-deploys backend
```

### Manual Build
```bash
# Frontend
cd frontend
npm run build
# Output: dist/

# Backend (Vercel handles this)
# No manual build needed
```

---

## 🗂️ Common Tasks

**Blog Post:** `/admin` → New Post → Write → Publish
**Photos:** `/admin/albums` → Select album → Upload → Save
**Experience:** Edit `professionalInfo.json` → Push
**Resume:** Replace `Resume.pdf` → Push

---

## 🐛 Debug

**API:** `curl http://localhost:5000/` → Should return `{"message": "Hello from Flask..."}`
**Build:** `cd frontend && npm run build && npm run preview`
**Clean:** Delete `node_modules` or `.venv` → Reinstall

---

## 📊 Architecture at a Glance

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

## 🔑 Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| ChatAssistant.vue | AI chatbot UI | `frontend/src/components/` |
| useChatAssistant.js | Chatbot logic (828 lines) | `frontend/src/composables/` |
| gemini.py | AI API (SSE streaming) | `backend/api/` |
| blog.py | Blog CRUD API | `backend/api/` |
| albums.py | Albums/Photos API | `backend/api/` |
| auth.py | Admin authentication | `backend/` |
| router/index.js | Vue routing | `frontend/src/router/` |
| App.vue | Root layout | `frontend/src/` |

---

## 🎨 CSS Variables (Dark Theme)

```css
--bg-primary: #0f0f0f
--bg-secondary: #1a1a1a
--bg-card: #1f1f1f
--text-primary: #e6e6e6
--text-secondary: #b3b3b3
--accent-primary: #00d084
--accent-secondary: #00a36c
--border-color: #333333
```

---

## 🛠️ Tech Stack Summary

**Frontend:** Vue 3, Vite, Vue Router, markdown-it, DOMPurify, Vitest
**Backend:** Flask, Supabase (PostgreSQL), Google Gemini AI, pytest
**Hosting:** GitHub Pages (frontend), Vercel (backend)
**CI/CD:** GitHub Actions

---

## 📝 Common Git Commands

```bash
# Create feature branch
git checkout -b feature/new-feature

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Push and deploy
git push origin main

# Check deployment status
# → https://github.com/richwellp/richwellp.github.io/actions
```

---

## 🔗 Links

- **Live:** https://richwellp.github.io
- **API:** https://richwellp-github-io.vercel.app
- **GitHub:** https://github.com/richwellp/richwellp.github.io
- **Supabase:** https://app.supabase.com
- **Vercel:** https://vercel.com/dashboard

**Docs:** [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)
