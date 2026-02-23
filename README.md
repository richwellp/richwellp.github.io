# Richwell's Portfolio

Personal portfolio website showcasing professional experience, projects, and interests.

**Live Site:** [richwellp.github.io](https://richwellp.github.io)

---

## Features

- **Responsive Design** - Desktop, tablet, and mobile optimized
- **Dark/Light Theme** - Persistent theme switching
- **Blog System** - Markdown-based with admin panel
- **Photo & Video Albums** - Travel, professional, and sports galleries
- **AI Chat Assistant** - Context-aware chatbot with streaming responses
- **PDF Resume Viewer** - Interactive embedded CV
- **CI/CD Pipeline** - Automated testing and deployment

---

## Tech Stack

### Frontend
- **Vue 3** + Composition API
- **Vue Router 4** - Client-side routing
- **Vite 7** - Fast build tool with HMR
- **Markdown-it** - Blog post rendering
- **Vitest** - Unit testing

### Backend
- **Flask** - Python web framework
- **Supabase** - Database for blog posts
- **Google Gemini API** - AI chatbot
- **pytest** - Testing framework

### Deployment
- **Frontend** → GitHub Pages (automated via GitHub Actions)
- **Backend** → Vercel (serverless functions)

---

## Project Structure

```
richwellp.github.io/
├── backend/              # Python/Flask API
│   ├── api/              # Endpoints (blog, chat)
│   ├── tests/            # pytest tests (18 tests)
│   └── requirements.txt
├── frontend/             # Vue.js SPA
│   ├── src/              # Components, views, composables
│   ├── tests/            # Vitest tests (11 tests)
│   └── package.json
└── .github/workflows/
    └── ci-cd.yml         # Automated testing + deployment
```

---

## Development

### Prerequisites
- **Python 3.11+**
- **Node.js 20+**
- **npm**

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run
```

**Environment variables** (create `.env`):
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_key
BLOG_ADMIN_KEY=your_admin_key
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Access at: `http://localhost:5173`

---

## Testing

### Run All Tests
```bash
# Backend (18 tests)
cd backend && python -m pytest tests/ -v

# Frontend (11 tests)
cd frontend && npm test -- --run
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

## CI/CD Pipeline

**Automated workflow** (`.github/workflows/ci-cd.yml`):
1. **On every push/PR:**
   - Run backend tests (pytest)
   - Run frontend tests (vitest)
   - Verify build succeeds

2. **On push to `main`:**
   - Run all tests
   - Deploy to GitHub Pages (if tests pass)

**View status:** [Actions Tab](https://github.com/richwellp/richwellp.github.io/actions)

---

## Site Structure

| Route | Description |
|-------|-------------|
| `/` | About Me - Introduction and education |
| `/experience` | Work history and academic projects |
| `/cv` | Interactive PDF resume |
| `/misc` | Hub for albums and blog |
| `/misc/travel` | Travel photo gallery |
| `/misc/professional` | Work events and milestones |
| `/misc/sports` | Volleyball and powerlifting |
| `/misc/blog` | Technical blog |
| `/misc/blog/:slug` | Individual blog post |
| `/admin` | Blog admin panel (requires auth) |

---

## Adding Content

### Blog Posts
1. Create markdown file: `public/blog/YYYY-MM-DD-post-slug.md`
2. File is automatically discovered by Vite
3. Access at: `/misc/blog/post-slug`

**Or use Admin Panel:**
- Visit `/admin` with admin key
- Create, edit, publish posts via web UI

### Photos/Videos
1. Add files to: `public/assets/photos/{category}/`
2. Update data files in `src/data/`
3. See `src/data/README.md` for details

### Resume
Replace `public/assets/Resume.pdf` and rebuild.

---

## Architecture Notes

### Why Monorepo Structure?
- **Backend tests** in `backend/tests/` - Python imports work correctly
- **Frontend tests** in `frontend/tests/` - JS module resolution works
- Each module is self-contained and independently deployable

### Why Separate Tests?
A centralized `/tests` folder would:
- Break Python imports (requires PYTHONPATH hacks)
- Break JS imports (requires config rewrites)
- Complicate CI/CD workflows

---

## License

Personal portfolio - all rights reserved.

## Contact

- **Email:** Contact via website
- **LinkedIn:** [richwellp](https://linkedin.com/in/richwellp)
