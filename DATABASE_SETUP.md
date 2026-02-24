# Database Setup Guide

## Quick Setup

Run these SQL commands in your Supabase SQL Editor in this exact order:

### Step 1: Create Albums Schema

Copy and run the **entire contents** of `backend/database/albums_schema.sql` in Supabase SQL Editor.

Or use this simplified version:

```sql
-- Albums table
CREATE TABLE IF NOT EXISTS albums (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT NOT NULL,
    subtitle TEXT,
    categories TEXT[] DEFAULT NULL,
    order_index INTEGER DEFAULT 0,
    published BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Photos table
CREATE TABLE IF NOT EXISTS photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    album_id UUID NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    caption TEXT,
    location TEXT,
    date_taken DATE,
    category TEXT,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_photos_album_id ON photos(album_id);
CREATE INDEX IF NOT EXISTS idx_photos_category ON photos(category);
CREATE INDEX IF NOT EXISTS idx_photos_date_taken ON photos(date_taken);
CREATE INDEX IF NOT EXISTS idx_albums_slug ON albums(slug);

-- RLS Policies (Read-only public access)
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read access to albums" ON albums;
CREATE POLICY "Allow public read access to albums" ON albums FOR SELECT USING (true);

DROP POLICY IF EXISTS "Allow public read access to photos" ON photos;
CREATE POLICY "Allow public read access to photos" ON photos FOR SELECT USING (true);
```

### Step 2: Seed Albums and Photos

Copy and run the **entire contents** of `backend/database/seed_photos.sql` in Supabase SQL Editor.

This will:
- Create 3 albums (Travel, Sports, Me)
- Add sample photos for Travel (USA, Philippines, Japan)
- Add sample photos for Me (Professional photos)
- Add placeholder for Sports photos (add your own later via /admin)

**Note:** The file uses `ON CONFLICT` so it's safe to run multiple times.

### Step 3: Create Blog Schema (if not exists)

```sql
-- From backend/database/blog_schema.sql

CREATE TABLE IF NOT EXISTS blog_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT DEFAULT 'Richwell Perez',
    published BOOLEAN DEFAULT false,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Auto-set published_at trigger
CREATE OR REPLACE FUNCTION set_published_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.published = TRUE AND (OLD.published = FALSE OR OLD.published IS NULL) AND NEW.published_at IS NULL THEN
        NEW.published_at = NOW();
    END IF;
    IF NEW.published = FALSE AND OLD.published = TRUE THEN
        NEW.published_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS blog_posts_published_trigger ON blog_posts;
CREATE TRIGGER blog_posts_published_trigger
    BEFORE INSERT OR UPDATE ON blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION set_published_at();

-- RLS Policies
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read access to published posts" ON blog_posts;
CREATE POLICY "Allow public read access to published posts"
    ON blog_posts FOR SELECT
    USING (published = true);
```

## Verification

After running the migrations, verify the tables exist:

```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;
```

You should see:
- albums
- blog_posts
- photos

## Environment Variables

Make sure your `.env` files have:

**Backend (.env)**
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
BLOG_ADMIN_KEY=your_admin_key
```

**Frontend (.env)**
```
VITE_API_URL=http://localhost:5000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Testing

1. Start backend: `cd backend && flask run`
2. Start frontend: `cd frontend && npm run dev`
3. Visit: `http://localhost:5173`
4. Albums page should load without errors
5. Visit `/admin` to test admin panel
