-- Seed Albums and Photos Data (Supabase Storage Version)
-- This uses Supabase Storage URLs instead of local static files
-- Run this AFTER running albums_schema.sql

-- ============================================
-- 0. Seed Albums First
-- ============================================
INSERT INTO albums (slug, name, icon, subtitle, categories, order_index, published) VALUES
('travel', 'Travel', '✈️', 'Exploring the world', ARRAY['usa', 'philippines', 'japan']::TEXT[], 0, true),
('sports', 'Sports', '⚽', 'Athletic moments', NULL, 1, true),
('me', 'Me', '👤', 'Personal moments', NULL, 2, true)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    icon = EXCLUDED.icon,
    subtitle = EXCLUDED.subtitle,
    categories = EXCLUDED.categories,
    order_index = EXCLUDED.order_index,
    published = EXCLUDED.published;

-- ============================================
-- 1. Me Album Photos (Using Supabase Storage)
-- ============================================
-- After uploading photos to Supabase Storage bucket 'photos', add them here
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/graduation.jpg',
 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/headshot.jpg',
 'Professional headshot', 2)
ON CONFLICT DO NOTHING;

-- ============================================
-- 2. Travel Album Photos (Add after uploading)
-- ============================================
-- Example format:
-- INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
-- ((SELECT id FROM albums WHERE slug = 'travel'),
--  'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/wyoming.jpg',
--  'Wyoming (Medicine Bow)', 'usa', 1);

-- ============================================
-- 3. Sports Album Photos (Add after uploading)
-- ============================================
-- INSERT INTO photos (album_id, url, caption, order_index) VALUES
-- ((SELECT id FROM albums WHERE slug = 'sports'),
--  'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/sports/basketball.jpg',
--  'Basketball game', 1);

-- ============================================
-- NOTES
-- ============================================
-- 1. Upload photos to Supabase Storage first:
--    - Go to: https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/buckets
--    - Create folder structure in 'photos' bucket
--    - Upload your images
--    - Get public URL from Supabase UI
--
-- 2. File organization in bucket:
--    photos/
--    ├── me/
--    │   ├── graduation.jpg
--    │   └── headshot.jpg
--    ├── travel/
--    │   ├── usa/
--    │   ├── philippines/
--    │   └── japan/
--    └── sports/
--
-- 3. URL format:
--    https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/[path]
--
-- 4. Verify setup:
--    SELECT * FROM albums;
--    SELECT * FROM photos;
