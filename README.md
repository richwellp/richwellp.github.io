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
```

---

## Table of Contents

- [Quick Start](#quick-start)
- [Common Content Updates](#common-content-updates)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Emergency Procedures](#-emergency-procedures)

---

## Quick Start

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

## Common Content Updates

> **Most updates require NO code changes - just edit JSON and push!**

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

### 1. Update Professional Information

**File:** `frontend/public/data/professionalInfo.json`

This single JSON file powers your Experience, Projects, About Me pages, Command Palette search, and AI Chatbot context.

#### Add a New Job

```json
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
        "Improved performance by 50%"
      ],
      "technologies": ["Python", "React", "AWS"]
    }
  ]
}
```

**Workflow:**
```bash
# 1. Edit the JSON
code frontend/public/data/professionalInfo.json

# 2. Validate syntax
cat frontend/public/data/professionalInfo.json | python -m json.tool

# 3. Test locally
cd frontend && npm run dev

# 4. Deploy
git add frontend/public/data/professionalInfo.json
git commit -m "Add new job experience"
git push origin main
```

### 2. Update Contact Information

**File:** `frontend/src/config/contact.js`

```javascript
export const CONTACT = {
  email: 'your.email@example.com',
  linkedin: 'https://www.linkedin.com/in/your-profile',
  github: 'https://github.com/yourusername'
}
```

### 3. Manage Blog Posts & Albums

Use the admin panel: **https://richwellp.github.io/admin**

**Features:**
- Markdown editor with live preview
- Draft/publish toggle
- Photo/video uploads (MP4, MOV, WEBM supported)
- Drag-and-drop reordering

**Admin Password:** Set as `BLOG_ADMIN_KEY` in Vercel environment variables

### 4. Update Your Resume

```bash
# Replace the PDF file
cp ~/Downloads/new-resume.pdf frontend/public/assets/Resume.pdf

git add frontend/public/assets/Resume.pdf
git commit -m "Update resume"
git push origin main
```

**Note:** Resume is automatically parsed and used in chatbot responses!

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
│   │       └── Resume.pdf              ← Replace to update resume
│   ├── src/
│   │   ├── components/                 # Reusable UI components
│   │   ├── composables/                # Shared logic
│   │   ├── views/                      # Page components
│   │   ├── config/
│   │   │   ├── contact.js              ← Contact information
│   │   │   └── api.js
│   │   └── router/
│   └── tests/                          # Vitest tests (47 tests)
│
├── backend/
│   ├── api/
│   │   ├── blog.py                     # Blog CRUD endpoints
│   │   ├── albums.py                   # Albums CRUD endpoints
│   │   ├── gemini.py                   # AI chatbot logic
│   │   └── index.py                    # Main Flask app
│   ├── config.py                       # Configuration
│   └── tests/                          # pytest tests (50 tests)
│
└── .github/workflows/
    └── ci-cd.yml                       # Automated testing on push
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

```bash
# Frontend tests (47 tests)
cd frontend
npm test -- --run                       # Run all tests once
npm test                                # Watch mode

# Backend tests (50 tests)
cd backend
python -m pytest -v                     # Run all tests
python -m pytest tests/test_blog.py -v  # Run specific file
```

**Golden Rule: TEST BEFORE DEPLOYING**

Both test suites must pass before pushing to main. GitHub Actions will also run tests automatically.

---

## 🐛 Troubleshooting

### Content Not Updating

**Problem:** Changed JSON but website shows old content

**Solutions:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Validate JSON syntax: `cat frontend/public/data/professionalInfo.json | python -m json.tool`
3. Check browser console (F12) for errors
4. Verify deployment: [vercel.com/dashboard](https://vercel.com/dashboard)

### Chatbot Not Working

**Check:**
1. `GEMINI_API_KEY` is set in Vercel environment variables
2. Browser console for errors (F12 → Console)
3. Gemini API quotas (free tier: 15 RPM, 1,500 RPD)

### Tests Failing

```bash
# 1. See what changed
git status
git diff

# 2. Reinstall dependencies
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
3. Look for red ❌ to see which test failed

**Common causes:**
- Test failure (run tests locally first!)
- Syntax error in code
- Missing environment variable in Vercel

### Debugging Tips

**Backend (Python):**
```python
def chat():
    user_message = request.get_json()['message']
    print(f"DEBUG: Received: {user_message}")  # Add this
    # ...
```

**Frontend (JavaScript):**
```javascript
const sendMessage = async (input) => {
  console.log('DEBUG: Sending:', input)  // Add this
  // ...
}
```

**Check Logs:**
- Local: Terminal running `flask run` + Browser console (F12)
- Production: https://vercel.com/dashboard → Your Project → Logs

---

## 🚨 Emergency Procedures

### Rollback to Previous Version

```bash
# 1. See recent commits
git log --oneline -10

# 2. Rollback to last working commit (e.g., abc123)
git reset --hard abc123

# 3. Force push (CAREFUL!)
git push origin main --force
```

⚠️ **Warning:** This permanently removes later commits. Only use in emergencies!

### Undo All Local Changes

```bash
# Discard ALL uncommitted changes
git checkout .

# Remove untracked files
git clean -fd
```

### Safe Experimentation

```bash
# Create experiment branch
git checkout -b experiment

# Make changes, test...

# If it works:
git checkout main
git merge experiment

# If it doesn't:
git checkout main
git branch -D experiment
```

---

## Key Features

- **AI Chat Assistant** - Context-aware chatbot powered by Google Gemini (2-4 second responses)
- **Blog System** - Markdown editor with admin panel
- **Photo Albums** - Video support, drag-and-drop management
- **Command Palette** - Quick navigation with Cmd/Ctrl + K
- **Responsive Design** - Works on all devices
- **Auto-Deployment** - Push to GitHub → Live in 2-3 minutes
- **Automated Testing** - 97 tests ensure quality

---

## 🤝 Contributing

This is a personal portfolio, but suggestions are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

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

> **Pro Tip:** Most updates only require editing `professionalInfo.json` - no code changes needed!
