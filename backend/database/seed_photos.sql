-- Seed Albums and Photos Data
-- This migrates existing photos from static files to database
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
-- 1. Travel Album Photos (USA)
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/wyoming/IMG_6023.JPG', 'Wyoming (Medicine Bow)', 'usa', 1),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/wyoming/personal.JPG', 'Me in Wyoming', 'usa', 2),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/IMG_4426.JPG', 'Colorado (Pikes Peak)', 'usa', 3),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/IMG_4430.JPG', 'Colorado (Pikes Peak)', 'usa', 4),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/personal_emlake.jpg', 'Colorado (Emerald Lake)', 'usa', 5),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/california/IMG_4551.JPG', 'La Jolla, California', 'usa', 6);

-- ============================================
-- 2. Travel Album Photos (Philippines)
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/IMG_8348.jpg', 'Siargao (Cloud 9)', 'philippines', 1),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/IMG_8744.jpg', 'Flight to Siargao', 'philippines', 2),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/PXL_20230920_091946963.jpg', 'Coron (Mt. Tapyas)', 'philippines', 3);

-- ============================================
-- 3. Travel Album Photos (Japan)
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/japan/20240603_194332.jpg', 'Tokyo Tower', 'japan', 1),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/japan/20240604_121505.jpg', 'Japan food', 'japan', 2);

-- ============================================
-- 4. Sports Album Photos
-- ============================================
-- Add your sports photos here using the same pattern:
-- INSERT INTO photos (album_id, url, caption, order_index) VALUES
-- ((SELECT id FROM albums WHERE slug = 'sports'), '/assets/photos/sports/photo1.jpg', 'Caption', 1);

-- ============================================
-- 5. Me Album Photos (renamed from Professional)
-- ============================================
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'), '/assets/photos/professional/professional_0.jpg', 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'), '/assets/photos/professional/professional_1.jpg', 'Professional headshot', 2);

-- ============================================
-- 6. Verify Seeded Data
-- ============================================
-- Run these queries to verify:
SELECT
  a.name AS album,
  p.category,
  COUNT(*) AS photo_count
FROM photos p
JOIN albums a ON a.id = p.album_id
GROUP BY a.name, a.order_index, p.category
ORDER BY a.order_index, p.category;

-- View all photos:
-- SELECT a.name, p.caption, p.category, p.url FROM photos p JOIN albums a ON a.id = p.album_id ORDER BY a.name, p.category, p.order_index;
