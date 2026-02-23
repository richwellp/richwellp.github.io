# .

This template should help get you started developing with Vue 3 in Vite.

## Requirements

**Node.js Version:** ^20.19.0 or >=22.12.0

You can check your Node.js version with:
```bash
node --version
```

To install or update Node.js, visit [nodejs.org](https://nodejs.org/)

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

There are two ways to deploy:

#### Option 1: Automated Deployment with GitHub Actions

GitHub Actions automatically builds and deploys the site whenever you push to the `main` branch.

**Initial Setup (One-time):**

1. The workflow file already exists at `.github/workflows/deploy.yml`

2. Configure GitHub Pages to use GitHub Actions:
   - Go to: `https://github.com/richwellp/richwellp.github.io/settings/pages`
   - Under **"Build and deployment"**, change **Source** to `GitHub Actions`
   - Click **Save**

**Deploying Changes:**

```bash
# Make your changes, then:
git add .
git commit -m "Your commit message"
git push origin main
```

That's it! GitHub Actions will:
- Install dependencies
- Build the project (`npm run build`)
- Deploy the `dist/` folder to GitHub Pages
- Your changes will be live in 1-2 minutes

**Monitoring Deployments:**

View deployment status at: `https://github.com/richwellp/richwellp.github.io/actions`

#### Option 2: Manual Deployment

If you prefer to deploy manually or GitHub Actions is not available:

**Using gh-pages (Recommended for manual deployment):**

1. Install gh-pages package:
   ```bash
   npm install --save-dev gh-pages
   ```

2. Add deploy script to `package.json`:
   ```json
   "scripts": {
     "deploy": "npm run build && gh-pages -d dist"
   }
   ```

3. Deploy:
   ```bash
   npm run deploy
   ```

4. Configure GitHub Pages:
   - Go to repository settings → Pages
   - Set source to `gh-pages` branch
   - Root directory: `/ (root)`

**Manual copy to gh-pages branch:**

1. Build the project:
   ```bash
   npm run build
   ```

2. The build output is in `dist/` folder

3. Copy contents to `gh-pages` branch:
   ```bash
   # From the repository root
   git checkout gh-pages
   cp -r frontend/dist/* .
   git add .
   git commit -m "Deploy update"
   git push origin gh-pages
   git checkout main
   ```

4. GitHub Pages will serve from the `gh-pages` branch

#### GitHub Actions Workflow Explained

The deployment workflow (`.github/workflows/deploy.yml`) contains two jobs:

**Build Job:**
```yaml
- Checkout code from repository
- Setup Node.js 20
- Install dependencies (npm ci)
- Build the project (npm run build)
- Upload the dist/ folder as artifact
```

**Deploy Job:**
```yaml
- Download the build artifact
- Deploy to GitHub Pages
- Provides deployment URL
```

**Key Features:**
- Triggers on push to `main` branch
- Can also be triggered manually from Actions tab
- Uses GitHub Pages deployment environment
- Caches npm dependencies for faster builds
- Only requires read/write permissions for Pages

**Troubleshooting GitHub Actions:**

If deployment fails:
1. Check the Actions tab for error logs
2. Verify `package-lock.json` is committed
3. Ensure all dependencies are in `package.json`
4. Check that build succeeds locally: `npm run build`
5. Verify GitHub Pages is configured to use GitHub Actions

#### Deployment Checklist

Before deploying, ensure:
- [ ] All tests pass
- [ ] Build completes without errors: `npm run build`
- [ ] Preview the build locally: `npm run preview`
- [ ] Check console for errors in the preview
- [ ] Verify all routes work correctly
- [ ] Test on mobile viewport
- [ ] Check that all assets load correctly (images, PDFs, etc.)

### Development Workflow

1. Run the development server: `npm run dev`
2. Make changes to components in `src/`
3. View updates live at `http://localhost:5173`
4. Build for production when ready: `npm run build`
5. Test the production build: `npm run preview`

---

## Maintenance Guide

### Project Structure Overview

```
frontend/
├── public/              # Static assets served directly
│   ├── assets/         # Images, PDFs, and other media
│   │   ├── photos/     # Photo albums (travel, professional, sports)
│   │   └── pdfs/       # Resume and other documents
│   └── favicon.ico     # Site icon
├── src/
│   ├── assets/         # Build-time assets
│   ├── components/     # Reusable Vue components
│   │   ├── AlbumViewer.vue      # Photo album display
│   │   ├── ChatAssistant.vue    # AI chat interface
│   │   ├── CommandPalette.vue   # Keyboard shortcuts
│   │   └── OptimizedImage.vue   # Image optimization wrapper
│   ├── composables/    # Reusable Vue composition functions
│   │   ├── useBlog.js          # Blog post management
│   │   ├── useTheme.js         # Theme switching logic
│   │   └── useStructuredData.js # SEO structured data
│   ├── router/         # Vue Router configuration
│   ├── views/          # Page components
│   │   ├── AboutMe.vue         # Homepage
│   │   ├── Experience.vue      # Work experience
│   │   ├── Projects.vue        # Project showcase
│   │   ├── CV.vue             # Resume viewer
│   │   ├── Contact.vue        # Contact form
│   │   ├── Misc.vue           # Miscellaneous content
│   │   ├── BlogList.vue       # Blog listing
│   │   ├── BlogPost.vue       # Individual blog posts
│   │   └── album views/       # Photo album pages
│   ├── data/           # Static data files
│   │   ├── blogPosts.json     # Blog post metadata
│   │   └── albums.json        # Photo album configurations
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── README.md           # This file
├── package.json        # Dependencies and scripts
└── vite.config.js      # Build configuration
```

### Adding Blog Posts

Blog posts are managed through `src/data/blogPosts.json` and markdown content.

**Step 1: Create the blog post file**

Create a new markdown file in `public/assets/blog/`:
```
public/assets/blog/my-new-post.md
```

**Step 2: Add metadata to blogPosts.json**

Edit `src/data/blogPosts.json`:
```json
{
  "slug": "my-new-post",
  "title": "My New Blog Post",
  "date": "2026-02-23",
  "excerpt": "A brief description of the post (2-3 sentences)",
  "tags": ["Vue.js", "WebDev", "Tutorial"],
  "readingTime": 5,
  "published": true
}
```

**Step 3: Test locally**
```bash
npm run dev
```
Navigate to `/misc/blog` to see your new post.

**Blog Post Markdown Tips:**
- Use `#` for main heading (H1)
- Use `##` for sections (H2)
- Use `###` for subsections (H3)
- Code blocks: triple backticks with language
- Images: `![Alt text](/assets/blog/images/image.png)`
- Links: `[Text](https://example.com)`

### Updating Professional Information

**Update About Me section:**
- Edit `src/views/AboutMe.vue`
- Modify the timeline in the `<script setup>` section for the animated subtitle
- Update the text content in the `<template>` section

**Update Experience page:**
- Edit `src/views/Experience.vue`
- Update the experiences array in the `<script setup>` section
- Add new job entries with title, company, dates, and description

**Update Projects:**
- Edit `src/views/Projects.vue`
- Update the projects array with new project details
- Include title, description, technologies, links, and images

**Update Resume/CV:**
- Replace `public/assets/pdfs/resume.pdf` with your updated resume
- Keep the same filename or update the path in `src/views/CV.vue`

### Adding and Optimizing Images

**Photo Album Images:**
1. Place images in appropriate directories:
   ```
   public/assets/photos/travel/
   public/assets/photos/professional/
   public/assets/photos/sports/
   ```

2. Update album configurations in component data:
   - Travel: `src/views/TravelAlbum.vue`
   - Professional: `src/views/ProfessionalAlbum.vue`
   - Sports: `src/views/SportsAlbum.vue`

3. Add new photos to the `photos` array:
   ```javascript
   {
     src: '/assets/photos/travel/new-photo.jpg',
     caption: 'Photo description',
     type: 'image' // or 'video'
   }
   ```

**Using OptimizedImage Component:**

The `OptimizedImage` component automatically handles:
- Lazy loading
- Responsive sizing
- Loading states
- Error handling

Usage in templates:
```vue
<OptimizedImage
  src="/assets/photos/path/to/image.jpg"
  alt="Description"
  size="md"           <!-- xs | sm | md | lg | full -->
  loading="lazy"      <!-- eager | lazy -->
  img-class="custom-class"
/>
```

**Image Size Guidelines:**
- **xs**: Small icons/thumbnails (< 100px)
- **sm**: Card thumbnails (200-400px)
- **md**: Standard content images (400-800px)
- **lg**: Hero images (800-1200px)
- **full**: Lightbox/fullscreen (original size)

**Image Optimization Tips:**
- Use WebP format when possible for better compression
- Keep images under 500KB for web performance
- Use descriptive filenames: `travel-tokyo-2024.jpg` not `IMG_1234.jpg`
- Always provide meaningful `alt` text for accessibility

### Quick Commands Reference

```bash
# Development
npm run dev          # Start dev server (http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build locally

# Deployment
git push origin main # Auto-deploy via GitHub Actions

# Testing
npm run test         # Run tests (if configured)

# Package Management
npm install          # Install dependencies
npm update           # Update dependencies
npm outdated         # Check for outdated packages
```

### Features Guide

**Theme Switching:**
- Toggle between light, dark, and auto modes
- Auto mode follows system preferences
- Persisted in localStorage

**Command Palette:**
- Press `Ctrl+K` (or `Cmd+K` on Mac) to open
- Quick navigation to any page
- Search functionality

**AI Chat Assistant:**
- Click the chat icon in bottom-right corner
- Ask questions about Richwell's experience, projects, or skills
- Powered by Claude API (requires API key configuration)

**SEO Features:**
- Structured data for rich snippets
- Dynamic meta tags per page
- Sitemap generation
- Social media preview tags

**Performance Features:**
- Lazy-loaded images
- Code splitting by route
- Optimized bundle size
- Service worker for caching (if enabled)

**Accessibility:**
- Keyboard navigation support
- ARIA labels and roles
- Color contrast compliance
- Screen reader friendly

---

## Troubleshooting

**Build Errors:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node.js version: `node --version`

**Images Not Loading:**
- Verify file paths start with `/assets/`
- Check file exists in `public/assets/`
- Clear browser cache
- Check browser console for 404 errors

**Styling Issues:**
- Verify CSS scoped vs global styles
- Check for conflicting CSS classes
- Test in incognito mode (no extensions)
- Use Vue DevTools to inspect components

**Deployment Issues:**
- Check GitHub Actions logs
- Verify `base` in `vite.config.js` matches repo name
- Ensure all files are committed
- Check GitHub Pages settings
