-- Blog Posts Schema for Supabase
-- Run this in your Supabase SQL Editor

-- ============================================
-- 1. Create Blog Posts Table
-- ============================================
CREATE TABLE IF NOT EXISTS blog_posts (
  id BIGSERIAL PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  excerpt TEXT DEFAULT '',
  author TEXT DEFAULT 'Richwell Perez',
  tags TEXT[] DEFAULT '{}',
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for blog_posts
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published ON blog_posts(published);
CREATE INDEX IF NOT EXISTS idx_blog_posts_published_at ON blog_posts(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_blog_posts_tags ON blog_posts USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_blog_posts_created_at ON blog_posts(created_at DESC);

-- Full text search indexes for title and content
CREATE INDEX IF NOT EXISTS idx_blog_posts_title_search ON blog_posts USING GIN(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_blog_posts_content_search ON blog_posts USING GIN(to_tsvector('english', content));

-- ============================================
-- 2. Create Updated_at Trigger Function
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to blog_posts table
DROP TRIGGER IF EXISTS update_blog_posts_updated_at ON blog_posts;
CREATE TRIGGER update_blog_posts_updated_at
    BEFORE UPDATE ON blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 3. Auto-set published_at Trigger
-- ============================================
-- Automatically set/clear published_at when publish status changes
CREATE OR REPLACE FUNCTION set_published_at()
RETURNS TRIGGER AS $$
BEGIN
    -- If post is being published and published_at is not set
    IF NEW.published = TRUE AND (OLD.published = FALSE OR OLD.published IS NULL) AND NEW.published_at IS NULL THEN
        NEW.published_at = NOW();
    END IF;

    -- If post is being unpublished, clear published_at
    IF NEW.published = FALSE AND OLD.published = TRUE THEN
        NEW.published_at = NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to blog_posts table
DROP TRIGGER IF EXISTS set_published_at_trigger ON blog_posts;
CREATE TRIGGER set_published_at_trigger
    BEFORE UPDATE ON blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION set_published_at();

-- ============================================
-- 4. Enable Row Level Security (RLS)
-- ============================================
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read access to published posts
CREATE POLICY "Published posts are viewable by everyone"
ON blog_posts FOR SELECT
USING (published = TRUE);

-- Note: Add admin policies later for INSERT/UPDATE/DELETE operations
-- You'll need to create these after setting up authentication

-- ============================================
-- 5. Verify Installation
-- ============================================
-- Run these queries to verify:
-- SELECT id, slug, title, published, published_at FROM blog_posts ORDER BY created_at DESC;
-- SELECT COUNT(*) AS total_posts FROM blog_posts;
-- SELECT COUNT(*) AS published_posts FROM blog_posts WHERE published = TRUE;
