-- Albums and Photos Schema for Supabase
-- Run this in your Supabase SQL Editor

-- ============================================
-- 1. Create Albums Table
-- ============================================
CREATE TABLE IF NOT EXISTS albums (
  id BIGSERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  icon TEXT DEFAULT '📷',
  subtitle TEXT,
  order_index INTEGER DEFAULT 0,
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for albums
CREATE INDEX IF NOT EXISTS idx_albums_published ON albums(published);
CREATE INDEX IF NOT EXISTS idx_albums_slug ON albums(slug);
CREATE INDEX IF NOT EXISTS idx_albums_order ON albums(order_index);

-- ============================================
-- 2. Create Photos Table
-- ============================================
CREATE TABLE IF NOT EXISTS photos (
  id BIGSERIAL PRIMARY KEY,
  album_id BIGINT NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
  file_path TEXT NOT NULL,
  caption TEXT,
  type TEXT DEFAULT 'image' CHECK (type IN ('image', 'video')),
  order_index INTEGER DEFAULT 0,
  category TEXT,  -- For travel album tabs (wyoming, colorado, japan, etc.)
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for photos
CREATE INDEX IF NOT EXISTS idx_photos_album ON photos(album_id);
CREATE INDEX IF NOT EXISTS idx_photos_published ON photos(published);
CREATE INDEX IF NOT EXISTS idx_photos_category ON photos(category);
CREATE INDEX IF NOT EXISTS idx_photos_order ON photos(album_id, order_index);

-- ============================================
-- 3. Insert Initial Albums
-- ============================================
INSERT INTO albums (slug, name, icon, subtitle, order_index, published) VALUES
('travel', 'Travel', '✈️', 'Exploring Philippines, USA, Japan, and many more', 1, TRUE),
('me', 'Me', '📷', 'Personal moments, graduation, and career milestones', 2, TRUE),
('sports', 'Sports', '🏐', 'Volleyball and athletic achievements', 3, FALSE)
ON CONFLICT (slug) DO NOTHING;

-- ============================================
-- 4. Insert Sample Photos (Travel - Wyoming)
-- ============================================
-- You'll need to upload these images to Supabase Storage first
-- Then update the file_path to match your storage bucket URLs

-- Example format:
-- INSERT INTO photos (album_id, file_path, caption, type, category, order_index, published) VALUES
-- ((SELECT id FROM albums WHERE slug = 'travel'), 'https://your-project.supabase.co/storage/v1/object/public/travel-photos/wyoming/image1.jpg', 'Caption here', 'image', 'wyoming', 1, TRUE);

-- ============================================
-- 5. Create Updated_at Trigger Function
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
-- 6. Enable Row Level Security (RLS)
-- ============================================
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read access to published albums
CREATE POLICY "Public albums are viewable by everyone"
ON albums FOR SELECT
USING (published = TRUE);

-- Policy: Allow public read access to published photos in published albums
CREATE POLICY "Public photos are viewable by everyone"
ON photos FOR SELECT
USING (
  published = TRUE
  AND EXISTS (
    SELECT 1 FROM albums
    WHERE albums.id = photos.album_id
    AND albums.published = TRUE
  )
);

-- Note: Add admin policies later for INSERT/UPDATE/DELETE operations
-- You'll need to create these after setting up authentication

-- ============================================
-- 7. Verify Installation
-- ============================================
-- Run these queries to verify:
-- SELECT * FROM albums;
-- SELECT * FROM photos;
