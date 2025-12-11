# .

This template should help get you started developing with Vue 3 in Vite.

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

## About This Portfolio

This is a personal portfolio website showcasing professional experience, academic projects, and personal interests in AI and software engineering.

### Site Structure

- **About me** (`/`) - Homepage featuring personal introduction, educational background, professional journey, and interests
- **Experience** (`/experience`) - Detailed work experience and academic projects in chronological order
- **CV** (`/cv`) - Embedded PDF viewer for downloadable resume
- **Misc** (`/misc`) - Gallery and miscellaneous content

### Key Features

- Fully responsive design optimized for desktop and mobile
- Vue Router for client-side navigation
- Embedded PDF viewer for resume
- Photo gallery for personal and professional images
- Contact information in footer (email and LinkedIn)
- Visitor tracking map integration
- Clean, modern UI with professional color scheme

### Project Dependencies

- Vue 3 - Progressive JavaScript framework
- Vue Router 4 - Official routing library
- Vite - Next-generation frontend tooling

### Asset Management

Static assets (photos, PDFs) are stored in `public/assets/`:
- `public/assets/photos/` - Personal and professional photographs
- `public/assets/Resume.pdf` - Current resume in PDF format

To update assets, replace files in the respective directories and rebuild the project.

### Deployment

The site is deployed to GitHub Pages at [richwellp.github.io](https://richwellp.github.io).

After making changes:
1. Build the production version: `npm run build`
2. Deploy the `dist/` folder to GitHub Pages
3. Ensure GitHub Pages is configured to serve from the correct branch/folder

### Development Workflow

1. Run the development server: `npm run dev`
2. Make changes to components in `src/`
3. View updates live at `http://localhost:5173`
4. Build for production when ready: `npm run build`
5. Test the production build: `npm run preview`
