# Richwell Perez - Portfolio

Personal portfolio with blog, photo albums, admin panel, and AI chatbot.

**Live:** [richwellp.github.io](https://richwellp.github.io)

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run  # http://localhost:5000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev  # http://localhost:5173
```

---

## Common Tasks

### Update Content

**Experience/Projects/Skills:** Edit `frontend/public/data/professionalInfo.json`
**Blog posts:** Use `/admin` panel (includes markdown editor)
**Photos:** Use `/admin/albums` panel
**Resume:** Replace `frontend/public/assets/Resume.pdf`
**Contact info:** Edit `frontend/src/config/contact.js`

### Test

```bash
cd backend && python -m pytest -v          # 50 tests
cd frontend && npm test -- --run           # 47 tests
```

### Deploy

```bash
git add .
git commit -m "your message"
git push origin main  # Auto-deploys via GitHub Actions
```

---

## Tech Stack

**Frontend:** Vue 3, Vite, Vue Router
**Backend:** Flask, Google Gemini AI
**Database:** Supabase (PostgreSQL + Storage)
**Deploy:** GitHub Pages + Vercel
**Tests:** Vitest (47) + pytest (50)

---

## Documentation

**[Complete Developer Guide](./docs/GUIDE.md)** - Everything: architecture, API endpoints, database schema, authentication, adding media, troubleshooting

---

## Features

- AI Chatbot (Google Gemini, 2-4s responses)
- Blog with markdown editor
- Photo/video albums
- Command Palette (Cmd/Ctrl+K)
- Responsive design
- Auto-deploy on push

---

## Environment Variables

Set in Vercel dashboard → Settings → Environment Variables:

**Backend:**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
BLOG_ADMIN_KEY=your_admin_password
GEMINI_API_KEY=your_gemini_key
```

**Frontend:**
```env
VITE_API_URL=https://your-backend.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

---

## Troubleshooting

**Tests failing:** `git status && git diff` to see changes
**Content not updating:** Hard refresh (`Ctrl+Shift+R`)
**Deployment failed:** Check [GitHub Actions](https://github.com/richwellp/richwellp.github.io/actions)

See [docs/GUIDE.md](./docs/GUIDE.md) for complete troubleshooting.

---

## Contact

**Richwell Perez**
- Email: [richwell.perez@gmail.com](mailto:richwell.perez@gmail.com)
- LinkedIn: [richwell-perez](https://linkedin.com/in/richwell-perez)
- GitHub: [richwellp](https://github.com/richwellp)
