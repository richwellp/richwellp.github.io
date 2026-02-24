# Richwell Perez - Portfolio Website

A modern, full-stack personal portfolio website built with Vue 3 and Flask, featuring a blog system, photo albums, and an interactive chatbot assistant.

**Live Site:** [richwellp.github.io](https://richwellp.github.io)

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io

# 2. Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export BLOG_ADMIN_KEY="your-secure-admin-key"
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export GEMINI_API_KEY="your-gemini-key"

# Run backend (Terminal 1)
flask run

# 3. Frontend setup (Terminal 2)
cd ../frontend
npm install

# Create .env.local
echo "VITE_API_URL=http://localhost:5000" > .env.local

# Run frontend
npm run dev

# Visit http://localhost:5173
```

---

## ✨ Features

- **Responsive Design** - Desktop, tablet, and mobile optimized
- **Dark/Light Theme** - Persistent theme switching with smooth transitions
- **Blog System** - Database-driven with markdown editor and admin panel
- **Photo & Video Albums** - Travel, professional, and sports galleries with lightbox
- **AI Chat Assistant** - Context-aware chatbot with streaming typewriter animation
- **Command Palette** - Quick navigation (Cmd/Ctrl + K)
- **PDF Resume Viewer** - Interactive embedded CV
- **SEO Optimized** - Structured data and meta tags
- **CI/CD Pipeline** - Automated testing and deployment

---

## 🛠️ Tech Stack

### Frontend
- **Vue 3** + Composition API
- **Vue Router 4** - Client-side routing
- **Vite 7** - Fast build tool with HMR
- **Markdown-it** - Blog post rendering
- **Vitest** - Unit testing (33 tests)

### Backend
- **Flask** - Python web framework
- **Supabase PostgreSQL** - Database for blog posts
- **Google Gemini API** - AI chatbot
- **pytest** - Testing framework (18 tests)

### Deployment
- **Frontend** → GitHub Pages (automated via GitHub Actions)
- **Backend** → Vercel (serverless functions)

---

## 📂 Project Structure

```
richwellp.github.io/
├── frontend/               # Vue 3 frontend application
│   ├── public/
│   │   ├── assets/
│   │   │   ├── photos/    # Album images and videos
│   │   │   └── icons/     # Favicons and app icons
│   │   └── robots.txt
│   ├── src/
│   │   ├── assets/        # CSS and fonts
│   │   ├── components/    # Vue components
│   │   │   ├── AdminAuthModal.vue
│   │   │   ├── AlbumViewer.vue
│   │   │   ├── ChatAssistant.vue
│   │   │   ├── CommandPalette.vue
│   │   │   ├── DeleteConfirmModal.vue
│   │   │   ├── Footer.vue
│   │   │   ├── Header.vue
│   │   │   ├── MarkdownEditor.vue
│   │   │   └── OptimizedImage.vue
│   │   ├── composables/   # Vue composables
│   │   │   ├── useAdminAuth.js
│   │   │   ├── useAdminBlog.js
│   │   │   ├── useBlog.js
│   │   │   ├── useChatAssistant.js
│   │   │   └── useStructuredData.js
│   │   ├── config/        # Configuration files
│   │   │   └── api.js     # API endpoints
│   │   ├── data/          # Static data
│   │   │   ├── travelPhotos.js
│   │   │   ├── professionalPhotos.js
│   │   │   └── sportsPhotos.js
│   │   ├── router/        # Vue Router
│   │   │   └── index.js
│   │   ├── views/         # Page components
│   │   │   ├── admin/     # Admin panel
│   │   │   ├── albums/    # Album pages
│   │   │   └── blog/      # Blog pages
│   │   ├── App.vue        # Root component
│   │   └── main.js        # Entry point
│   ├── tests/             # Vitest tests
│   ├── package.json
│   └── vite.config.js
├── backend/                # Flask backend API
│   ├── api/
│   │   ├── __init__.py
│   │   ├── index.py       # Main app and CORS
│   │   └── blog.py        # Blog endpoints
│   ├── tests/
│   │   └── test_blog.py
│   ├── requirements.txt
│   └── vercel.json
├── .github/
│   └── workflows/
│       └── ci.yml         # CI/CD pipeline
└── README.md              # This file
```

---

## 💻 Development Setup

### Prerequisites
- **Python 3.13+**
- **Node.js 20+**
- **npm**
- **Git**

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Environment Variables** (create `.env` or export):

```bash
# Required
export BLOG_ADMIN_KEY="your-secure-admin-key-change-this"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-supabase-anon-key"
export GEMINI_API_KEY="your-gemini-api-key"

# Optional
export FLASK_ENV=development
```

**Database Setup** (Supabase PostgreSQL):

```sql
CREATE TABLE blog_posts (
  id BIGSERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  excerpt TEXT,
  content TEXT NOT NULL,
  author TEXT DEFAULT 'Richwell Perez',
  tags TEXT[],
  published BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_blog_posts_published ON blog_posts(published);
CREATE INDEX idx_blog_posts_published_at ON blog_posts(published_at DESC);
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
```

**Run Backend:**

```bash
cd backend
flask run
# Server runs on http://localhost:5000
```

### Frontend Setup

```bash
cd frontend
npm install
```

**Environment Variables** (create `.env.local`):

```env
# Development
VITE_API_URL=http://localhost:5000

# Production
VITE_API_URL=https://richwellp-github-io.vercel.app
```

**Available Scripts:**

```bash
npm run dev          # Start development server (localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm test             # Run Vitest tests
npm run test:ui      # Run tests with UI
npm run test:coverage # Run tests with coverage report
```

**IDE Setup:**

- **Recommended:** [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar)
- **Important:** Disable Vetur if installed (conflicts with Vue - Official)

---

## 🧪 Testing

### Run All Tests

```bash
# Backend (18 tests)
cd backend && python -m pytest -v

# Frontend (33 tests)
cd frontend && npm test -- --run

# With coverage
cd backend && python -m pytest --cov
cd frontend && npm run test:coverage
```

### Add New Tests

**Backend:**
```bash
# Create: backend/tests/test_feature.py
cd backend && python -m pytest tests/test_feature.py -v
```

**Frontend:**
```bash
# Create: frontend/tests/unit/feature.test.js
cd frontend && npm test -- feature
```

---

## 🚢 Deployment

### Frontend (GitHub Pages)

Frontend is automatically deployed via GitHub Actions when you push to `main`.

**Workflow:** `.github/workflows/ci.yml`

```yaml
# Triggered on push to main
# Steps:
# 1. Run backend tests
# 2. Run frontend tests
# 3. Build frontend
# 4. Deploy to GitHub Pages
```

**Manual Deployment:**

```bash
cd frontend
npm run build
# Upload frontend/dist to hosting
```

**Configuration:**

- Repository Settings → Pages → Source: GitHub Actions
- Base URL: `base: '/'` in `vite.config.js`
- Build output: `frontend/dist/`

### Backend (Vercel)

**vercel.json Configuration:**

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    { "source": "/", "destination": "/api" },
    { "source": "/(.*)", "destination": "/api/$1" }
  ]
}
```

**Deployment Steps:**

1. Install Vercel CLI: `npm i -g vercel`
2. Link project: `cd backend && vercel`
3. Set environment variables in Vercel dashboard:
   - `BLOG_ADMIN_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GEMINI_API_KEY`
4. Deploy: `vercel --prod`

### CI/CD Pipeline

**Automated workflow** (`.github/workflows/ci.yml`):

1. **On every push/PR:**
   - Run backend tests (pytest)
   - Run frontend tests (vitest)
   - Build frontend bundle

2. **On push to `main`:**
   - Run all tests
   - Deploy to GitHub Pages (if tests pass)

**View status:** [Actions Tab](https://github.com/richwellp/richwellp.github.io/actions)

---

## 🌐 Site Structure

| Route | Description |
|-------|-------------|
| `/` | About Me - Introduction and education |
| `/experience` | Work history and academic projects |
| `/projects` | Portfolio of technical projects |
| `/cv` | Interactive PDF resume viewer |
| `/contact` | Contact form with backend validation |
| `/misc` | Hub for albums and blog |
| `/misc/albums` | Albums landing page |
| `/misc/travel` | Travel photo gallery (by location) |
| `/misc/professional` | Work events and milestones |
| `/misc/sports` | Volleyball and powerlifting |
| `/misc/blog` | Technical blog listing |
| `/misc/blog/:slug` | Individual blog post |
| `/admin` | Blog admin panel (requires auth) |
| `/admin/new` | Create new blog post |
| `/admin/edit/:slug` | Edit existing blog post |

---

## 📝 Content Management

### Adding Blog Posts

#### Via Admin Panel (Recommended)

1. Visit `/admin`
2. Enter your `BLOG_ADMIN_KEY`
3. Click "New Post"
4. Fill in:
   - **Title** - Post title
   - **Slug** - URL-friendly identifier (auto-generated from title)
   - **Excerpt** - Brief description for listings
   - **Content** - Markdown content with live preview
   - **Tags** - Comma-separated tags
   - **Author** - Defaults to "Richwell Perez"
   - **Dates** - Auto-filled timestamps
5. Toggle "Publish immediately" or save as draft
6. Click "Create Post"

#### Programmatically

```javascript
// Using the API directly
const response = await fetch('https://richwellp-github-io.vercel.app/blog/posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${BLOG_ADMIN_KEY}`
  },
  body: JSON.stringify({
    slug: 'my-post-slug',
    title: 'My Post Title',
    excerpt: 'Brief description',
    content: '# Markdown content here',
    tags: ['javascript', 'vue'],
    published: true,
    author: 'Richwell Perez'
  })
})
```

### Adding Photos/Videos to Albums

#### Travel Album (with location tabs)

1. Add media to `frontend/public/assets/photos/travel/<location>/`
2. Edit `frontend/src/data/travelPhotos.js`:

```javascript
export const travelPhotos = {
  wyoming: [
    {
      src: '/assets/photos/travel/wyoming/yellowstone.jpg',
      caption: 'Yellowstone National Park'
    },
    {
      src: '/assets/photos/travel/wyoming/sunset.mp4',
      type: 'video',  // Required for videos
      caption: 'Wyoming sunset timelapse'
    }
  ]
}
```

3. To add a new location tab:

```javascript
export const travelCategories = [
  { id: 'wyoming', name: 'Wyoming' },
  { id: 'texas', name: 'Texas' }  // New location
]

