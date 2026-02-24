-- ============================================
-- Debug: Check Current Database State
-- ============================================

-- 1. Check all albums
SELECT id, slug, name, subtitle, categories, order_index, published, created_at
FROM albums
ORDER BY created_at;

-- 2. Check for duplicate albums
SELECT slug, COUNT(*) as count
FROM albums
GROUP BY slug
HAVING COUNT(*) > 1;

-- 3. Check all photos
SELECT p.id, a.slug as album, p.url, p.caption, p.category, p.order_index
FROM photos p
JOIN albums a ON p.album_id = a.id
ORDER BY a.slug, p.order_index;

-- 4. Count photos per album
SELECT a.slug, COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON a.id = p.album_id
GROUP BY a.slug
ORDER BY a.slug;

-- ============================================
-- Fix: Remove Duplicate Albums
-- ============================================

-- Find and keep only the OLDEST instance of each album
-- Delete newer duplicates
DELETE FROM albums
WHERE id NOT IN (
    SELECT MIN(id)
    FROM albums
    GROUP BY slug
);

-- Verify duplicates are gone
SELECT slug, COUNT(*) as count
FROM albums
GROUP BY slug
ORDER BY slug;

-- ============================================
-- Verify Final State
-- ============================================

-- Should show 3 albums, no duplicates
SELECT id, slug, name, published, order_index
FROM albums
ORDER BY order_index;
