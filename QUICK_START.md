# Quick Start Guide

## 🚀 Get Up and Running in 3 Steps

### 1️⃣ Run Database Migrations (Supabase SQL Editor)

Open your Supabase project → SQL Editor, then run these **2 files in order**:

**First:** `backend/database/albums_schema.sql`
- Creates albums and photos tables
- Sets up indexes and RLS policies

**Second:** `backend/database/seed_photos.sql`
- Creates 3 albums (Travel, Sports, Me)
- Adds sample photos
- Safe to run multiple times

**Optional:** If blog_posts table doesn't exist, run `backend/database/blog_schema.sql`

### 2️⃣ Test Locally

```bash
# Terminal 1 - Backend
cd backend
flask run

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit http://localhost:5173

**Test these pages:**
- ✅ Albums page (`/misc/albums`) - should show 3 albums
- ✅ Travel album - should show photos by category
- ✅ Admin panel (`/admin`) - enter your admin key

### 3️⃣ Deploy

```bash
git push origin main
```

**Environment Variables Needed:**

Backend (Vercel):
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `BLOG_ADMIN_KEY`

Frontend (Vercel):
- `VITE_API_URL` (your backend URL)
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## 🔧 Troubleshooting

**"relation 'albums' does not exist"**
→ Run `backend/database/albums_schema.sql` in Supabase

**"No photos showing"**
→ Run `backend/database/seed_photos.sql` in Supabase

**Admin panel not working**
→ Check `BLOG_ADMIN_KEY` is set in backend environment

**Images not loading**
→ Photo URLs in database must point to valid images (update via `/admin/albums/:slug/photos`)

## 📖 Full Documentation

- **DATABASE_SETUP.md** - Detailed database setup with full SQL
- **DEPLOYMENT_CHECKLIST.md** - Complete deployment guide with testing checklist
- **README.md** - Project overview and architecture

## ✨ What's New

- **Albums Admin Panel** - Manage albums at `/admin/albums`
- **Photo Manager** - Manage photos at `/admin/albums/:slug/photos`
- **Category Filtering** - Travel album supports USA, Philippines, Japan categories
- **Mobile Responsive** - All admin pages work on mobile
- **API-Driven** - All album data from Supabase, no hardcoded photos

## 🎯 Next Steps

1. Upload photos via admin panel
2. Add your sports photos
3. Customize album categories
4. Write blog posts via `/admin/blogs`
5. Update photo captions and locations
