# Deployment Checklist

## Pre-Deployment

### ✅ Tests Passing
- [x] Backend: 46/46 tests passing
- [x] Frontend: 43/43 tests passing
- [x] All code committed and clean

### Database Setup (Run in Supabase SQL Editor)

**Step 1: Create Albums Schema**
```sql
-- Copy and run the entire contents of: backend/database/albums_schema.sql
```

**Step 2: Seed Albums**
```sql
-- Copy and run from: backend/database/seed_photos.sql (albums INSERT section)
```

**Step 3: Seed Photos (Optional)**
```sql
-- Copy and run from: backend/database/seed_photos.sql (photos INSERT section)
```

**Step 4: Verify Blog Schema Exists**
```sql
-- If blog_posts table doesn't exist, run: backend/database/blog_schema.sql
```

### Environment Variables Check

**Backend Environment (`backend/.env` or Vercel)**
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
BLOG_ADMIN_KEY=your_secure_admin_key_here
```

**Frontend Environment (`frontend/.env` or Vercel)**
```
VITE_API_URL=https://your-backend-url.vercel.app
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Deployment Steps

### 1. Push to GitHub
```bash
git push origin main
```

### 2. Deploy Backend (Vercel)
- Go to Vercel dashboard
- Select your backend project
- Add environment variables (SUPABASE_URL, SUPABASE_KEY, BLOG_ADMIN_KEY)
- Deploy from main branch
- Wait for deployment to complete
- Note the production URL

### 3. Deploy Frontend (Vercel)
- Go to Vercel dashboard
- Select your frontend project
- Update VITE_API_URL with backend production URL
- Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY
- Deploy from main branch
- Wait for deployment to complete

## Post-Deployment Testing

### Public Pages (No Auth Required)
- [ ] Home page (/) loads
- [ ] Experience page loads
- [ ] Projects page loads
- [ ] CV page loads
- [ ] Misc page loads
- [ ] Contact page works
- [ ] Albums page loads and displays albums
- [ ] Click each album (Travel, Sports, Me) - photos load
- [ ] Blog list page (/misc/blog) shows published posts
- [ ] Click a blog post - full post displays
- [ ] Chatbot icon visible and clickable
- [ ] Chatbot messages stream with animation
- [ ] Chatbot links are visible (bright blue color)

### Mobile Responsive Testing
- [ ] All pages display correctly on mobile
- [ ] Navigation works on mobile
- [ ] Albums grid adapts to mobile
- [ ] Blog posts readable on mobile
- [ ] Chatbot accessible on mobile
- [ ] Contact form works on mobile

### Admin Panel (Requires Auth)
- [ ] Navigate to /admin - auth modal appears
- [ ] Enter admin key - dashboard loads
- [ ] Dashboard shows correct stats (blog posts, albums, photos)
- [ ] Click "Manage Blog" - blog list loads
  - [ ] Can create new blog post
  - [ ] Can edit existing post
  - [ ] Can publish/unpublish post
  - [ ] Can delete post
- [ ] Click "Manage Albums" - albums list loads
  - [ ] Can create new album
  - [ ] Can edit album (name, icon, categories)
  - [ ] Can publish/unpublish album
  - [ ] Can delete album
- [ ] Click "Manage Photos" on an album
  - [ ] Photos grid displays
  - [ ] Can add new photo
  - [ ] Can edit photo (caption, location, date, category)
  - [ ] Can delete photo
  - [ ] Sort options work (order, date, category)

### Performance Check
- [ ] Images load efficiently
- [ ] No console errors in browser
- [ ] API responses are quick
- [ ] Chatbot streaming is smooth
- [ ] Page transitions are smooth

## Rollback Plan (If Issues Found)

1. Revert to previous deployment in Vercel
2. Check GitHub Actions for CI/CD errors
3. Review Vercel deployment logs
4. Check Supabase logs for database issues

## Success Criteria

✅ All public pages accessible
✅ All admin features working
✅ Mobile responsive
✅ No console errors
✅ Tests passing in CI/CD
✅ Database migrations applied

## Notes

- Admin key is required for /admin access
- Albums require database migration before they work
- Blog posts need to be published to appear publicly
- Photos require valid image URLs
- Supabase RLS policies allow public read access only
