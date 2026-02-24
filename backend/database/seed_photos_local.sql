-- Seed Albums and Photos Data (Local Files Version)
-- This uses local static files from frontend/public/assets/photos/
-- Run this AFTER running reset_albums.sql (or the albums section only)

-- ============================================
-- 0. Seed Albums First (if not already done)
-- ============================================
INSERT INTO albums (slug, name, subtitle, categories, order_index, published) VALUES
('travel', 'Travel', 'Exploring the world', ARRAY['usa', 'philippines', 'japan']::TEXT[], 1, true),
('sports', 'Sports', 'Athletic moments', NULL, 2, true),
('me', 'Me', 'Personal moments', NULL, 3, true)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    subtitle = EXCLUDED.subtitle,
    categories = EXCLUDED.categories,
    order_index = EXCLUDED.order_index,
    published = EXCLUDED.published;

-- ============================================
-- 1. Me Album Photos (Local)
-- ============================================
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'),
 '/assets/photos/professional_0.jpg',
 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'),
 '/assets/photos/professional_1.jpg',
 'Professional headshot', 2)
ON CONFLICT DO NOTHING;

-- ============================================
-- 2. Travel Album Photos - USA
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/wyoming/IMG_6023.JPG',
 'Wyoming (Medicine Bow)', 'usa', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/wyoming/personal.JPG',
 'Me in Wyoming', 'usa', 2),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/colorado/IMG_4426.JPG',
 'Colorado (Pikes Peak)', 'usa', 3),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/colorado/IMG_4430.JPG',
 'Colorado (Pikes Peak)', 'usa', 4),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/colorado/personal_emlake.jpg',
 'Colorado (Emerald Lake)', 'usa', 5),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/california/IMG_4551.JPG',
 'La Jolla, California', 'usa', 6)
ON CONFLICT DO NOTHING;

-- ============================================
-- 3. Travel Album Photos - Philippines
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/philippines/IMG_8348.jpg',
 'Siargao (Cloud 9)', 'philippines', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/philippines/IMG_8744.jpg',
 'Flight to Siargao', 'philippines', 2),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/philippines/PXL_20230920_091946963.jpg',
 'Coron (Mt. Tapyas)', 'philippines', 3)
ON CONFLICT DO NOTHING;

-- ============================================
-- 4. Travel Album Photos - Japan
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/japan/20240603_194332.jpg',
 'Tokyo Tower', 'japan', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 '/assets/photos/travel/japan/20240604_121505.jpg',
 'Japan food', 'japan', 2)
ON CONFLICT DO NOTHING;

-- ============================================
-- 5. Sports Album Photos (Add your own)
-- ============================================
-- No sports photos seeded yet. Add them when you have some:
-- INSERT INTO photos (album_id, url, caption, order_index) VALUES
-- ((SELECT id FROM albums WHERE slug = 'sports'),
--  '/assets/photos/sports/basketball.jpg',
--  'Basketball game', 1);

-- ============================================
-- Verify Installation
-- ============================================
SELECT
    a.slug as album,
    COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON p.album_id = a.id
GROUP BY a.slug, a.order_index
ORDER BY a.order_index;

-- Should show:
-- travel: 11 photos
-- sports: 0 photos
-- me: 2 photos
