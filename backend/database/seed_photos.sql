-- Seed Photos Data
-- This migrates existing photos from static files to database
-- Run this AFTER running albums_schema.sql

-- ============================================
-- 1. Travel Album Photos (USA)
-- ============================================
INSERT INTO photos (album_id, file_path, caption, type, category, order_index, published) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/wyoming/IMG_6023.JPG', 'Wyoming (Medicine Bow)', 'image', 'usa', 1, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/wyoming/personal.JPG', 'Me in Wyoming', 'image', 'usa', 2, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/IMG_4426.JPG', 'Colorado (Pikes Peak)', 'image', 'usa', 3, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/IMG_4430.JPG', 'Colorado (Pikes Peak)', 'image', 'usa', 4, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/colorado/personal_emlake.jpg', 'Colorado (Emerald Lake)', 'image', 'usa', 5, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/california/IMG_4551.JPG', 'La Jolla, California', 'image', 'usa', 6, TRUE);

-- ============================================
-- 2. Travel Album Photos (Philippines)
-- ============================================
INSERT INTO photos (album_id, file_path, caption, type, category, order_index, published) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/IMG_8348.jpg', 'Siargao (Cloud 9)', 'image', 'philippines', 1, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/IMG_8744.jpg', 'Flight to Siargao', 'image', 'philippines', 2, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/philippines/PXL_20230920_091946963.jpg', 'Coron (Mt. Tapyas)', 'image', 'philippines', 3, TRUE);

-- ============================================
-- 3. Travel Album Photos (Japan)
-- ============================================
INSERT INTO photos (album_id, file_path, caption, type, category, order_index, published) VALUES
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/japan/20240603_194332.jpg', 'Tokyo Tower', 'image', 'japan', 1, TRUE),
((SELECT id FROM albums WHERE slug = 'travel'), '/assets/photos/travel/japan/20240604_121505.jpg', 'Japan food', 'image', 'japan', 2, TRUE);

-- ============================================
-- 4. Me Album Photos (renamed from Professional)
-- ============================================
INSERT INTO photos (album_id, file_path, caption, type, category, order_index, published) VALUES
((SELECT id FROM albums WHERE slug = 'me'), '/assets/photos/professional/professional_0.jpg', 'Graduation day at UIUC', 'image', NULL, 1, TRUE),
((SELECT id FROM albums WHERE slug = 'me'), '/assets/photos/professional/professional_1.jpg', 'Professional headshot', 'image', NULL, 2, TRUE);

-- ============================================
-- 5. Verify Seeded Data
-- ============================================
-- Run these queries to verify:
SELECT
  a.name AS album,
  p.category,
  COUNT(*) AS photo_count
FROM photos p
JOIN albums a ON a.id = p.album_id
GROUP BY a.name, p.category
ORDER BY a.order_index, p.category;

-- View all photos:
-- SELECT a.name, p.caption, p.category, p.file_path FROM photos p JOIN albums a ON a.id = p.album_id ORDER BY a.name, p.category, p.order_index;
