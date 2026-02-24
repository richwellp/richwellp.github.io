# Deployment Guide

Complete guide for deploying the portfolio with blog and albums features.

## Prerequisites

- Supabase project with SQL Editor access
- Vercel account (or any hosting service)
- Environment variables ready (see below)

## Quick Deploy (3 Steps)

### Step 1: Database Setup

Open Supabase SQL Editor and run these files in order:

**1.1 Albums Schema**
```bash
# Copy/paste: backend/database/albums_schema.sql
```
Creates albums and photos tables with UUID IDs, categories support, and RLS policies.

**1.2 Seed Data**
```bash
# Copy/paste: backend/database/seed_photos.sql
```
Creates 3 albums (Travel, Sports, Me) with sample photos.

**1.3 Blog Schema** (if needed)
```bash
# Copy/paste: backend/database/blog_schema.sql
```
Creates blog_posts table with auto-date trigger.

**Verify Setup:**
```sql
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('albums', 'photos', 'blog_posts')
ORDER BY tablename;

-- Should return: albums, blog_posts, photos
```

### Step 2: Environment Variables

**Backend (Vercel Environment Variables)**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key  # NOT anon key!
BLOG_ADMIN_KEY=your_secure_admin_password
ALLOWED_ORIGINS=https://yourdomain.com,https://*.vercel.app
```

**Frontend (Vercel Environment Variables)**
```env
VITE_API_URL=https://your-backend.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Important:**
- Backend uses **service_role** key for admin operations
- Frontend uses **anon** key for public reads
- Never expose service_role key in frontend

### Step 3: Deploy

```bash
git push origin main
```

Vercel will auto-deploy both frontend and backend.

## Local Testing

```bash
# Terminal 1 - Backend
cd backend
flask run

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit http://localhost:5173 and test:
- ✅ Albums page (`/misc/albums`)
- ✅ Individual albums (Travel, Sports, Me)
- ✅ Blog posts (`/misc/blog`)
- ✅ Admin panel (`/admin`) with your admin key

## Post-Deployment Checklist

### Public Features
- [ ] Home, Experience, Projects, CV, Contact pages load
- [ ] Albums page shows 3 albums
- [ ] Travel album filters by category (USA, Philippines, Japan)
- [ ] Blog list shows published posts only
- [ ] Individual blog posts display correctly
- [ ] Chatbot icon visible, messages stream smoothly
- [ ] All pages mobile responsive

### Admin Features
- [ ] `/admin` shows auth modal
- [ ] Dashboard displays blog and album stats
- [ ] Blog admin: create, edit, publish, delete posts
- [ ] Albums admin: create, edit, publish, delete albums
- [ ] Photo manager: add, edit, delete photos
- [ ] All admin pages mobile responsive

## Troubleshooting

**"relation 'albums' does not exist"**
→ Run `backend/database/albums_schema.sql` in Supabase

**"column 'categories' does not exist"**
→ Re-run albums_schema.sql (it adds this column)

**Photos not loading**
→ Check photo URLs in database point to valid images
→ Update via `/admin/albums/:slug/photos`

**Admin operations fail**
→ Verify backend uses service_role key (not anon)
→ Check BLOG_ADMIN_KEY matches what you enter in UI

**CORS errors**
→ Check ALLOWED_ORIGINS includes your frontend domain

## Database Schema

**Albums:**
- id (UUID), slug (text unique), name, icon, subtitle
- categories (text[]) - for category filtering
- order_index, published, timestamps

**Photos:**
- id (UUID), album_id (UUID FK), url (text)
- caption, location, date_taken, category
- order_index, timestamps

**Blog Posts:**
- id (UUID), slug (text unique), title, excerpt, content
- author, published, published_at, timestamps

## Admin Features

**Blog Admin** (`/admin/blogs`)
- Markdown editor with live preview
- Publish/unpublish toggle
- Reading time auto-calculation
- SEO-friendly slugs

**Albums Admin** (`/admin/albums`)
- Create albums with emoji icons
- Category configuration for filtering
- Publish/unpublish toggle
- Photo count display

**Photo Manager** (`/admin/albums/:slug/photos`)
- Add photos with URLs
- Edit captions, locations, dates
- Category assignment
- Sort by order, date, or category
- Drag-and-drop reordering (coming soon)

## Architecture

**Backend:** Flask + Supabase PostgreSQL
- RESTful API with blueprints
- Admin endpoints with Bearer token auth
- Rate limiting on chat endpoint

**Frontend:** Vue 3 + Vite
- Composition API with composables
- Vue Router for SPA navigation
- Mobile-first responsive design

**Database:** Supabase PostgreSQL
- UUID primary keys
- Row Level Security for public reads
- Service role key for admin writes

## Rollback Plan

If deployment issues occur:
1. Revert to previous Vercel deployment
2. Check GitHub Actions logs
3. Review Vercel deployment logs
4. Check Supabase logs for database errors

## Next Steps

After successful deployment:
1. Add your sports photos via admin panel
2. Customize Travel album categories
3. Write blog posts
4. Update photo captions and locations
5. Configure custom domain (optional)
