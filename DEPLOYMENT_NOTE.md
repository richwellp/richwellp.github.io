# Deployment Note - Database Seeding Required

## 🔴 Action Required: Run Database Seeds

### Issue: Blog Dates Showing "Recent" or Empty

If you're seeing "Recent" instead of actual dates on the blog section at `/misc`, it means the blog posts haven't been seeded in your database yet.

### Solution: Run Blog Seed Script

Open your **Supabase SQL Editor** and run:

```sql
-- Copy and paste: backend/database/seed_blog_posts.sql
```

This will create 4 sample blog posts:
- ✅ "Getting Started with Vue 3" (30 days ago)
- ✅ "My Internship Experience at Amazon" (15 days ago)
- ✅ "Building a REST API with Flask and Supabase" (7 days ago)
- ✅ "Advanced TypeScript Patterns" (Draft, not shown publicly)

### Verify It Worked

After running the seed script, check:

```sql
-- Should return 4 posts
SELECT COUNT(*) FROM blog_posts;

-- Should return 3 published, 1 draft
SELECT published, COUNT(*) FROM blog_posts GROUP BY published;
```

Then refresh your site at `/misc` - you should now see blog posts with proper dates!

---

## ✅ What's Already Fixed

1. **Album name updated** - "Professional" → "Me" ✓
2. **Album icon updated** - 💼 → 👤 ✓
3. **Date fallback** - Shows "Recent" instead of "Invalid date" ✓

## 📋 Complete Database Setup Checklist

Make sure you've run ALL these scripts in Supabase SQL Editor:

- [ ] `backend/database/albums_schema.sql` - Creates albums and photos tables
- [ ] `backend/database/seed_photos.sql` - Seeds 3 albums with photos
- [ ] `backend/database/blog_schema.sql` - Creates blog_posts table (if not exists)
- [ ] `backend/database/seed_blog_posts.sql` - Seeds 4 sample blog posts ⬅️ **Do this now!**

## 🚀 After Seeding

Once all seeds are run:
1. Visit `/misc` - blog section should show 3 posts with dates
2. Visit `/misc/blog` - full blog list with all posts
3. Click any post - full content should display
4. Visit `/admin` - you can manage all posts

---

**TL;DR:** Run `backend/database/seed_blog_posts.sql` in Supabase to fix the date issue!
