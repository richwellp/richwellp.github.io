# Adding Images & Videos to Blog Posts

## Quick Reference

### Images
```markdown
![Alt text](https://your-image-url.com/image.jpg)
```

### Videos (YouTube/Vimeo)
```markdown
[Watch Video: Title](https://youtube.com/watch?v=VIDEO_ID)
```

---

## Option 1: Upload to Supabase Storage (Recommended)

**Best for:** Images and videos you own/control

### Step 1: Create Blog Media Bucket

1. Go to Supabase Dashboard: https://app.supabase.com
2. Select your project
3. Click **Storage** in sidebar
4. Click **New bucket**
5. Name: `blog-media`
6. Public bucket: **Yes** ✅
7. Click **Create**

### Step 2: Upload Your Media

1. Click on `blog-media` bucket
2. Click **Upload file**
3. Select your image/video
4. Click **Upload**

### Step 3: Get Public URL

1. Click on the uploaded file
2. Click **Copy URL**
3. URL format: `https://PROJECT.supabase.co/storage/v1/object/public/blog-media/filename.jpg`

### Step 4: Use in Blog Post

**For images:**
```markdown
![My awesome image](https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/blog-media/my-image.jpg)
```

**For videos:**
Videos work the same way:
```markdown
![My video](https://cglrernscnxefiynhgvq.supabase.co/storage/v1/object/public/blog-media/my-video.mp4)
```

**Note:** Browsers will auto-detect video files and show video controls.

---

## Option 2: Use External Hosting

### Imgur (Images)

1. Go to https://imgur.com
2. Click **New post**
3. Upload image
4. Right-click image → **Copy image address**
5. Use in markdown:

```markdown
![Description](https://i.imgur.com/ABC123.jpg)
```

### YouTube (Videos)

1. Upload to YouTube
2. Copy video URL: `https://youtube.com/watch?v=ABC123`
3. Use as link in markdown:

```markdown
[Watch: My Video Tutorial](https://youtube.com/watch?v=ABC123)
```

Or embed thumbnail:
```markdown
[![Video Title](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtube.com/watch?v=VIDEO_ID)
```

### Cloudinary (Images/Videos)

1. Sign up: https://cloudinary.com (free tier)
2. Upload media
3. Copy public URL
4. Use in markdown

---

## Option 3: GitHub Repository (For Code Projects)

If your blog post is about a code project:

1. Add images to your project's GitHub repo: `/docs/images/`
2. Go to the raw image URL
3. Use in markdown:

```markdown
![Architecture diagram](https://raw.githubusercontent.com/username/repo/main/docs/images/diagram.png)
```

---

## Best Practices

### Image Optimization

