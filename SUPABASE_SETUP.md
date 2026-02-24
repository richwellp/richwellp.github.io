# Supabase Setup for File Uploads

## Get Your Supabase Anon Key

1. Go to your Supabase Dashboard:
   ```
   https://supabase.com/dashboard/project/cglrernscnxefiynhgvq/settings/api
   ```

2. Find the "**anon public**" key (NOT the service_role key)

3. Copy the key

4. Update `frontend/.env`:
   ```
   VITE_SUPABASE_ANON_KEY=YOUR_ANON_KEY_HERE
   ```
   Replace `YOUR_ANON_KEY_HERE` with the actual key you copied

## File Upload Feature

Once configured, you can upload files directly in the admin panel:

### How to Add Photos/Videos:

1. Go to `/admin/albums`
2. Click "Manage Photos" on any album
3. Click "+ Add Photo"
4. **Upload file** by clicking the upload area
5. Add caption, location, date, etc.
6. Click "Add"

### Supported Formats:

- **Images:** JPG, PNG, GIF, WEBP
- **Videos:** MP4, MOV, WEBM
- **Max Size:** 50MB per file

### Storage Structure:

Files are uploaded to Supabase Storage bucket "photos":
```
photos/
├── me/
│   ├── 1234567890-abc123.jpg
│   └── ...
├── travel/
│   ├── 1234567890-xyz789.mp4
│   └── ...
└── sports/
    └── ...
```

## How It Works:

1. **File Selection:** Choose file from your computer
2. **Auto Upload:** File uploads to Supabase Storage automatically
3. **URL Generation:** Public URL is generated and saved to database
4. **Display:** Photo/video appears in album viewer immediately

## Troubleshooting:

**"Upload failed"** error:
- Check that anon key is correct in `.env`
- Restart dev server: `npm run dev`
- Check Supabase Storage permissions (bucket should be public)

**Videos not playing:**
- Ensure video format is supported (MP4 recommended)
- Check file size is under 50MB
- Verify bucket is public in Supabase Dashboard

## Security Note:

The anon key is safe to use in the frontend - it has restricted permissions and can only:
- Read public data
- Upload to storage (with RLS policies)
- Insert/update data you've granted access to

The service_role key should NEVER be used in the frontend (it's in backend/.env only).
