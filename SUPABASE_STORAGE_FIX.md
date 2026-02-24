# Fix Supabase Storage CORB Errors

## Problem
Photos load in `/admin` but not on public pages (`/misc/albums/me`).
Error: "Cross-Origin Read Blocking (CORB)"

## Root Cause
The Supabase Storage `photos` bucket is not public, so browsers block the image requests.

## Solution: Make Storage Bucket Public

### Step 1: Make Bucket Public
1. Go to: https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/buckets
2. Find the `photos` bucket
3. Click the three dots (•••) next to it
4. Select **"Edit bucket"** or **"Make public"**
5. Toggle **"Public bucket"** to ON
6. Save

### Step 2: Add Public Access Policy
1. Go to: https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/policies
2. Click **"New Policy"** for the `photos` bucket
3. Use template: **"Allow public read access"**
4. Or manually create policy:
   ```sql
   CREATE POLICY "Public read access"
   ON storage.objects FOR SELECT
   USING (bucket_id = 'photos');
   ```
5. Save policy

### Step 3: Verify
1. Open browser console on `/misc/albums/me`
2. Check Network tab - images should load with 200 status
3. No more CORB errors

## Why Admin Works But Public Doesn't
- Admin uses authenticated API calls (with Bearer token)
- Public pages load images directly from Storage URLs (no auth)
- Public URLs need bucket to be public

## After Fix
- Photos will load on all pages
- No authentication needed for viewing
- Upload still requires admin authentication
