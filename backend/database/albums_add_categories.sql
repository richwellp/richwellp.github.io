-- Add categories column to albums table
-- This allows albums like "Travel" to define photo categories (usa, philippines, japan)
-- Albums without categories (like "Me") can leave this NULL

ALTER TABLE albums ADD COLUMN IF NOT EXISTS categories TEXT[] DEFAULT NULL;

-- Update Travel album with existing categories
UPDATE albums
SET categories = ARRAY['usa', 'philippines', 'japan']::TEXT[]
WHERE slug = 'travel';

-- Me album has no categories (NULL is fine)
-- Sports album has no categories (NULL is fine)

-- Verify the update
SELECT slug, name, categories FROM albums;
