# Upload Photos to Supabase Storage

This guide shows you how to upload all your local photos to Supabase Storage and populate the database.

---

## Step 1: Create Folder Structure in Supabase

Go to [Supabase Storage](https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/buckets)

**If you haven't created the bucket yet:**
1. Click **"New bucket"**
2. Name: `photos`
3. **✅ Check "Public bucket"**
4. Click "Create"

**Create this folder structure:**
```
photos/
├── me/
├── travel/
│   ├── usa/
│   ├── philippines/
│   └── japan/
└── sports/
```

To create folders:
1. Click on `photos` bucket
2. Click "Create folder" → Name it (e.g., `me`, `travel`, etc.)
3. Go into each folder and create subfolders as needed

---

## Step 2: Upload Photos from Local Files

### Me Album (2 photos)
**From:** `frontend/public/assets/photos/`
**To:** `photos/me/` in Supabase

Upload and rename:
- `professional_0.jpg` → `graduation.jpg`
- `professional_1.jpg` → `headshot.jpg`

---

### Travel Album - USA (6 photos)
**From:** `frontend/public/assets/photos/travel/`
**To:** `photos/travel/usa/` in Supabase

Upload these files:
- `wyoming/IMG_6023.JPG` → `wyoming-medicine-bow.jpg`
- `wyoming/personal.JPG` → `wyoming-me.jpg`
- `colorado/IMG_4426.JPG` → `colorado-pikes-peak-1.jpg`
- `colorado/IMG_4430.JPG` → `colorado-pikes-peak-2.jpg`
- `colorado/personal_emlake.jpg` → `colorado-emerald-lake.jpg`
- `california/IMG_4551.JPG` → `california-la-jolla.jpg`

---

### Travel Album - Philippines (3 photos)
**From:** `frontend/public/assets/photos/travel/philippines/`
**To:** `photos/travel/philippines/` in Supabase

Upload and rename:
- `IMG_8348.jpg` → `siargao-cloud9.jpg`
- `IMG_8744.jpg` → `siargao-flight.jpg`
- `PXL_20230920_091946963.jpg` → `coron-mt-tapyas.jpg`

---

### Travel Album - Japan (2 photos)
**From:** `frontend/public/assets/photos/travel/japan/`
**To:** `photos/travel/japan/` in Supabase

Upload and rename:
- `20240603_194332.jpg` → `tokyo-tower.jpg`
- `20240604_121505.jpg` → `japan-food.jpg`

---

## Step 3: Run the Seed SQL

After uploading all photos, go to [Supabase SQL Editor](https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/sql/new)

**Copy and paste this SQL:**

```sql
-- ============================================
-- Clear existing photos (optional)
-- ============================================
-- DELETE FROM photos;

-- ============================================
-- Seed Albums
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
-- Me Album Photos
-- ============================================
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/graduation.jpg',
 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/headshot.jpg',
 'Professional headshot', 2);

-- ============================================
-- Travel Album - USA Photos
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/wyoming-medicine-bow.jpg',
 'Wyoming (Medicine Bow)', 'usa', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/wyoming-me.jpg',
 'Me in Wyoming', 'usa', 2),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/colorado-pikes-peak-1.jpg',
 'Colorado (Pikes Peak)', 'usa', 3),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/colorado-pikes-peak-2.jpg',
 'Colorado (Pikes Peak)', 'usa', 4),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/colorado-emerald-lake.jpg',
 'Colorado (Emerald Lake)', 'usa', 5),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/california-la-jolla.jpg',
 'La Jolla, California', 'usa', 6);

-- ============================================
-- Travel Album - Philippines Photos
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/philippines/siargao-cloud9.jpg',
 'Siargao (Cloud 9)', 'philippines', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/philippines/siargao-flight.jpg',
 'Flight to Siargao', 'philippines', 2),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/philippines/coron-mt-tapyas.jpg',
 'Coron (Mt. Tapyas)', 'philippines', 3);

-- ============================================
-- Travel Album - Japan Photos
-- ============================================
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/japan/tokyo-tower.jpg',
 'Tokyo Tower', 'japan', 1),
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/japan/japan-food.jpg',
 'Japan food', 'japan', 2);

-- ============================================
-- Verify
-- ============================================
SELECT
    a.slug as album,
    COUNT(p.id) as photo_count
FROM albums a
LEFT JOIN photos p ON p.album_id = a.id
GROUP BY a.slug, a.order_index
ORDER BY a.order_index;
```

**Expected result:**
- travel: 11 photos
- sports: 0 photos
- me: 2 photos

---

## Step 4: Test Your Site

Visit: `https://richwellp.github.io/misc`

**Check:**
- ✅ 3 album cards visible
- ✅ Click "Me" → 2 photos load from Supabase
- ✅ Click "Travel" → 11 photos grouped by USA, Philippines, Japan
- ✅ Click "Sports" → Empty (no photos yet)

---

## Quick Upload Tips

**Batch upload:**
1. You can select multiple files at once in Supabase Storage uploader
2. Rename them after upload by clicking the file → "Rename"

**Verify URLs work:**
- After uploading, click any file in Supabase Storage
- Copy the public URL
- Open it in a browser to verify it loads

---

## Summary

**Total photos to upload:**
- Me: 2 photos
- Travel/USA: 6 photos
- Travel/Philippines: 3 photos
- Travel/Japan: 2 photos
- **Total: 13 photos**

**Time estimate:** About 10-15 minutes for manual upload

**Benefits:**
- ✅ Photos served from CDN (fast worldwide)
- ✅ No repo bloat
- ✅ Scalable (add more photos easily)
- ✅ Local backups preserved in repo
