# Richwell Perez - Portfolio Website

A modern, full-stack personal portfolio featuring a blog system, photo albums, admin panel, and AI chatbot assistant.

**Live Site:** [richwellp.github.io](https://richwellp.github.io)

---

## Essential Commands

```bash
# TESTING (run before every commit!)
cd backend && python -m pytest -v          # Backend tests (50 tests)
cd frontend && npm test -- --run           # Frontend tests (47 tests)

# LOCAL DEVELOPMENT
cd backend && flask run                     # Backend: http://localhost:5000
cd frontend && npm run dev                  # Frontend: http://localhost:5173

# DEPLOYMENT
git add .
git commit -m "Your changes"
git push origin main                        # Auto-deploys via Vercel (~2-3 min)

# CODE QUALITY
cd frontend && npm run lint                 # Check for code issues
cd frontend && npm run build                # Test production build
```

---

## Table of Contents

- [How to Make Changes](#how-to-make-changes-to-your-website)
- [Quick Start (Development)](#quick-start-development)
- [Understanding Your Architecture](#understanding-your-architecture)
- [Common Content Updates](#common-content-updates)
- [Working Without AI](#working-without-ai)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Customization](#-customization-guide)
- [Debugging](#-debugging-strategies)
- [Troubleshooting](#-troubleshooting)
- [Emergency Procedures](#-emergency-procedures)

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

## Understanding Your Architecture

### Frontend (Vue 3)

**Key Pattern: Composables (Shared State)**

```javascript
// Composables = reusable logic with shared state
import { useProfessionalInfo } from './composables/useProfessionalInfo'

const { projects, experience, loadProfessionalInfo } = useProfessionalInfo()
await loadProfessionalInfo()  // Loads once, shared everywhere
```

**File Organization:**
- `frontend/src/views/` - Page components (Experience.vue, Projects.vue, etc.)
- `frontend/src/components/` - Reusable UI pieces (ChatAssistant.vue, CommandPalette.vue)
- `frontend/src/composables/` - Shared logic (useBlog.js, useProfessionalInfo.js)
- `frontend/src/router/` - URL routing configuration
- `frontend/public/data/` - **YOUR CONTENT** (professionalInfo.json)

### Backend (Flask + Python)

**File Organization:**
- `backend/api/` - API endpoints (blog.py, albums.py, gemini.py, index.py)
- `backend/config.py` - Configuration settings (rate limits, API keys)
- `backend/tests/` - Test files (pytest)

**Key Concepts:**
- **Blueprints:** Organize routes (blog_bp, albums_bp)
- **CORS:** Allows frontend to call backend from different domain
- **Rate Limiting:** Prevents API abuse (10 requests/minute per IP)

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

# 3. Validate JSON syntax (catches typos!)
cat frontend/public/data/professionalInfo.json | python -m json.tool

# 4. Test locally
cd frontend && npm run dev
# Visit http://localhost:5173 and verify changes

# 5. Deploy
git add frontend/public/data/professionalInfo.json
git commit -m "Add new job experience"
git push origin main
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
- Upload photos/videos (MP4, MOV, WEBM supported)
- Create/manage albums
- Drag-and-drop reordering
- Set cover images (videos prioritized)
- Add captions, dates, locations

### 5. Update Your Resume

```bash
# Replace the PDF file
cp ~/Downloads/new-resume.pdf frontend/public/assets/Resume.pdf

# Commit and push
git add frontend/public/assets/Resume.pdf
git commit -m "Update resume"
git push origin main
```

**Note:** Resume is automatically parsed and used in chatbot responses!

---

## Working Without AI

### Strategy 1: Read Existing Code

Your codebase has examples of everything:
- Need to add a new API endpoint? Look at `backend/api/blog.py`
- Need to create a component? Look at `frontend/src/components/`
- Need to write a test? Look at existing tests in `tests/` folders

### Strategy 2: Start Small

Don't try to understand everything at once:
1. Find the file you need to change
2. Make ONE small change
3. Test it immediately (`npm run dev`)
4. If it works, make another small change
5. Repeat

### Strategy 3: Use Tests as Safety Net

```bash
# Before making changes
cd backend && python -m pytest -v          # Should all pass
cd frontend && npm test -- --run           # Should all pass

# Make your changes...

# After making changes
cd backend && python -m pytest -v          # Still passing?
cd frontend && npm test -- --run           # Still passing?

# If tests fail, you broke something - undo or fix
```

### Strategy 4: Search the Codebase

```bash
# Find where something is used
grep -r "useProfessionalInfo" frontend/src/

# Find a function definition
grep -r "def call_gemini" backend/

# Find a component
find . -name "*Chat*.vue"
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
| **Analytics** | Cloudflare Web Analytics (privacy-friendly) |

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
│   │   │   ├── ChatAssistant.vue       # AI chatbot interface
│   │   │   ├── CommandPalette.vue      # Cmd+K search
│   │   │   └── MarkdownEditor.vue      # Blog post editor
│   │   ├── composables/                # Shared logic (Vue Composition API)
│   │   │   ├── useProfessionalInfo.js  # Loads professional data
│   │   │   ├── useBlog.js              # Blog API calls
│   │   │   ├── useChatAssistant.js     # Chatbot logic
│   │   │   └── useAdminAuth.js         # Admin authentication
│   │   ├── views/                      # Page components
│   │   │   ├── Experience.vue          # Fully dynamic from JSON
│   │   │   ├── Projects.vue            # Fully dynamic from JSON
│   │   │   ├── Contact.vue             # Contact form
│   │   │   └── admin/                  # Admin panel pages
│   │   ├── config/
│   │   │   ├── contact.js              # Contact information
│   │   │   └── api.js                  # API endpoint URLs
│   │   └── router/
│   │       └── index.js                # Route definitions
│   └── tests/                          # Vitest unit tests (47 tests)
│
├── backend/
│   ├── api/
│   │   ├── blog.py                     # Blog CRUD endpoints
│   │   ├── albums.py                   # Albums CRUD endpoints
│   │   ├── gemini.py                   # AI chatbot logic
│   │   ├── resume_parser.py            # PDF resume parser (cached)
│   │   └── index.py                    # Main Flask app, chat endpoints
│   ├── config.py                       # Configuration (rate limits, etc.)
│   └── tests/                          # pytest tests (50 tests)
│
├── .github/workflows/
│   └── ci-cd.yml                       # Automated testing on push
│
├── README.md                           # This file
└── MAINTENANCE_GUIDE.md                # Detailed maintenance guide
```

---

## 🔐 Environment Variables

### Backend (`backend/.env` or Vercel)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key        # NOT anon key!
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

**Where to set these:**
- **Local development:** Create `.env` files in `backend/` and `frontend/`
- **Production:** Set in Vercel dashboard → Project → Settings → Environment Variables

---

## 🧪 Testing

### Running Tests

```bash
# Frontend tests (47 tests)
cd frontend
npm test -- --run                       # Run all tests once
npm test                                # Watch mode (re-runs on changes)
npm test tests/unit/useBlog.test.js     # Run specific test file

# Backend tests (50 tests)
cd backend
python -m pytest -v                     # Run all tests with verbose output
python -m pytest tests/test_blog.py -v  # Run specific test file
python -m pytest -v -s                  # Show print statements
```

### Understanding Test Failures

**Example failure:**
```
FAILED tests/test_blog.py::test_create_post - AssertionError: assert 500 == 201
```

**What it means:**
- Test: `test_create_post`
- File: `tests/test_blog.py`
- Problem: Expected status code 201 (Created), got 500 (Server Error)
- Action: Check the blog post creation logic in `backend/api/blog.py`

### Why Tests Matter

Tests are **safety nets** - they catch bugs before users see them.

**Example:**
```python
# This test ensures the chatbot rate limit works
def test_rate_limit_works():
    # Send 10 messages (the limit)
    for i in range(10):
        response = client.post('/chat', json={'message': 'test'})
        assert response.status_code == 200

    # 11th message should be rejected
    response = client.post('/chat', json={'message': 'test'})
    assert response.status_code == 429  # Too Many Requests
```

If this test fails after you make a change, you know you broke the rate limiter.

**Golden Rule: TEST BEFORE DEPLOYING**

```bash
# Every single time, before git push:
cd backend && python -m pytest -v
cd frontend && npm test -- --run

# Both must show "passed" - no failures
# If tests fail, DON'T push - fix the issue first
```

---

## 🚀 Deployment

### Automatic Deployment

**Every push to `main` branch automatically deploys:**

```bash
git add .
git commit -m "Your changes"
git pushgin main

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

### Deployment Checklist

Before pushing to main:
- [ ] All tests pass locally
- [ ] Changes tested in dev server (`npm run dev`)
- [ ] JSON files validated (`python -m json.tool`)
- [ ] No console errors in browser (F12)
- [ ] Git commit message is clear

---

## 🎨 Customization Guide

### Change Theme Colors

**File:** `frontendue`

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
<!-- frontend/src/views/Testimonials.vue -->
<template>
  <div class="testimonials">
    <div class="container">
      <h1>Testimonials</h1>
      <p>What people say about working with me...</p>
      <!-- Your content here -->
    </div>
  </div>
</template>

<script setup>
// Your JavaScript here
</script>

<style scoped>
.testimonials {
  padding: 4rem 2rem;
}
/* Copy CSS patterns from other pages */
</style>
```

**2. Add route:**

```javascript
// frontend/src/router/index.js
{
  path: '/testimonials',
  name: 'Testimonials',
  component: () => import('../views/Testimonials.vue')
}
```

**3. Add to navbar:**

```vue
<!-- frontend/src/App.vue - in the nav-links section -->
<RouterLink to="/testimonials" @click="closeMobileMenu">
  Testimonials
</RouterLink>
```

**4. Test and deploy:**

```bash
npm run dev  # Test locally at http://localhost:5173/testimonials
git add .
git commit -m "Add testimonials page"
git push origin main
```

### Modify Chatbot Behavior

**File:** `backend/config.py`

```python
# Change AI model
GEMINI_MODEL = 'gemini-2.5-flash'  # or 'gemini-1.5-pro'

# Rate limits
RATE_LIMIT_REQUESTS = 10  # messages per minute
RATE_LIMIT_WINDOW = 60    # window in seconds

# Message length
MESSAGE_LENGTH_LIMIT = 2000  # characters
HISTORY_LIMIT = 20  # maximum conversation history
```

---

## 🐛 Debugging Strategies

### 1. Use Print Statements

**Backend (Python):**

```python
def chat():
    user_message = request.get_json()['message']
    print(f"DEBUG: Received message: {user_message}")  # Add this

    response = call_gemini(user_message)
    print(f"DEBUG: Gemini response: {response}")       # Add this

    return jsonify(response=response)
```

**Frontend (JavaScript):**

```javascript
const sendMessage = async (input) => {
  console.log('DEBUG: Sending message:', input)  // Add this

  const response = await fetch('/chat', { ... })
  const data = await response.json()

  console.log('DEBUG: Received:', data)  // Add this
}
```

### 2. Browser DevTools (F12)

- **Console Tab:** Shows JavaScript errors and your `console.log()` statements
- **Network Tab:** Shows all API requests - click one to see request/response
- **Elements Tab:** Inspect HTML/CSS to debug styling issues

### 3. Flask Debug Mode (Local Only)

```bash
# Shows detailed error pages with stack traces
export FLASK_DEBUG=1  # Linux/Mac
set FLASK_DEBUG=1     # Windows
flask run
```

⚠️ **Never enable debug mode in production!**

### 4. Check Logs

**Local Development:**
- Backend: Terminal running `flask run` shows all requests and errors
- Frontend: Browser console (F12 → Console)

**Production (Vercel):**
- Visit: https://vercel.com/dashboard → Your Project → Logs
- Filter by "Errors" to see what went wrong

---

## 🐛 Troubleshooting

### Content Not Updating

**Problem:** Changed JSON but website shows old content

**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Check Vercel deployment status: [vercel.com/dashboard](https://vercel.com/dashboard)
3. Verify JSON syntax: `cat frontend/public/data/professionalInfo.json | python -m json.tool`
4. Check browser console (F12) for errors

### Chatbot Not Working

**Problem:** Chatbot doesn't respond

**Check:**
1. Verify `GEMINI_API_KEY` is set in Vercel environment variables
2. Check browser console for errors (F12 → Console)
3. Test API directly:
   ```bash
   curl -X POST https://your-backend.vercel.app/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"test"}'
   ```
4. Check Gemini API quotas (free tier: 15 RPM, 1,500 RPD)

### Tests Failing

**Problem:** `npm test` or `pytest` shows failures

**Solution:**

```bash
# 1. Did you change code? See what changed
git status              # See modified files
git diff                # See exact changes

# 2. Dependencies issue? Reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

cd backend
pip install -r requirements.txt --force-reinstall

# 3. Run tests again
cd backend && python -m pytest -v
cd frontend && npm test -- --run
```

### Deployment Failed

**Check GitHub Actions:**
1. Go to: https://github.com/richwellp/richwellp.github.io/actions
2. Click the failed run
3. Look for red ❌ - shows which test failed

**Common causes:**
- Test failure (run tests locally first!)
- Syntax error in code
- Missing environment variable in Vercel

### Website Shows 404 or Blank Page

**Check:**
1. Build succeeded: `cd frontend && npm run build`
2. Routes are correct: Check `frontend/src/router/index.js`
3. Vercel deployment logs for errors

---

## 🚨 Emergency Procedures

### Rollback to Previous Version

**If you break something badly:**

```bash
# 1. See recent commits
git log --oneline -10

# 2. Identify the last working commit (e.g., abc123)
# 3. Rollback to that commit
git reset --hard abc123

# 4. Force push (CAREFUL - overwrites remote)
git push origin main --force

# Vercel will auto-deploy the old working version in ~2 minutes
```

⚠️ **Warning:** This permanently removes commits after `abc123`. Only use in emergencies!

### Undo All Local Changes

```bash
# Discard ALL uncommitted changes
git checkout .

# Remove untracked files
git clean -fd

# Your code is back to the last commit
```

### Create a Safe Experiment Branch

```bash
# Create new branch for experiments
git checkout -b experiment

# Make changes, test...
# If it works:
git checkout main
git merge experiment

# If it doesn't work:
git checkout main
git branch -D experiment  # Delete the branch
```

---

## 📊 Test Coverage

```
Frontend: 47 tests ✅
Backend:  50 tests ✅
Total:    97 tests ✅
```

All tests run automatically on every push via GitHub Actions.

---

## Key Features

- **AI Chat Assistant** - Context-aware chatbot powered by Google Gemini (2-4 second responses)
- **Blog System** - Markdown editor with admin panel, live preview
- **Photo Albums** - Video support (MP4/MOV/WEBM), drag-and-drop management
- **Admin Panel** - Full CRUD for content management at `/admin`
- **Command Palette** - Quick navigation with Cmd/Ctrl + K
- **Responsive Design** - Works perfectly on all devices
- **SEO Optimized** - Structured data and meta tags
- **Auto-Deployment** - Push to GitHub → Live in 2-3 minutes
- **Automated Testing** - 97 tests ensure quality (runs on every push)
- **Performance Optimized** - Resume caching, prompt caching, context preloading

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

- Email: [richwell.perez@gmail.com](mailto:richwell.perez@gmail.com)
- LinkedIn: [richwell-perez](https://linkedin.com/in/richwell-perez)
- GitHub: [richwellp](https://github.com/richwellp)

---

## 🎓 Learning Resources

**Vue 3:** [vuejs.org](https://vuejs.org/guide/)
**Vite:** [vitejs.dev](https://vitejs.dev/)
**Flask:** [flask.palletsprojects.com](https://flask.palletsprojects.com/)
**Supabase:** [supabase.com/docs](https://supabase.com/docs)
**Gemini AI:** [ai.google.dev](https://ai.google.dev/)
**Pytest:** [docs.pytest.org](https://docs.pytest.org/en/stable/)
**Vitest:** [vitest.dev/guide](https://vitest.dev/guide/)

---

## Additional Documentation

- **[MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md)** - Comprehensive maintenance guide (900+ lines)
- **Detailed deployment guide** included in this README (see Deployment section)
- **Refactoring summaries** available in git history

---

**Built with Vue 3 and Flask**

> **Pro Tip:** Most updates only require editing `professionalInfo.json` - no code changes needed!

> **You CAN maintain this yourself:** 90% of updates = edit JSON, tests catch bugs automatically, everything is documented. Start small, learn by doing. 💪