**Before uploading:**
1. Resize to reasonable dimensions (max 1920px wide)
2. Compress images:
   - PNG: Use TinyPNG (https://tinypng.com)
   - JPG: Use JPEG Optimizer
3. Target: < 500KB per image

**Why?**
- Faster page loads
- Better SEO
- Lower storage costs

### Video Recommendations

**For short clips (< 30 seconds):**
- Upload to Supabase Storage as MP4
- Keep file size < 10MB

**For longer videos:**
- Use YouTube or Vimeo
- Link in blog post (don't embed full video)

### Alt Text Best Practices

Always include descriptive alt text:

```markdown
# ❌ Bad
![image](url.jpg)

# ✅ Good
![Bar chart showing 50% increase in user engagement after implementing dark mode](url.jpg)
```

**Why?**
- Accessibility for screen readers
- SEO benefits
- Shows if image fails to load

---

## Markdown Image Syntax Reference

### Basic Image
```markdown
![Alt text](https://example.com/image.jpg)
```

### Image with Title (hover text)
```markdown
![Alt text](https://example.com/image.jpg "Hover text")
```

### Linked Image (clickable)
```markdown
[![Alt text](https://example.com/thumb.jpg)](https://example.com/full-size.jpg)
```

### Image Gallery (Multiple Images)
```markdown
![Image 1](url1.jpg)
![Image 2](url2.jpg)
![Image 3](url3.jpg)
```

---

## Video in Blog Posts

### Important: HTML is Disabled

Your blog's markdown renderer has HTML disabled for security (`html: false` in markdown-it config).

**This means:**
- ❌ `<video>` tags won't work
- ❌ `<iframe>` embeds won't work
- ✅ Image syntax works (renders as `<img>`)
- ✅ Links work

### Solution 1: Link to Video
```markdown
**Watch the demo:** [View Video →](https://youtube.com/watch?v=ABC123)
```

### Solution 2: Video Thumbnail + Link
```markdown
[![Click to watch demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtube.com/watch?v=VIDEO_ID)
```

This creates a clickable thumbnail that opens YouTube.

### Solution 3: Upload MP4 to Supabase

Modern browsers detect MP4 files and render them with video controls:

```markdown
![Demo video](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/demo.mp4)
```

Browser will show:
- Video player with play/pause
- Volume controls
- Fullscreen button

---

## Example Blog Post with Media

```markdown
# My Awesome Project

In this post, I'll walk you through building a Vue 3 dashboard.

## Architecture Overview

Here's the system architecture:

![System architecture diagram showing frontend, backend, and database layers](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/architecture.png)

## Live Demo

Check out the live demo in action:

[![Demo video thumbnail](https://img.youtube.com/vi/ABC123/maxresdefault.jpg)](https://youtube.com/watch?v=ABC123)

## Key Features

The dashboard includes several key features:

![Dashboard screenshot showing dark mode interface](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/dashboard-dark.jpg)

![Dashboard screenshot showing light mode interface](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/dashboard-light.jpg)

## Performance Metrics

After optimization, we saw dramatic improvements:

![Performance graph showing 50% reduction in load time](https://PROJECT.supabase.co/storage/v1/object/public/blog-media/performance.png)

## Conclusion

Watch the full tutorial on YouTube: [Complete Vue 3 Dashboard Tutorial →](https://youtube.com/watch?v=XYZ789)
```

---

## Storage Limits

### Supabase Free Tier
- **Storage:** 1 GB
- **Bandwidth:** 2 GB/month
- **Good for:** 100-200 optimized images

### Recommendations
- Compress all images before upload
- Use external hosting (Imgur, YouTube) for large media
- Monitor usage in Supabase Dashboard

---

## Troubleshooting

### Image Not Showing

**Check:**
1. ✅ URL is public (not localhost or private)
2. ✅ File extension is correct (.jpg, .png, .gif, .mp4)
3. ✅ No typos in URL
4. ✅ Image exists (test URL in browser)

**Test:**
```markdown
![Test](https://via.placeholder.com/600x400?text=Test+Image)
```

If test image shows, your URL is wrong.

### Video Not Playing

**Check:**
1. ✅ File is MP4 format (most compatible)
2. ✅ File size < 10MB (large files may timeout)
3. ✅ URL is public
4. ✅ Browser supports video format

**Alternative:** Link to YouTube instead.

---

## Security Note

**Why HTML is disabled:**
- Prevents XSS attacks
- No `<script>` injection
- No malicious `<iframe>` embeds
- Safe user-generated content

**What works:**
- ✅ Images via markdown syntax
- ✅ Links via markdown syntax
- ✅ All standard markdown formatting

**What doesn't work:**
- ❌ `<video>` tags
- ❌ `<iframe>` embeds
- ❌ Custom HTML
- ❌ JavaScript

This is intentional for security.

---

## Quick Commands

**Create blog-media bucket (SQL):**
```sql
-- Run in Supabase SQL Editor
INSERT INTO storage.buckets (id, name, public)
VALUES ('blog-media', 'blog-media', true);
```

**Get all images in bucket:**
```sql
SELECT * FROM storage.objects WHERE bucket_id = 'blog-media';
```

---

**Need help?** Check the main [Technical Documentation](./TECHNICAL_DOCUMENTATION.md)
