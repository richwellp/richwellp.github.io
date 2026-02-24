# Working Independently - Developer Guide

This guide helps you maintain and develop your portfolio website without AI assistance.

---

## Quick Reference

### Essential Commands

```bash
# TESTING (run before every commit)
cd backend && python -m pytest -v          # Backend tests (50 tests)
cd frontend && npm test -- --run           # Frontend tests (47 tests)

# LOCAL DEVELOPMENT
cd backend && flask run                     # Backend: http://localhost:5000
cd frontend && npm run dev                  # Frontend: http://localhost:5173

# DEPLOYMENT
git add .
git commit -m "Your message"
git push origin main                        # Auto-deploys via Vercel

# CODE QUALITY
cd frontend && npm run lint                 # Check for code issues
cd frontend && npm run build                # Test production build
```

---

## Understanding Your Architecture

### Frontend (Vue 3)

**Key Pattern: Composables (Shared State)**
```javascript
// composables = reusable logic with shared state
import { useProfessionalInfo } from './composables/useProfessionalInfo'

const { projects, experience, loadProfessionalInfo } = useProfessionalInfo()
await loadProfessionalInfo()  // Loads once, shared everywhere
```

**File Organization:**
- `frontend/src/views/` - Page components (Experience.vue, Projects.vue, etc.)
- `frontend/src/components/` - Reusable UI pieces (ChatAssistant.vue, CommandPalette.vue)
- `frontend/src/composables/` - Shared logic (useBlog.js, useProfessionalInfo.js)
- `frontend/src/router/` - URL routing configuration
- `frontend/public/data/` - **YOUR CONTENT** (professionalInfo.json)

### Backend (Flask + Python)

**File Organization:**
- `backend/api/` - API endpoints (blog.py, albums.py, gemini.py)
- `backend/config.py` - Configuration settings
- `backend/tests/` - Test files

---

## Common Tasks Without AI

### 1. Update Your Professional Info

**File:** `frontend/public/data/professionalInfo.json`

```bash
# 1. Open the file
code frontend/public/data/professionalInfo.json

# 2. Edit the JSON (add job, project, skill, etc.)
# Use the examples already in the file as templates

# 3. Validate JSON syntax (catches typos)
cat frontend/public/data/professionalInfo.json | python -m json.tool

# 4. Test locally
cd frontend && npm run dev
# Visit http://localhost:5173 and verify changes

# 5. Deploy
git add frontend/public/data/professionalInfo.json
git commit -m "Update professional info"
git push origin main
```

### 2. Add a Blog Post

**Use the Admin Panel:**
1. Visit: https://richwellp.github.io/admin
2. Enter admin password (set in Vercel as `BLOG_ADMIN_KEY`)
3. Click "New Post"
4. Write in Markdown with live preview
5. Click "Publish"

**No code changes needed!**

### 3. Manage Photo Albums

**Use the Admin Panel:**
1. Visit: https://richwellp.github.io/admin
2. Go to "Albums" tab
3. Create album, upload photos/videos
4. Drag to reorder, set cover photo

**No code changes needed!**

### 4. Fix a Bug

**Step-by-step:**

```bash
# 1. Reproduce the bug locally
cd frontend && npm run dev     # Start frontend
cd backend && flask run        # Start backend (separate terminal)

# 2. Check browser console (F12) for errors
# Look for red error messages - they show file:line numbers

# 3. Find the file causing the error
# Example: "Error in ChatAssistant.vue:145"
# Open: frontend/src/components/ChatAssistant.vue, line 145

# 4. Make a small fix, test immediately
# Keep dev server running, changes auto-reload

# 5. Before committing, RUN TESTS
cd backend && python -m pytest -v
cd frontend && npm test -- --run

# 6. Only commit if all tests pass
git add .
git commit -m "Fix: description of what you fixed"
git push origin main
```

### 5. Add a New Page

**Example: Add "Testimonials" page**

```bash
# 1. Create the page component
# File: frontend/src/views/Testimonials.vue
```

```vue
<template>
  <div class="testimonials">
    <div class="container">
      <h1>Testimonials</h1>
      <p>What people say about working with me...</p>
      <!-- Your content here -->
    </div>
  </div>
</template>

<script setup>
// Your JavaScript here
</script>

<style scoped>
.testimonials {
  padding: 4rem 2rem;
}
/* Copy CSS patterns from other pages */
</style>
```

```bash
# 2. Add route
# File: frontend/src/router/index.js
# Copy an existing route and modify:
```

