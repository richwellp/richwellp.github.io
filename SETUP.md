# Setup Guide

Complete guide to set up this portfolio project on a new machine.

## Prerequisites

- **Node.js**: v20.19.0 or v22.12.0+ (check: `node --version`)
- **Python**: 3.11+ (check: `python --version`)
- **Git**: Latest version (check: `git --version`)
- **npm**: Comes with Node.js (check: `npm --version`)

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/richwellp/richwellp.github.io.git
cd richwellp.github.io

# 2. Setup backend
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Create .env file (see Backend Setup below)

# 3. Setup frontend
cd ../frontend
npm install
# Create .env file (see Frontend Setup below)

# 4. Run locally
# Terminal 1 (Backend):
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
flask run

# Terminal 2 (Frontend):
cd frontend
npm run dev
```

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create Environment File

Create `backend/.env` with these variables:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key_here

# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Blog Admin Authentication
BLOG_ADMIN_KEY=your_secure_random_key_here

# CORS Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:*,https://yourdomain.com,https://*.vercel.app
```

### 3. Get API Keys

#### Supabase (Database)

1. Go to https://supabase.com/dashboard
2. Click **"New Project"**
3. Fill in project details, wait ~2 minutes for setup
4. Go to **Settings** → **API**
5. Copy:
   - **Project URL** → Use as `SUPABASE_URL`
   - **service_role** key → Use as `SUPABASE_KEY` (⚠️ Keep secret!)

#### Create Database Table

In Supabase SQL Editor, run:

```sql
CREATE TABLE blog_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    author VARCHAR(255) DEFAULT 'Your Name',
    tags TEXT[] DEFAULT '{}',
    published BOOLEAN DEFAULT false,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_posts_published ON blog_posts(published, published_at DESC);
CREATE INDEX idx_posts_slug ON blog_posts(slug);
CREATE INDEX idx_posts_tags ON blog_posts USING GIN(tags);
```

#### Gemini API (Chatbot)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click **"Create API Key"**
4. Copy key → Use as `GEMINI_API_KEY`

#### Blog Admin Key

Generate a secure random string:

```bash
# On macOS/Linux:
openssl rand -hex 32

# On Windows (PowerShell):
[Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

# Or just use a strong password
```

### 4. Verify Setup

```bash
cd backend
python -m pytest -v  # All tests should pass
flask run            # Should start on http://localhost:5000
```

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Create Environment File

Create `frontend/.env`:

```bash
# Backend API URL
VITE_API_URL=http://localhost:5000

# Optional: Override contact information
# VITE_CONTACT_EMAIL=your-email@example.com
# VITE_CONTACT_LINKEDIN=https://linkedin.com/in/your-profile
# VITE_CONTACT_GITHUB=https://github.com/yourusername
```

### 3. Verify Setup

```bash
cd frontend
npm test -- --run     # All tests should pass
npm run dev           # Should start on http://localhost:5173
```

---

## Configuration Files

### Backend Config (`backend/config.py`)

Centralized constants for:
- Rate limiting (10 requests / 60 seconds)
- Message limits (2000 characters)
- Gemini model selection
- Contact information

Edit this file to change default behavior.

### Frontend Config

- `frontend/src/config/api.js` - API endpoints
- `frontend/src/config/contact.js` - Contact information
- `frontend/src/config/constants.js` - App-wide constants

---

## Deployment

### Backend (Vercel)

1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Deploy: `cd backend && vercel`
4. Add environment variables in Vercel Dashboard:
   - Go to project → Settings → Environment Variables
   - Add all variables from `.env` file
   - Select all environments (Production, Preview, Development)
5. Redeploy to apply env vars

### Frontend (GitHub Pages)

Frontend auto-deploys via GitHub Actions when you push to `main`.

Before deploying, update `frontend/.env`:
```bash
VITE_API_URL=https://your-vercel-backend.vercel.app
```

