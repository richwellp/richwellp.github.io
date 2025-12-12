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