```javascript
{
  path: '/testimonials',
  name: 'Testimonials',
  component: () => import('../views/Testimonials.vue')
}
```

```bash
# 3. Add to navbar
# File: frontend/src/App.vue
# Find the <nav> section and add:
```

```vue
<RouterLink to="/testimonials">Testimonials</RouterLink>
```

```bash
# 4. Test locally
npm run dev
# Visit http://localhost:5173/testimonials

# 5. Deploy
git add .
git commit -m "Add testimonials page"
git push origin main
```

---

## Understanding the Tests

### Why Tests Matter

Tests are **safety nets** - they catch bugs before users see them.

**Example:**
```python
# This test ensures the chatbot rate limit works
def test_rate_limit_works():
    # Send 10 messages (the limit)
    for i in range(10):
        response = client.post('/chat', json={'message': 'test'})
        assert response.status_code == 200

    # 11th message should be rejected
    response = client.post('/chat', json={'message': 'test'})
    assert response.status_code == 429  # Too Many Requests
```

If this test fails after you make a change, you know you broke the rate limiter.

### Running Specific Tests

```bash
# Run one test file
cd backend && python -m pytest tests/test_blog.py -v

# Run one specific test
cd backend && python -m pytest tests/test_blog.py::test_list_posts -v

# Run with verbose output (shows print statements)
cd backend && python -m pytest -v -s

# Frontend: run specific test file
cd frontend && npm test tests/unit/useBlog.test.js
```

### Reading Test Failures

**Example failure:**
```
FAILED tests/test_blog.py::test_create_post - AssertionError: assert 500 == 201
```

**What it means:**
- Test: `test_create_post`
- File: `tests/test_blog.py`
- Problem: Expected status code 201 (Created), got 500 (Server Error)
- Action: Check the blog post creation logic in `backend/api/blog.py`

---

## Debugging Without AI

### 1. Use Print Statements

**Backend (Python):**
```python
def chat():
    user_message = request.get_json()['message']
    print(f"DEBUG: Received message: {user_message}")  # Add this

    response = call_gemini(user_message)
    print(f"DEBUG: Gemini response: {response}")       # Add this

    return jsonify(response=response)
```

**Frontend (JavaScript):**
```javascript
const sendMessage = async (input) => {
  console.log('DEBUG: Sending message:', input)  // Add this

  const response = await fetch('/chat', { ... })
  const data = await response.json()

  console.log('DEBUG: Received:', data)  // Add this
}
```

### 2. Browser DevTools (F12)

**Console Tab:** Shows JavaScript errors and your `console.log()` statements
**Network Tab:** Shows all API requests - click one to see request/response
**Elements Tab:** Inspect HTML/CSS to debug styling issues

### 3. Flask Debug Mode (Local Only)

```bash
# Shows detailed error pages with stack traces
export FLASK_DEBUG=1  # Linux/Mac
set FLASK_DEBUG=1     # Windows
flask run
```

---

## Learning Resources

### Vue 3 (Frontend Framework)
- Official Guide: https://vuejs.org/guide/
- Composition API: https://vuejs.org/guide/extras/composition-api-faq.html
- **Most useful:** Read other `.vue` files in your project as examples

### Flask (Backend Framework)
- Official Tutorial: https://flask.palletsprojects.com/tutorial/
- Quickstart: https://flask.palletsprojects.com/quickstart/

### Testing
- Pytest Guide: https://docs.pytest.org/en/stable/getting-started.html
- Vitest Guide: https://vitest.dev/guide/

### Git Basics
```bash
git status              # See what changed
git diff                # See exact changes
git log                 # See commit history
git checkout -b feat    # Create new branch
git reset --hard        # Undo all changes (DESTRUCTIVE)
```

---

## When Things Break

### Deployment Failed

**Check GitHub Actions:**
1. Go to: https://github.com/richwellp/richwellp.github.io/actions
2. Click the failed run
3. Look for red ❌ - shows which test failed

**Common causes:**
- Test failure (run tests locally first!)
- Syntax error in code
- Missing environment variable in Vercel

### Website Shows Old Content

```bash
# Hard refresh browser
# Windows: Ctrl + Shift + R
# Mac: Cmd + Shift + R

# Check Vercel deployment
# Visit: https://vercel.com/dashboard
# Look for latest deployment status
```

### Chatbot Not Working

```bash
# 1. Check API key is set in Vercel
# Go to: Project → Settings → Environment Variables
# Verify: GEMINI_API_KEY exists

# 2. Check browser console (F12)
# Look for errors mentioning /chat

# 3. Test backend directly
curl -X POST https://your-backend.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}'
```