export const travelPhotos = {
  // ... existing locations
  texas: [
    { src: '/assets/photos/travel/texas/austin.jpg', caption: 'Austin skyline' }
  ]
}
```

#### Professional Album (simple grid)

1. Add media to `frontend/public/assets/photos/professional/`
2. Edit `frontend/src/data/professionalPhotos.js`:

```javascript
export const professionalPhotos = [
  {
    src: '/assets/photos/professional/graduation.jpg',
    caption: 'Graduation day at UIUC'
  },
  {
    src: '/assets/photos/professional/presentation.mp4',
    type: 'video',
    caption: 'Conference presentation'
  }
]
```

#### Sports Album (simple grid)

1. Add media to `frontend/public/assets/photos/sports/`
2. Edit `frontend/src/data/sportsPhotos.js`:

```javascript
export const sportsPhotos = [
  {
    src: '/assets/photos/sports/volleyball.jpg',
    caption: 'Volleyball tournament finals'
  }
]
```

3. Remove "Coming Soon" flag in `frontend/src/views/albums/SportsAlbum.vue`

#### Media Format Guidelines

**Images:**
- Formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- No `type` field needed (defaults to `'image'`)

**Videos:**
- Formats: `.mp4` (recommended), `.webm`, `.mov`
- **Must include** `type: 'video'`
- Keep under 20MB
- Use H.264 codec for MP4

### Creating a New Album

Example: Adding a "Food" album

1. **Create data file:** `frontend/src/data/foodPhotos.js`

```javascript
export const foodPhotos = [
  { src: '/assets/photos/food/ramen.jpg', caption: 'Homemade ramen' }
]
```

2. **Create view file:** `frontend/src/views/albums/FoodAlbum.vue`

```vue
<template>
  <AlbumViewer
    title="Food"
    icon="🍜"
    subtitle="Culinary adventures and recipes"
    :photos="foodPhotos"
  />
