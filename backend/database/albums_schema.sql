-- Albums and Photos Schema for Supabase
-- Run this in your Supabase SQL Editor

-- ============================================
-- 1. Create Albums Table
-- ============================================
CREATE TABLE IF NOT EXISTS albums (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  icon TEXT NOT NULL DEFAULT '📷',
  subtitle TEXT,
  categories TEXT[] DEFAULT NULL,
  order_index INTEGER DEFAULT 0,
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for albums
CREATE INDEX IF NOT EXISTS idx_albums_slug ON albums(slug);
CREATE INDEX IF NOT EXISTS idx_albums_order ON albums(order_index);
CREATE INDEX IF NOT EXISTS idx_albums_published ON albums(published);

-- ============================================
-- 2. Create Photos Table
-- ============================================
CREATE TABLE IF NOT EXISTS photos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  album_id UUID NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  caption TEXT,
  location TEXT,
  date_taken DATE,
  category TEXT,
  order_index INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for photos
CREATE INDEX IF NOT EXISTS idx_photos_album_id ON photos(album_id);
CREATE INDEX IF NOT EXISTS idx_photos_category ON photos(category);
CREATE INDEX IF NOT EXISTS idx_photos_date_taken ON photos(date_taken);
CREATE INDEX IF NOT EXISTS idx_photos_order ON photos(album_id, order_index);

-- ============================================
-- 3. Create Updated_at Trigger Function
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to albums table
DROP TRIGGER IF EXISTS update_albums_updated_at ON albums;
CREATE TRIGGER update_albums_updated_at
    BEFORE UPDATE ON albums
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to photos table
DROP TRIGGER IF EXISTS update_photos_updated_at ON photos;
CREATE TRIGGER update_photos_updated_at
    BEFORE UPDATE ON photos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 4. Enable Row Level Security (RLS)
-- ============================================
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Public albums are viewable by everyone" ON albums;
DROP POLICY IF EXISTS "Public photos are viewable by everyone" ON photos;

-- Policy: Allow public read access to all albums (published filter handled in app)
CREATE POLICY "Public read access to albums"
ON albums FOR SELECT
USING (true);

-- Policy: Allow public read access to all photos (filtering handled in app)
CREATE POLICY "Public read access to photos"
ON photos FOR SELECT
USING (true);

-- Note: For admin write operations, use service_role key which bypasses RLS
-- The backend API uses the service_role key for admin operations

-- ============================================
-- 5. Verify Installation
-- ============================================
-- Run these queries to verify tables were created:
-- SELECT * FROM albums;
-- SELECT * FROM photos;
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('albums', 'photos');