### Tests Suddenly Failing

```bash
# 1. Did you change code? Undo and see if tests pass
git status              # See what you changed
git diff                # See exact changes
git checkout .          # UNDO ALL CHANGES (careful!)

# 2. Dependencies issue? Reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

cd backend
pip install -r requirements.txt --force-reinstall

# 3. Run tests again
cd backend && python -m pytest -v
cd frontend && npm test -- --run
```

---

## Project Structure Reference

```
richwellp.github.io/
├── frontend/
│   ├── public/
│   │   ├── data/
│   │   │   └── professionalInfo.json    ← EDIT THIS for content updates
│   │   └── assets/
│   │       └── Resume.pdf               ← Replace to update resume
│   ├── src/
│   │   ├── components/                  ← Reusable UI pieces
│   │   ├── composables/                 ← Shared logic
│   │   ├── views/                       ← Page components
│   │   ├── router/                      ← URL routing
│   │   ├── config/                      ← Contact info, API URLs
│   │   └── App.vue                      ← Main app, navbar, theme
│   └── tests/                           ← Frontend tests (47 tests)
│
├── backend/
│   ├── api/
│   │   ├── blog.py                      ← Blog endpoints
│   │   ├── albums.py                    ← Albums endpoints
│   │   ├── gemini.py                    ← AI chatbot logic
│   │   └── index.py                     ← Main Flask app, chat endpoints
│   ├── config.py                        ← Backend configuration
│   └── tests/                           ← Backend tests (50 tests)
│
├── .github/workflows/
│   └── ci-cd.yml                        ← Automated testing on push
│
├── README.md                            ← Quick start guide
├── MAINTENANCE_GUIDE.md                 ← Detailed maintenance docs
└── WORKING_INDEPENDENTLY.md             ← This file
```

---

## Making Changes Safely

**Golden Rule: TEST BEFORE DEPLOYING**

```bash
# Every single time, before git push:
cd backend && python -m pytest -v
cd frontend && npm test -- --run

# Both must show "passed" - no failures
# If tests fail, DON'T push - fix the issue first
```

**Why:**
- Failed tests mean broken functionality
- GitHub Actions will reject your deployment
- Users won't see broken features

---

## Getting Unstuck

### Strategy 1: Read Existing Code
Your codebase has examples of everything:
- Need to add a new API endpoint? Look at `backend/api/blog.py`
- Need to create a component? Look at `frontend/src/components/`
- Need to write a test? Look at existing tests in `tests/` folders

### Strategy 2: Start Small
Don't try to understand everything at once:
1. Find the file you need to change
2. Make ONE small change
3. Test it immediately
4. If it works, make another small change
5. Repeat

### Strategy 3: Use Documentation Comments
Most files have comments explaining what they do:
```javascript
// Load context (blog posts + professional info) once on first chat open
const loadContext = async () => {
  // ...
}
```

### Strategy 4: Search the Codebase
```bash
# Find where something is used
grep -r "useProfessionalInfo" frontend/src/

# Find a function definition
grep -r "def call_gemini" backend/

# Find a component
find . -name "*Chat*.vue"
```

---

## Emergency: Rollback Changes

**If you break something:**

```bash
# See recent commits
git log --oneline -10

# Rollback to previous commit (replace abc123 with commit hash)
git reset --hard abc123

# Force push (CAREFUL - overwrites remote)
git push origin main --force

# Vercel will auto-deploy the old working version
```

---

## Next Steps

1. **Practice making small changes**
   - Update professionalInfo.json
   - Change a color in App.vue
   - Add a blog post via admin panel

2. **Get comfortable with tests**
   - Run them after every change
   - Read the test files to understand what they check

3. **Bookmark these docs**
   - README.md - Quick reference
   - MAINTENANCE_GUIDE.md - Detailed guide
   - This file - Independent development

4. **Use version control**
   - Commit often with clear messages
   - Create branches for experiments: `git checkout -b experiment`
   - You can always undo: `git reset --hard`

---

## Summary

**You CAN maintain this website yourself:**
- 90% of updates = edit JSON, no coding
- Tests catch bugs automatically
- Everything is documented
- Start small, learn by doing

**When you need help:**
- Read existing code (best examples)
- Check error messages (they show file:line)
- Run tests (they tell you what broke)
- Google specific errors (copy/paste error message)

**You built this. You can maintain it. 💪**
