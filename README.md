# Richwell Perez - Portfolio Website

A modern, full-stack personal portfolio featuring a blog system, photo albums, admin panel, and AI chatbot assistant.

**Live Site:** [richwellp.github.io](https://richwellp.github.io)

---

## How to Make Changes to Your Website

> **Most content updates require NO code changes - just edit JSON and push!**

### Quick Reference

| What to Update | File to Edit | Requires Coding? |
|----------------|--------------|------------------|
| **Job Experience** | `frontend/public/data/professionalInfo.json` | No |
| **Projects** | `frontend/public/data/professionalInfo.json` | No |
| **Skills** | `frontend/public/data/professionalInfo.json` | No |
| **Education** | `frontend/public/data/professionalInfo.json` | No |
| **Contact Info** | `frontend/src/config/contact.js` | No |
| **Blog Posts** | Admin Panel (`/admin`) | No |
| **Photo Albums** | Admin Panel (`/admin`) | No |
| **Resume PDF** | Replace `frontend/public/assets/Resume.pdf` | No |
| **Theme Colors** | `frontend/src/App.vue` (CSS variables) | Yes |
| **New Pages** | Create new `.vue` file + add route | Yes |

---

## Common Content Updates

### 1. Update Professional Information

**File:** `frontend/public/data/professionalInfo.json`

This single JSON file powers:
- Experience page (all job cards)
- Projects page (all project cards)
- About Me page (animations)
- Command Palette search (Cmd+K)
- AI Chatbot context

#### Add a New Job

```bash
# 1. Open the JSON file
code frontend/public/data/professionalInfo.json

# 2. Add to the "experience" array (at the top for most recent job)
{
  "experience": [
    {
      "title": "Software Engineer",
      "company": "New Company",
      "location": "San Francisco, CA",
      "dates": "January 2026 - Present",
      "current": true,
      "description": "Building amazing software products",
      "highlights": [
        "Led development of key feature X",
        "Improved performance by 50%",
        "Mentored 3 junior developers"
      ],
      "technologies": ["Python", "React", "AWS"]
    },
    // ... your other jobs below
  ]
}

# 3. Save, commit, and push
git add frontend/public/data/professionalInfo.json
git commit -m "Add new job experience"
git push

# 4. Wait ~2 minutes for Vercel to deploy
# 5. Changes appear everywhere automatically!
```

**What Updates Automatically:**
- Experience page shows new job card
- Chatbot knows about your new role
- Command Palette can search new company/technologies
- All without touching any code!

#### Add a New Project

```json
{
  "projects": [
    {
      "name": "My Awesome Project",
      "subtitle": "AI-Powered Task Manager",
      "description": "Built an AI assistant that helps manage daily tasks",
      "highlights": [
        "Integrated GPT-4 for natural language processing",
        "Deployed to 1000+ users in first month",
        "Featured on Product Hunt"
      ],
      "technologies": ["Vue.js", "Python", "OpenAI"],
      "links": ["https://github.com/username/project"]
    },
    // ... other projects
  ]
}
```

#### Update Skills (Including New Categories!)

```json
{
  "skills": {
    "languages": ["Python", "JavaScript", "Go"],
    "frameworks": ["Vue.js", "React", "Django"],
    "cloud": ["AWS", "Azure", "GCP"],
    "new_category": ["Skill 1", "Skill 2"]  // ← Add any category!
  }
}
```

**Magic:** New categories are automatically detected! No code changes needed.

### 2. Update Contact Information

**File:** `frontend/src/config/contact.js`

```javascript
export const CONTACT = {
  email: 'your.email@example.com',
  linkedin: 'https://www.linkedin.com/in/your-profile',
  github: 'https://github.com/yourusername'
}
```

This updates:
- Contact page
- Error messages
- Chatbot context

### 3. Update Blog Posts

Use the admin panel: **https://richwellp.github.io/admin**

**Features:**
- Markdown editor with live preview
- Syntax highlighting for code blocks
- Draft/publish toggle
- Tag management
- SEO metadata

**Admin Password:** Set as `BLOG_ADMIN_KEY` in Vercel environment variables

### 4. Manage Photo Albums

Use the admin panel: **https://richwellp.github.io/admin**

**Features:**
- Upload photos/videos
- Video support (MP4, MOV, WEBM)
- Create/manage albums
- Drag-and-drop reordering
- Set cover images
- Add captions, dates, locations

### 5. Update Your Resume

```bash
# Replace the PDF file
cp ~/Downloads/new-resume.pdf frontend/public/assets/Resume.pdf

# Commit and push
git add frontend/public/assets/Resume.pdf
git commit -m "Update resume"
git push
```

---

## Quick Start (Development)

### Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://python.org/))
- **Git** ([Download](https://git-scm.com/))

### Local Development

```bash
# Clone repository
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io

# Backend (Terminal 1)
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# Visit http://localhost:5173
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue 3, Vite, Vue Router, Vitest |
| **Backend** | Flask (Python), Google Gemini AI |
| **Database** | Supabase (PostgreSQL) |
| **Storage** | Supabase Storage (photos/videos) |
| **Deployment** | Vercel (auto-deploy from GitHub) |
| **CI/CD** | GitHub Actions (automated testing) |

---

## 📂 Project Structure

```
richwellp.github.io/
├── frontend/
│   ├── public/
│   │   ├── data/
│   │   │   └── professionalInfo.json  ← EDIT THIS for content updates
│   │   └── assets/
│   │       ├── photos/                 # Professional photos
│   │       └── Resume.pdf              ← Replace to update resume
│   ├── src/
│   │   ├── components/                 # Reusable UI components
│   │   ├── composables/                # Shared logic (Vue Composition API)
│   │   │   └── useProfessionalInfo.js ← Loads professional data
│   │   ├── views/                      # Page components
│   │   │   ├── Experience.vue          # Fully dynamic from JSON
│   │   │   ├── Projects.vue            # Fully dynamic from JSON
│   │   │   └── ...
│   │   ├── config/
│   │   │   └── contact.js             ← Contact information
│   │   └── router/
│   │       └── index.js               # Route definitions
│   └── tests/                         # Vitest unit tests (47 tests)
│
├── backend/
│   ├── api/
│   │   ├── blog.py                    # Blog CRUD endpoints
│   │   ├── albums.py                  # Albums CRUD endpoints
│   │   └── chat.py                    # AI Chatbot endpoint
│   ├── config.py                      # Configuration
│   └── tests/                         # pytest tests (50 tests)
│
├── MAINTENANCE_GUIDE.md               ← Detailed maintenance guide
├── DEPLOYMENT_GUIDE.md                ← Deployment instructions
└── REFACTORING_SUMMARY.md             ← Recent changes summary
```

---

## 🔐 Environment Variables

### Backend (`backend/.env` or Vercel)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key  # NOT anon key
BLOG_ADMIN_KEY=your_secure_admin_password
GEMINI_API_KEY=your_gemini_api_key_from_google
ALLOWED_ORIGINS=https://richwellp.github.io
```

### Frontend (`frontend/.env` or Vercel)

```env
VITE_API_URL=https://your-backend.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

---

## 🧪 Testing

```bash
# Frontend tests (47 tests)
cd frontend
npm test -- --run

# Backend tests (50 tests)
cd backend
python -m pytest -v

# All tests must pass before deploying!
```

---

## 🚀 Deployment

### Automatic Deployment

**Every push to `main` branch automatically deploys:**

```bash
git add .
git commit -m "Your changes"
git push origin main

# GitHub Actions runs tests
# ↓
# If tests pass, Vercel deploys (~2-3 minutes)
# ↓
# Live at https://richwellp.github.io
```

### Manual Deploy (if needed)

```bash
# Build frontend
cd frontend
npm run build

# Deploy using Vercel CLI
vercel --prod
```

---

## 🎨 Customization Guide

### Change Theme Colors

**File:** `frontend/src/App.vue`

```css
/* Find the :root section and edit these variables */
:root {
  --accent-primary: #00d4aa;      /* Main accent (green)  */
  --bg-primary: #0a0e27;          /* Main background */
  --bg-secondary: #141b3b;        /* Alternate background */
  --bg-card: #1a2238;             /* Card background */
  --text-primary: #ffffff;        /* Main text color */
  --text-secondary: #a0aec0;      /* Secondary text */
}
```

### Add a New Page

**1. Create the page component:**

```vue
<!-- frontend/src/views/NewPage.vue -->
<template>
  <div class="new-page">
    <div class="container">
      <h1>New Page</h1>
      <p>Your content here...</p>
    </div>
  </div>
</template>

<script setup>
// Your logic here
</script>

<style scoped>
.new-page {
  padding: 4rem 2rem;
}
</style>
```

**2. Add route:**

```javascript
// frontend/src/router/index.js
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('../views/NewPage.vue')
}
```

**3. Add to navbar:**

```vue
<!-- frontend/src/App.vue - in the nav-links section -->
<RouterLink to="/new-page" @click="closeMobileMenu">
  New Page
</RouterLink>
```

### Modify Chatbot Behavior

**File:** `backend/config.py`

```python
# Change AI model
GEMINI_MODEL = 'gemini-2.5-flash'  # or 'gemini-1.5-pro'

# Rate limits
RATE_LIMIT_MESSAGES = 10  # messages per minute
RATE_LIMIT_WINDOW = 60    # window in seconds
```

---

## 🐛 Troubleshooting

### Content Not Updating

**Problem:** Changed JSON but website shows old content

**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Check Vercel deployment status: [vercel.com/dashboard](https://vercel.com/dashboard)
3. Verify JSON syntax: `cat frontend/public/data/professionalInfo.json | python -m json.tool`

### Chatbot Not Working

**Problem:** Chatbot doesn't respond

**Check:**
1. Verify `GEMINI_API_KEY` is set in Vercel environment variables
2. Check browser console for errors (F12 → Console)
3. Test API: `curl -X POST https://your-backend.vercel.app/chat -H "Content-Type: application/json" -d '{"message":"test"}'`

### Tests Failing

**Problem:** `npm test` or `pytest` shows failures

**Solution:**
```bash
# Clear caches and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

cd backend
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

- **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** - Comprehensive maintenance guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment step-by-step
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Recent changes and improvements

---

## Key Features

- **AI Chat Assistant** - Context-aware chatbot powered by Google Gemini
- **Blog System** - Markdown editor with admin panel
- **Photo Albums** - Video support, drag-and-drop management
- **Admin Panel** - Full CRUD for content management
- **Command Palette** - Quick navigation (Cmd/Ctrl + K)
- **Responsive Design** - Works perfectly on all devices
- **SEO Optimized** - Structured data and meta tags
- **Auto-Deployment** - Push to GitHub → Live in 2 minutes
- **Automated Testing** - 97 tests ensure quality

---

## 📊 Test Coverage

```
Frontend: 47 tests ✅
Backend:  50 tests ✅
Total:    97 tests ✅
```

All tests run automatically on every push via GitHub Actions.

---

## 🤝 Contributing

This is a personal portfolio, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `npm test` and `pytest`
5. Commit: `git commit -m "Add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## Contact

**Richwell Perez**

Email: [richwell.perez@gmail.com](mailto:richwell.perez@gmail.com)
LinkedIn: [richwell-perez](https://linkedin.com/in/richwell-perez)
GitHub: [richwellp](https://github.com/richwellp)

---

## 🎓 Learning Resources

**Vue 3:** [vuejs.org](https://vuejs.org/)
**Vite:** [vitejs.dev](https://vitejs.dev/)
**Flask:** [flask.palletsprojects.com](https://flask.palletsprojects.com/)
**Supabase:** [supabase.com/docs](https://supabase.com/docs)
**Gemini AI:** [ai.google.dev](https://ai.google.dev/)

---

**Built with Vue 3 and Flask**

> **Pro Tip:** Most updates only require editing `professionalInfo.json` - no code changes needed!
