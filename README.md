# Richwell Perez - Portfolio

My personal portfolio with blog, photo albums, admin panel, and AI chatbot.

**Live:** [richwellp.github.io](https://richwellp.github.io)

---

## Quick Commands

```bash
# Test before committing
cd backend && python -m pytest -v          # 50 tests
cd frontend && npm test -- --run           # 47 tests

# Run locally
cd backend && flask run                     # http://localhost:5000
cd frontend && npm run dev                  # http://localhost:5173

# Deploy
git push origin main                        # Auto-deploys via Vercel
```

---

## Setup

**Requirements:** Node.js 18+, Python 3.11+, Git

```bash
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173

---

## Updating Content

Most content updates don't require code changes - just edit JSON and push.

### Professional Info (Experience, Projects, Skills)

**Edit:** `frontend/public/data/professionalInfo.json`

This file powers the Experience page, Projects page, About Me, search, and chatbot.

Example - adding a job:

```json
{
  "experience": [
    {
      "title": "Software Engineer",
      "company": "Acme Corp",
      "location": "SF",
      "dates": "Jan 2026 - Present",
      "current": true,
      "description": "Building stuff",
      "highlights": [
        "Led feature X",
        "Improved performance 50%"
      ],
      "technologies": ["Python", "React"]
    }
  ]
}
```

Test locally, then:

```bash
git add frontend/public/data/professionalInfo.json
git commit -m "Add new job"
git push
```

### Contact Info

**Edit:** `frontend/src/config/contact.js`

```javascript
export const CONTACT = {
  email: 'your.email@example.com',
  linkedin: 'https://linkedin.com/in/yourprofile',
  github: 'https://github.com/yourusername'
}
```

### Blog Posts & Albums

Use the admin panel at `/admin` - includes markdown editor, draft/publish toggle, and photo uploads.

**Admin password:** Set `BLOG_ADMIN_KEY` in Vercel environment variables.

### Resume

Replace `frontend/public/assets/Resume.pdf` with your new resume and push.

---

## Tech Stack

- **Frontend:** Vue 3, Vite, Vue Router
- **Backend:** Flask, Google Gemini AI
- **Database:** Supabase (PostgreSQL)
- **Storage:** Supabase Storage
- **Deploy:** Vercel
- **Tests:** Vitest (47) + pytest (50)

---

## Project Structure

```
richwellp.github.io/
├── frontend/
│   ├── public/data/professionalInfo.json  ← Edit for content
│   ├── public/assets/Resume.pdf            ← Replace resume here
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── composables/    # Shared logic
│   │   ├── views/          # Pages
│   │   ├── config/
│   │   │   └── contact.js  ← Edit contact info
│   │   └── router/
│   └── tests/              # 47 tests
│
├── backend/
│   ├── api/                # Flask endpoints
│   ├── config.py
│   └── tests/              # 50 tests
│
└── .github/workflows/      # CI/CD
```

---

## Environment Variables

### Backend

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
BLOG_ADMIN_KEY=your_admin_password
GEMINI_API_KEY=your_gemini_key
ALLOWED_ORIGINS=https://richwellp.github.io
```

### Frontend

```env
VITE_API_URL=https://your-backend.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

Set these in Vercel dashboard → Settings → Environment Variables.

---

## Testing

```bash
# Frontend
cd frontend
npm test -- --run        # Run once
npm test                 # Watch mode

# Backend
cd backend
python -m pytest -v      # All tests
python -m pytest tests/test_blog.py -v  # Specific file
```

Always test before pushing. GitHub Actions runs tests automatically on push.

---

## Troubleshooting

### Content not updating

Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

Validate JSON:
```bash
cat frontend/public/data/professionalInfo.json | python -m json.tool
```

### Chatbot not working

Check Vercel environment variables for `GEMINI_API_KEY`.

Check browser console (F12) for errors.

### Tests failing

```bash
# Check what changed
git status && git diff

# Reinstall
cd frontend && rm -rf node_modules package-lock.json && npm install
cd backend && pip install -r requirements.txt --force-reinstall

# Rerun
cd backend && python -m pytest -v
cd frontend && npm test -- --run
```

### Deployment failed

Check GitHub Actions: https://github.com/richwellp/richwellp.github.io/actions

Look for ❌ to see what failed.

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

## Features

- **AI Chatbot** - Google Gemini powered, 2-4 second responses
- **Blog** - Markdown editor with admin panel
- **Albums** - Photo/video support, drag-and-drop
- **Command Palette** - Cmd/Ctrl + K for quick nav
- **Responsive** - Works on all devices
- **Auto-deploy** - Push to GitHub → Live in 2-3 min

---

## Contact

**Richwell Perez**
- Email: [richwell.perez@gmail.com](mailto:richwell.perez@gmail.com)
- LinkedIn: [richwell-perez](https://linkedin.com/in/richwell-perez)
- GitHub: [richwellp](https://github.com/richwellp)