Commit and push:
```bash
git add frontend/.env
git commit -m "Update production API URL"
git push origin main
```

---

## Environment Variables Reference

| Variable | Where Used | Required | Description |
|----------|------------|----------|-------------|
| `SUPABASE_URL` | Backend | Yes | Supabase project URL |
| `SUPABASE_KEY` | Backend | Yes | Supabase service role key |
| `GEMINI_API_KEY` | Backend | Yes | Google Gemini API key |
| `BLOG_ADMIN_KEY` | Backend | Yes | Secret key for blog admin auth |
| `ALLOWED_ORIGINS` | Backend | No | CORS allowed origins (has defaults) |
| `VITE_API_URL` | Frontend | Yes | Backend API base URL |
| `VITE_CONTACT_EMAIL` | Frontend | No | Override default email |
| `VITE_CONTACT_LINKEDIN` | Frontend | No | Override default LinkedIn |
| `VITE_CONTACT_GITHUB` | Frontend | No | Override default GitHub |

---

## Troubleshooting

### Backend

**Tests fail with "ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
source backend/.venv/bin/activate  # Linux/Mac
backend\.venv\Scripts\activate     # Windows
```

**"SUPABASE_URL not found"**
```bash
# Check .env file exists in backend/ directory
# Check python-dotenv is installed
pip install python-dotenv
```

**Flask won't start**
```bash
# Set Flask app manually
export FLASK_APP=api/index.py  # Linux/Mac
set FLASK_APP=api/index.py     # Windows

# Or run with python
python -m flask run
```

### Frontend

**"VITE_API_URL is not set" error**
```bash
# Create frontend/.env file with VITE_API_URL
echo "VITE_API_URL=http://localhost:5000" > frontend/.env
```

**Build fails**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 already in use**
```bash
# Kill process on port 5173 (Linux/Mac)
lsof -ti:5173 | xargs kill

# Or change port
npm run dev -- --port 3000
```

### API Connection Issues

**CORS errors in browser console**
```bash
# Check backend ALLOWED_ORIGINS includes your frontend URL
# Update backend/.env:
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**404 on API calls**
```bash
# Verify backend is running on correct port
# Check VITE_API_URL matches backend URL
# Backend default: http://localhost:5000
```

---

## Running Tests

### Backend Tests

```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m pytest -v
```

Expected: 12 tests passing

### Frontend Tests

```bash
cd frontend
npm test -- --run
```

Expected: 11 tests passing

---

## Project Structure

```
richwellp.github.io/
├── backend/
│   ├── api/
│   │   ├── blog.py         # Blog API endpoints
│   │   ├── gemini.py       # Chatbot integration
│   │   ├── index.py        # Main Flask app
│   │   └── resume_parser.py
│   ├── config.py           # ⭐ Centralized config
│   ├── tests/
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env               # ⚠️ Create this (not tracked)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── config/        # ⭐ Centralized config
│   │   │   ├── api.js
│   │   │   ├── contact.js
│   │   │   └── constants.js
│   │   ├── data/
│   │   └── views/
│   ├── public/
│   ├── package.json
│   └── .env               # ⚠️ Create this (not tracked)
│
├── SETUP.md               # This file
└── README.md
```

---

## Next Steps

After setup:

1. **Test locally**: Verify both frontend and backend work
2. **Customize**: Update contact info in `frontend/src/config/contact.js`
3. **Add content**: Create blog posts via API or Supabase dashboard
4. **Deploy**: Follow deployment guide above
5. **Monitor**: Check Vercel logs for any errors

---

## Getting Help

- **Repository**: https://github.com/richwellp/richwellp.github.io
- **Issues**: https://github.com/richwellp/richwellp.github.io/issues
- **Documentation**:
  - [Flask](https://flask.palletsprojects.com/)
  - [Vue 3](https://vuejs.org/)
  - [Supabase](https://supabase.com/docs)
  - [Vercel](https://vercel.com/docs)
