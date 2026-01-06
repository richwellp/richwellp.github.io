## About This Portfolio

Welcome! This is a personal portfolio website showcasing professional experience, academic projects, and personal interests in my career.

### Site Structure

- **About Me** (`/`) - Personal introduction, education, professional journey, and interests
- **Experience** (`/experience`) - Work history and academic projects with collapsible cards
- **CV** (`/cv`) - Embedded PDF resume with download option
- **Misc** (`/misc`) - Hub for albums and blog
  - **Travel Album** (`/misc/travel`) - Travel photos by location (Wyoming, Colorado, etc.)
  - **Professional Album** (`/misc/professional`) - Work events and milestones
  - **Sports Album** (`/misc/sports`) - Volleyball and powerlifting content
  - **Blog** (`/misc/blog`) - Technical write-ups and personal reflections
  - **Blog Post** (`/misc/blog/:slug`) - Individual blog post view with markdown rendering

### Key Features

- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark/Light Theme**: Persistent theme switching with localStorage
- **Blog System**: Markdown-based blog with automatic post discovery using Vite's import.meta.glob
- **Photo & Video Albums**: Organized galleries with categories, lightbox viewer, and video support
- **Client-Side Routing**: Vue Router 4 with smooth navigation and scroll behavior
- **Embedded PDF Viewer**: Interactive resume display
- **Modern UI**: GitHub-inspired theme with CSS custom properties
- **Performance**: Optimized builds with code splitting and lazy loading
- **Contact Links**: SVG icons for email and LinkedIn in footer

### Project Dependencies

- **Vue 3** - Progressive JavaScript framework with Composition API
- **Vue Router 4** - Official routing library for SPA navigation
- **Vite 7** - Next-generation frontend build tool with fast HMR
- **Markdown-it** - Markdown parser for blog posts
- **Vite Plugin Vue DevTools** - Enhanced debugging experience

### Asset Management

Static assets are organized in `public/`:

**Photos and Videos:**
```
public/assets/photos/
├── travel/
│   ├── wyoming/
│   ├── colorado/
│   └── ...
├── professional/
└── sports/
```

**Blog Posts:**
```
public/blog/
├── README.md
└── YYYY-MM-DD-post-slug.md
```

**Resume:**
```
public/assets/Resume.pdf
```

**Adding New Content:**
- **Photos/Videos**: Add files to respective folders, update data files in `src/data/`
- **Blog Posts**: Create markdown file in `public/blog/` (automatically discovered)
- **Resume**: Replace `Resume.pdf` and rebuild

See `src/data/README.md` for detailed instructions on managing album content.

### Deployment

The site is deployed to GitHub Pages at [richwellp.github.io](https://richwellp.github.io).
