-- ============================================
-- STEP 1: Drop Existing Tables
-- ============================================
-- This will delete all albums and photos data
DROP TABLE IF EXISTS photos CASCADE;
DROP TABLE IF EXISTS albums CASCADE;

-- ============================================
-- STEP 2: Create Albums Table (Without Icon)
-- ============================================
CREATE TABLE albums (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  subtitle TEXT,
  categories TEXT[] DEFAULT NULL,
  order_index INTEGER DEFAULT 0,
  published BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for albums
CREATE INDEX idx_albums_slug ON albums(slug);
CREATE INDEX idx_albums_order ON albums(order_index);
CREATE INDEX idx_albums_published ON albums(published);

-- ============================================
-- STEP 3: Create Photos Table
-- ============================================
CREATE TABLE photos (
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
CREATE INDEX idx_photos_album_id ON photos(album_id);
CREATE INDEX idx_photos_category ON photos(category);
CREATE INDEX idx_photos_date_taken ON photos(date_taken);
CREATE INDEX idx_photos_order ON photos(album_id, order_index);

-- ============================================
-- STEP 4: Create Updated_at Trigger Function
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to albums table
CREATE TRIGGER update_albums_updated_at
    BEFORE UPDATE ON albums
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to photos table
CREATE TRIGGER update_photos_updated_at
    BEFORE UPDATE ON photos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- STEP 5: Enable Row Level Security (RLS)
-- ============================================
ALTER TABLE albums ENABLE ROW LEVEL SECURITY;
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read access to all albums
CREATE POLICY "Public read access to albums"
ON albums FOR SELECT
USING (true);

-- Policy: Allow public read access to all photos
CREATE POLICY "Public read access to photos"
ON photos FOR SELECT
USING (true);

-- Note: Admin write operations use service_role key which bypasses RLS

-- ============================================
-- STEP 6: Seed Albums
-- ============================================
INSERT INTO albums (slug, name, subtitle, categories, order_index, published) VALUES
('travel', 'Travel', 'Exploring the world', ARRAY['usa', 'philippines', 'japan']::TEXT[], 1, true),
('sports', 'Sports', 'Athletic moments', NULL, 2, true),
('me', 'Me', 'Personal moments', NULL, 3, true);

-- ============================================
-- STEP 7: Seed Photos (Me Album Only)
-- ============================================
-- These URLs assume you've uploaded to Supabase Storage bucket 'photos'
-- Upload your photos first, then run this
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/graduation.jpg',
 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/headshot.jpg',
 'Professional headshot', 2);

-- ============================================
-- STEP 8: Verify Installation
-- ============================================
-- Check albums
SELECT id, slug, name, subtitle, categories, published FROM albums ORDER BY order_index;

-- Check photos
SELECT p.id, a.slug as album, p.url, p.caption, p.category, p.order_index
FROM photos p
JOIN albums a ON p.album_id = a.id
ORDER BY a.order_index, p.order_index;

-- ============================================
-- DONE!
-- ============================================
-- You should see:
-- - 3 albums (travel, sports, me)
-- - 2 photos in the 'me' album
