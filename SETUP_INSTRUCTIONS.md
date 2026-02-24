# Database Setup Instructions

Follow these steps **in order** to set up your albums and photos database.

---

## Prerequisites

Before starting, upload your 2 photos to Supabase Storage:

### 1. Create Storage Bucket
1. Go to [Supabase Storage](https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/buckets)
2. Click **"New bucket"**
3. **Name:** `photos`
4. **✅ Check "Public bucket"** (very important!)
5. Click **"Create bucket"**

### 2. Upload Your Photos
1. Click on the `photos` bucket you just created
2. Click **"Create folder"** → Name it: `me`
3. Click into the `me` folder
4. Click **"Upload file"**
5. Upload these 2 files:
   - `frontend/public/assets/photos/professional_0.jpg` → **Rename to:** `graduation.jpg`
   - `frontend/public/assets/photos/professional_1.jpg` → **Rename to:** `headshot.jpg`

---

## Step 1: Reset Database

Go to [Supabase SQL Editor](https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/sql/new)

**Copy and paste the entire contents of this file:**
```
backend/database/reset_albums.sql
```

Click **"Run"** (or press Ctrl/Cmd + Enter)

**What this does:**
- ✅ Drops old albums and photos tables
- ✅ Creates new albums table (without icon column)
- ✅ Creates new photos table
- ✅ Sets up triggers and security policies
- ✅ Seeds 3 albums (Travel, Sports, Me)
- ✅ Seeds 2 photos in the Me album from Supabase Storage

**Expected output:**
```
DROP TABLE
DROP TABLE
CREATE TABLE
CREATE INDEX
...
INSERT 0 3
INSERT 0 2
```

---

## Step 2: Verify Setup

At the bottom of the SQL output, you should see:

### Albums Table (3 rows):
| slug   | name   | subtitle            |
|--------|--------|---------------------|
| travel | Travel | Exploring the world |
| sports | Sports | Athletic moments    |
| me     | Me     | Personal moments    |

### Photos Table (2 rows):
| album | url                                              | caption             |
|-------|--------------------------------------------------|---------------------|
| me    | https://...supabase.co/.../me/graduation.jpg     | Graduation day...   |
| me    | https://...supabase.co/.../me/headshot.jpg       | Professional...     |

---

## Step 3: Test Your Site

1. Visit your site: `https://richwellp.github.io/misc`
2. You should see 3 album cards: **Travel**, **Sports**, **Me**
3. Click on **"Me"** album
4. You should see your 2 photos loaded from Supabase!

---

## Step 4: Test Admin Panel

1. Visit: `https://richwellp.github.io/admin`
2. Enter your admin key
3. Go to **Albums Admin**
4. You should see all 3 albums
5. Click **"Manage Photos"** on the Me album
6. You should see your 2 photos

---

## Adding More Photos Later

### Via Admin Panel:
1. **First:** Upload photo to Supabase Storage
   - Go to Storage → photos bucket
   - Upload to appropriate folder (me, travel/usa, travel/japan, sports, etc.)
2. **Then:** Add via admin panel
   - Go to `/admin/albums`
   - Click "Manage Photos" on an album
   - Click "Add Photo"
   - Paste the Supabase Storage URL
   - Add caption, category (if needed)
   - Save

### Via SQL (Bulk):
```sql
INSERT INTO photos (album_id, url, caption, category, order_index) VALUES
((SELECT id FROM albums WHERE slug = 'travel'),
 'https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/photos/travel/usa/photo.jpg',
 'Photo caption', 'usa', 1);
```

---

## Troubleshooting

### Photos don't load?
- **Check:** Did you make the bucket public?
- **Check:** Can you access the URL directly in your browser?
- **Check:** Is the URL exactly as shown in Supabase Storage?

### "Album not found" error?
- **Check:** Did `reset_albums.sql` run successfully?
- **Verify:** Run `SELECT * FROM albums;` in SQL Editor

### Admin panel shows empty?
- **Check:** Are you using the correct admin key?
- **Check:** Did the seed queries run? Verify with `SELECT * FROM photos;`

---

## Clean Up (Optional)

After verifying everything works, you can delete the local photo files to keep your repo small:

```bash
rm frontend/public/assets/photos/professional_0.jpg
rm frontend/public/assets/photos/professional_1.jpg
```

Your photos are now served from Supabase Storage, not your repo!

---

## Summary

✅ Database reset complete
✅ 3 albums created (Travel, Sports, Me)
✅ 2 photos seeded in Me album
✅ Photos stored in Supabase Storage
✅ Admin panel ready to use
✅ Site live at https://richwellp.github.io

**Your photos are now in the cloud! 🎉**
