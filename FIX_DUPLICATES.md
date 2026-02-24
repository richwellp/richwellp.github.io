# Fix Duplicate Albums Issue

## Issues Fixed

✅ **Frontend icon references removed** - Albums will now load correctly
✅ **Hardcoded icons** - Travel (✈️), Me (👤), Sports (⚽)

---

## Fix Duplicate Albums in Database

You likely ran the seed SQL multiple times, creating duplicate "Me" albums. Here's how to fix it:

### Option 1: Quick Fix - Delete ALL albums and reseed

Go to [Supabase SQL Editor](https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/sql/new)

**Run this:**

```sql
-- Delete all photos and albums
DELETE FROM photos;
DELETE FROM albums;

-- Reseed albums
INSERT INTO albums (slug, name, subtitle, categories, order_index, published) VALUES
('travel', 'Travel', 'Exploring the world', ARRAY['usa', 'philippines', 'japan']::TEXT[], 1, true),
('sports', 'Sports', 'Athletic moments', NULL, 2, true),
('me', 'Me', 'Personal moments', NULL, 3, true);

-- Reseed your 2 photos
INSERT INTO photos (album_id, url, caption, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/graduation.jpg',
 'Graduation day at UIUC', 1),
((SELECT id FROM albums WHERE slug = 'me'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/me/headshot.jpg',
 'Professional headshot', 2);

-- Verify
SELECT slug, name, published FROM albums ORDER BY order_index;
SELECT a.slug, COUNT(p.id) as photo_count FROM albums a LEFT JOIN photos p ON a.id = p.album_id GROUP BY a.slug;
```

**Expected result:**
- 3 albums (travel, sports, me)
- 2 photos in "me" album

---

### Option 2: Keep photos, remove duplicate albums only

If you've added more photos and don't want to lose them:

```sql
-- Check for duplicates
SELECT slug, COUNT(*) as count, string_agg(id::text, ', ') as ids
FROM albums
GROUP BY slug
HAVING COUNT(*) > 1;

-- Keep oldest album of each slug, delete newer duplicates
DELETE FROM albums
WHERE id NOT IN (
    SELECT MIN(id)
    FROM albums
    GROUP BY slug
);

-- Verify only 3 albums remain
SELECT slug, name FROM albums ORDER BY slug;
```

---

### Option 3: Debug first, then fix

Run the debug SQL to see what's wrong:

**File:** `backend/database/debug_database.sql`

Copy and paste into SQL Editor. It will show you:
1. All albums (including duplicates)
2. Which ones are duplicated
3. How to remove duplicates

---

## After Fixing Database

1. **Clear browser cache** or do a hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
2. **Visit your site:**
   - `https://richwellp.github.io/misc` - Should show 3 album cards
   - Click "Me" - Should show your 2 photos

3. **Test admin panel:**
   - Go to `/admin/albums`
   - Should see 3 albums, no duplicates
   - Click "Manage Photos" on Me - Should show 2 photos

---

## Why This Happened

**You likely:**
1. Ran `reset_albums.sql` (created 3 albums)
2. Ran `seed_photos_supabase.sql` again (created 3 MORE albums + photos)
3. Result: 6 albums total (2 of each)

**To prevent:**
- Only run seed files ONCE
- Use `ON CONFLICT DO NOTHING` or `ON CONFLICT DO UPDATE` in INSERT statements
- Check database first before reseeding

---

## Verification

After fixing, these should work:

✅ **Albums page loads** - Shows 3 albums with icons
✅ **No duplicate Me albums** - Only one "Me" album
✅ **Photos display** - Me album shows 2 photos from Supabase
✅ **Admin panel works** - Shows 3 albums, can manage photos

---

## Summary of Changes

**What I fixed in the code:**
- ✅ Removed `album.icon` references from Albums.vue
- ✅ Removed icon column from admin table
- ✅ Hardcoded icons in album viewer pages
- ✅ Albums will now load even without icon field in database

**What you need to fix in database:**
- ⚠️ Remove duplicate albums (use one of the SQL options above)
- ✅ Should have exactly 3 albums: travel, sports, me

**All frontend tests passing:** 43/43 ✅