</template>

<script setup>
import AlbumViewer from '../../components/AlbumViewer.vue'
import { foodPhotos } from '../../data/foodPhotos'
</script>
```

3. **Add route** in `frontend/src/router/index.js`:

```javascript
{
  path: '/misc/food',
  name: 'food-album',
  component: () => import('../views/albums/FoodAlbum.vue')
}
```

4. **Link from navbar** or misc page

### Updating Resume

Replace `frontend/public/assets/Resume.pdf` with your updated PDF and rebuild.

---

## 🐛 Troubleshooting

### Common Issues

**Frontend not connecting to backend:**
- Check `VITE_API_URL` in `.env.local`
- Verify backend is running on correct port
- Check CORS configuration in `backend/api/index.py`

**Admin authentication failing:**
- Verify `BLOG_ADMIN_KEY` matches between backend `.env` and login
- Check browser console for 401/403 errors
- Ensure key is set in Vercel environment variables

**Images not loading:**
- Verify file path is correct (`/assets/photos/...`)
- Check file exists in `frontend/public/assets/photos/`
- Clear browser cache

**Build failing:**
- Run `npm install` to update dependencies
- Check Node.js version (requires 20.x+)
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Tests failing:**
- Update snapshots: `npm test -- -u`
- Check mock data matches actual API responses
- Verify environment variables are set for tests

**CORS errors:**
- Add your domain to `CORS(app, origins=[...])` in `backend/api/index.py`
- Ensure `OPTIONS` method is allowed
- Check browser dev tools network tab for preflight requests

### Development Tips

**Hot Module Replacement (HMR):**
Frontend auto-reloads on file changes. If HMR stops working:
```bash
# Kill dev server and restart
npm run dev
```

**Database Issues:**
Check Supabase connection:
```bash
curl -H "apikey: YOUR_KEY" "https://your-project.supabase.co/rest/v1/blog_posts?limit=1"
```

**Backend Debugging:**
Enable Flask debug mode:
```bash
export FLASK_ENV=development
flask run --debug
```

---

## 🏗️ Architecture Notes

### Why Monorepo Structure?
- **Backend tests** in `backend/tests/` - Python imports work correctly
- **Frontend tests** in `frontend/tests/` - JS module resolution works
- Each module is self-contained and independently deployable

### Why Separate Tests?
A centralized `/tests` folder would:
- Break Python imports (requires PYTHONPATH hacks)
- Break JS imports (requires config rewrites)
- Complicate CI/CD workflows

### Album System Architecture

**Benefits of Current Design:**
1. **No code duplication** - One `AlbumViewer` component handles all albums
2. **Easy to add photos** - Just edit a data file
3. **Easy to add new albums** - Create a new data file and page (10 lines of code)
4. **Consistent styling** - Changes to `AlbumViewer` affect all albums
5. **Maintainable** - Logic, styling, and data are separated

---

## License

Personal portfolio - all rights reserved.

## Contact

- **Email:** Contact via website
- **LinkedIn:** [richwellp](https://linkedin.com/in/richwellp)
