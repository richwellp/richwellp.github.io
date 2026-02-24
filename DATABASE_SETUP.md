# Database Setup Guide

## Quick Setup (2 Steps)

Run these SQL files in your Supabase SQL Editor **in order**:

### Step 1: Create Albums Schema

Copy and paste the **entire contents** of `backend/database/albums_schema.sql` into Supabase SQL Editor and click "Run".

This creates:
- `albums` table with categories support
- `photos` table with all metadata fields
- Indexes for performance
- Row Level Security policies for public read access
- Updated_at triggers

### Step 2: Seed Albums and Photos

Copy and paste the **entire contents** of `backend/database/seed_photos.sql` into Supabase SQL Editor and click "Run".

This seeds:
- 3 albums (Travel with categories, Sports, Me)
- Sample travel photos (USA, Philippines, Japan)
- Sample personal photos
- Uses `ON CONFLICT` so it's safe to run multiple times

### Step 3: Create Blog Schema (If Needed)

If your `blog_posts` table doesn't exist yet, copy and paste `backend/database/blog_schema.sql` into Supabase SQL Editor and click "Run".

## Verification

After running the migrations, verify everything is set up correctly:

```sql
-- Check tables exist
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('albums', 'photos', 'blog_posts')
ORDER BY tablename;

-- Check albums were created
SELECT slug, name, icon, categories FROM albums ORDER BY order_index;

-- Check photos were created
SELECT
  a.name as album,
  COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON p.album_id = a.id
GROUP BY a.name
ORDER BY a.name;
```

Expected results:
- 3 tables: albums, blog_posts, photos
- 3 albums: Travel, Sports, Me
- Travel should have ~11 photos
- Me should have 2 photos
- Sports should have 0 photos (add via admin later)

## Environment Variables

Make sure your `.env` files have the correct Supabase credentials:

**Backend (`backend/.env` or Vercel Environment Variables)**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_role_key
BLOG_ADMIN_KEY=your_secure_admin_password
```

**Frontend (`frontend/.env` or Vercel Environment Variables)**
```env
VITE_API_URL=http://localhost:5000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Important:**
- Backend uses the **service_role** key for admin operations (bypasses RLS)
- Frontend uses the **anon** key for public read access
- Never expose service_role key in frontend code

## Testing

Start the servers and test:

```bash
# Terminal 1 - Backend
cd backend
flask run

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit http://localhost:5173 and test:
- Albums page (`/misc/albums`) should show 3 albums
- Click Travel album - should show photos grouped by category
- Click Me album - should show 2 photos
- Visit `/admin` and test CRUD operations

## Troubleshooting

**"relation 'albums' does not exist"**
→ Run `backend/database/albums_schema.sql` in Supabase SQL Editor

**"column 'categories' does not exist"**
→ Drop and recreate albums table, or add column manually:
```sql
ALTER TABLE albums ADD COLUMN IF NOT EXISTS categories TEXT[] DEFAULT NULL;
```

**"No photos showing"**
→ Run `backend/database/seed_photos.sql` in Supabase SQL Editor
→ Check that photo URLs point to valid images

**"Admin operations fail"**
→ Verify backend uses SUPABASE_KEY (service_role, not anon key)
→ Check BLOG_ADMIN_KEY is set correctly

**"UUID errors"**
→ Ensure you're using gen_random_uuid() for IDs, not BIGSERIAL

## Schema Reference

**Albums Table:**
- id (UUID, primary key)
- slug (text, unique)
- name (text)
- icon (text)
- subtitle (text)
- categories (text[], nullable)
- order_index (integer)
- published (boolean)
- created_at, updated_at (timestamptz)

**Photos Table:**
- id (UUID, primary key)
- album_id (UUID, foreign key)
- url (text, image URL)
- caption (text, nullable)
- location (text, nullable)
- date_taken (date, nullable)
- category (text, nullable)
- order_index (integer)
- created_at, updated_at (timestamptz)
