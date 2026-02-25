-- Initial Album Setup
-- Run this AFTER running blog_schema.sql and albums_schema.sql
-- Creates the basic album structure without photos
-- Photos can be added via the admin panel at /admin

-- ============================================
-- Create Initial Albums
-- ============================================
INSERT INTO albums (slug, name, subtitle, categories, order_index, published) VALUES
('travel', 'Travel', 'Exploring the world', ARRAY['usa', 'philippines', 'japan']::TEXT[], 1, true),
('sports', 'Sports', 'Athletic moments', NULL, 2, true),
('me', 'Me', 'Personal moments', NULL, 3, true)
ON CONFLICT (slug) DO NOTHING;

-- ============================================
-- Verify Installation
-- ============================================
-- Check that albums were created:
-- SELECT id, slug, name, subtitle, published FROM albums ORDER BY order_index;
--
-- You should see 3 albums: travel, sports, me
-- Upload photos via the admin panel at /admin
