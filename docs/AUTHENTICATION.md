# Authentication

## Overview

Admin authentication uses **Bearer tokens** stored in localStorage.

- **Frontend:** https://richwellp.github.io
- **Backend:** https://richwellp-github-io.vercel.app
- **Method:** Authorization header with Bearer token

## How It Works

1. User enters password at `/admin`
2. Frontend stores admin key in localStorage
3. Every admin request includes `Authorization: Bearer <key>` header
4. Backend validates key with `@require_admin` decorator
5. User stays logged in until explicit logout or localStorage clear

## Security Features

✅ **Timing-safe comparison** - Uses `secrets.compare_digest()` to prevent timing attacks
✅ **No session management** - Stateless authentication
✅ **Works cross-origin** - No third-party cookie restrictions
✅ **Simple implementation** - Standard Bearer token pattern
✅ **XSS protection** - All public content (blog posts, chatbot) sanitized with DOMPurify

**Note:** Solo admin site. Public-facing content is already sanitized against XSS.

## Endpoints

```
POST   /auth/login     Verifies admin key (frontend stores in localStorage)
POST   /auth/logout    No-op (frontend clears localStorage)
GET    /auth/status    Check authentication status
GET    /auth/verify    Verify authenticated (protected endpoint)
```

## Admin Routes

All admin routes require `Authorization: Bearer <key>` header:

```
GET    /admin/blog/posts              List all posts (including drafts)
GET    /admin/blog/posts/<slug>       Get single post (any status)
POST   /admin/blog/posts              Create post
PUT    /admin/blog/posts/<slug>       Update post
DELETE /admin/blog/posts/<slug>       Delete post

GET    /admin/albums                  List albums
POST   /admin/albums/<slug>/photos    Upload photos
PUT    /admin/photos/<id>             Update photo
DELETE /admin/photos/<id>             Delete photo
```

## Environment Variable

Set `BLOG_ADMIN_KEY` in Vercel:

1. Go to https://vercel.com/dashboard
2. Select project → Settings → Environment Variables
3. Add `BLOG_ADMIN_KEY` with your password
4. Redeploy

## Troubleshooting

**Login fails (401):**
- Check `BLOG_ADMIN_KEY` in Vercel matches your password
- Verify environment variable is set for production
- Check Network tab → Response → Should see error message

**Token not working after login:**
- Open DevTools → Application → Local Storage → `https://richwellp.github.io`
- Should see `admin_token` with your key
- If missing → Login didn't succeed
- If present → Check Network → Request Headers → Should see `Authorization: Bearer ...`

**Still getting 401 after login:**
- Clear localStorage: `localStorage.clear()` in console
- Try logging in again
- Check that admin key in Vercel is correct

## Code Reference

**Backend:** `backend/auth.py` - Authentication utilities (supports Bearer tokens)
**Frontend:** `frontend/src/composables/useAdminAuth.js` - Auth composable (localStorage + Bearer)
**Component:** `frontend/src/components/AdminAuthModal.vue` - Login modal

## Implementation Details

**Frontend token storage:**
```javascript
localStorage.setItem('admin_token', key)  // Store on login
localStorage.getItem('admin_token')       // Retrieve for requests
localStorage.removeItem('admin_token')    // Clear on logout
```

**Frontend request headers:**
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

**Backend validation (with timing-safe comparison):**
```python
auth = request.headers.get('Authorization', '')
if auth.startswith('Bearer '):
    token = auth[7:]
    if secrets.compare_digest(token, ADMIN_KEY):
        # Authenticated
```
