# Richwell Perez - Portfolio Website

A modern, full-stack personal portfolio featuring a blog system, photo albums, admin panel, and AI chatbot assistant.

**Live Site:** [richwellp.github.io](https://richwellp.github.io)

---

## ✨ Features

- **Blog System** - Markdown editor with admin panel for managing posts
- **Photo Albums** - API-driven albums with category filtering (Travel, Sports, Me)
- **Admin Panel** - Full CRUD for blog posts, albums, and photos
- **AI Chat Assistant** - Context-aware chatbot with streaming responses
- **Responsive Design** - Mobile-first, works on all devices
- **Dark/Light Theme** - Persistent theme switching
- **Command Palette** - Quick navigation (Cmd/Ctrl + K)
- **SEO Optimized** - Structured data and meta tags

---

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone and install dependencies
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

### 2. Deploy to Production

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for complete deployment guide including:
- Database setup (Supabase)
- Environment variables
- Vercel deployment
- Testing checklist

---

## 🛠️ Tech Stack

**Frontend:** Vue 3, Vite, Vue Router, Markdown-it, Vitest
**Backend:** Flask, Supabase PostgreSQL, Google Gemini API, pytest
**Deployment:** Vercel (backend), GitHub Pages/Vercel (frontend)

---

## 📂 Project Structure

```
richwellp.github.io/
├── frontend/                 # Vue 3 SPA
│   ├── src/
│   │   ├── components/      # Reusable Vue components
│   │   ├── composables/     # Composition API logic
│   │   ├── views/           # Page components
│   │   │   ├── admin/       # Admin panel views
│   │   │   ├── albums/      # Album viewer pages
│   │   │   └── blog/        # Blog pages
│   │   ├── router/          # Vue Router config
│   │   └── config/          # API endpoints
│   └── tests/               # Vitest unit tests
│
├── backend/                  # Flask API
│   ├── api/
│   │   ├── index.py         # Main app, chat endpoint
│   │   ├── blog.py          # Blog CRUD endpoints
│   │   ├── albums.py        # Albums CRUD endpoints
│   │   └── gemini.py        # AI chatbot logic
│   ├── database/            # SQL schemas and seeds
│   │   ├── albums_schema.sql
│   │   ├── blog_schema.sql
│   │   ├── seed_photos.sql
│   │   └── seed_blog_posts.sql
│   └── tests/               # pytest tests
│
├── docs/                     # Documentation
│   └── DEPLOYMENT.md        # Deployment guide
│
└── .github/workflows/       # CI/CD
    └── ci.yml               # Automated testing
```

---

## 🔐 Environment Variables

### Backend
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key  # NOT anon key
BLOG_ADMIN_KEY=your_admin_password
GEMINI_API_KEY=your_gemini_api_key
ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend
```env
VITE_API_URL=https://your-backend-url.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

---

## 🧪 Testing

```bash
# Backend tests (46 tests)
cd backend
pytest -v

# Frontend tests (43 tests)
cd frontend
npm test -- --run
```

---

## 📱 Admin Panel

Access at `/admin` with your admin key.

**Features:**
- **Blog Admin** (`/admin/blogs`) - Create, edit, publish, delete posts
- **Albums Admin** (`/admin/albums`) - Manage albums and categories
- **Photo Manager** (`/admin/albums/:slug/photos`) - Add, edit, delete photos
- **Dashboard** (`/admin`) - View stats and quick links

---

## 🏗️ Database Schema

**Albums** - id (UUID), slug, name, icon, subtitle, categories (text[]), order_index
**Photos** - id (UUID), album_id (FK), url, caption, location, date_taken, category, order_index
**Blog Posts** - id (UUID), slug, title, excerpt, content, published, published_at

SQL schemas available in `backend/database/`

---

## 🤝 Contributing

This is a personal portfolio, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass (`pytest` and `npm test`)
5. Submit a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📧 Contact

**Richwell Perez**
[richwell.perez@gmail.com](mailto:richwell.perez@gmail.com)
[LinkedIn](https://linkedin.com/in/richwellp) • [GitHub](https://github.com/richwellp)

---

Built with ❤️ using Vue 3 and Flask
