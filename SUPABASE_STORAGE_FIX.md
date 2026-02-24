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

### Step 2: Check/Add Public Access Policy

#### Option A: Via SQL Editor (RECOMMENDED)
1. Go to: https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/sql/new
2. Run this SQL to check existing policies:
   ```sql
   SELECT * FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage';
   ```
3. If no policy exists for SELECT on bucket 'photos', create one:
   ```sql
   CREATE POLICY "Allow public SELECT access to photos bucket"
   ON storage.objects
   FOR SELECT
   TO public
   USING (bucket_id = 'photos');
   ```
4. Verify the policy was created by running the SELECT query again

#### Option B: Via Storage Policies UI
1. Go to: https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/storage/policies
2. Look for existing policies on the `photos` bucket
3. If none exist, click **"New Policy"**
4. Choose **"For full customization"**
5. Fill in:
   - **Policy name**: `Allow public read access`
   - **Allowed operation**: SELECT (check only this)
   - **Target roles**: `public`
   - **USING expression**: `bucket_id = 'photos'`
6. Click **"Review"** then **"Save policy"**

#### Verify Policy Works
After creating the policy, test with this SQL:
```sql
-- This should return your photos
SELECT * FROM storage.objects WHERE bucket_id = 'photos' LIMIT 5;
```

### Step 3: Verify
1. Open browser console on `/misc/albums/me`
2. Check Network tab - images should load with 200 status
3. No more CORB errors

## Why Admin Works But Public Doesn't
- Admin uses authenticated API calls (with Bearer token)
- Public pages load images directly from Storage URLs (no auth)
- Public URLs need bucket to be public

## Troubleshooting

### Still Getting CORB Errors?

1. **Check if policy is active:**
   ```sql
   SELECT
     policyname,
     permissive,
     roles,
     cmd,
     qual
   FROM pg_policies
   WHERE tablename = 'objects'
     AND schemaname = 'storage'
     AND policyname LIKE '%photos%';
   ```

2. **Check bucket configuration:**
   ```sql
   SELECT id, name, public FROM storage.buckets WHERE name = 'photos';
   ```
   - The `public` column should be `true`

3. **Test a direct image URL:**
   - Get a photo URL from your database
   - Open it in an incognito browser window
   - If it loads → policy works
   - If it fails → policy needs fixing

4. **Check browser console:**
   - Look for the exact error message
   - CORB error = policy issue
   - 404 error = wrong URL
   - 403 error = bucket not public or policy missing

### Common Issues

**Issue: Policy exists but still blocked**
- Solution: Make sure `TO public` is in the policy
- The `public` role is what allows unauthenticated access

**Issue: Bucket shows as public but images don't load**
- Solution: Policy might be on wrong operation (INSERT instead of SELECT)
- Verify with: `SELECT cmd FROM pg_policies WHERE policyname LIKE '%photos%';`
- Should show: `{SELECT}` or `SELECT`

## After Fix
- Photos will load on all pages
- No authentication needed for viewing
- Upload still requires admin authentication
