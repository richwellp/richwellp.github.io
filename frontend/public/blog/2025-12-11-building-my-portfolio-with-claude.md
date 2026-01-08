---
title: "Building My Portfolio Website with Claude Code"
date: "2025-12-11"
author: "Richwell Perez"
excerpt: "I used Claude Code as my AI pair programmer and generated this blog."
tags: ["web development", "vue", "flask", "AI", "portfolio"]
---

# Building My Portfolio Website with Claude Code

When I decided to build my personal portfolio website on November 6, 2024, I wanted something more than just another template. I wanted a site that reflected my technical skills, showcased my work effectively, and gave me the flexibility to grow it over time. Today, I'm excited to share how I built [richwellp.github.io](https://richwellp.github.io) with the help of Claude Code.

## The Vision

As an AI Engineer at Safran, I work with cutting-edge technology every day—building RAG chatbots, predictive models, and full-stack applications. My portfolio needed to reflect this technical depth while remaining approachable and easy to navigate. I wanted:

- A clean, modern design with dark/light theme support
- Fast performance and responsive design
- Easy content management for future blog posts
- A backend architecture ready for future features
- Professional presentation of my experience and projects

## Tech Stack: Modern and Pragmatic

After considering various options, I landed on a stack that balanced simplicity with scalability:

### Frontend: Vue 3 + Vite
I chose **Vue 3** with the Composition API for its elegant reactivity system and gentle learning curve. **Vite** provides lightning-fast hot module replacement during development and produces optimized production builds. The combination feels modern without being overly complex.

Key architectural decisions:
- **Composables over Vuex/Pinia**: For a portfolio site, Vue's composables (`useTheme.js`, `useBlog.js`) provided all the state management I needed without additional dependencies
- **Vue Router 4**: Client-side routing with history mode for clean URLs
- **Path aliases**: Using `@` as an alias to `src/` keeps imports clean and refactorable
- **GitHub-inspired theme**: Custom CSS properties with `data-theme` attributes for seamless dark/light mode switching

### Backend: Flask + Vercel
While the portfolio is primarily static content, I wanted the architecture in place for future API-driven features. **Flask** gives me a lightweight Python backend that's easy to extend, and deploying to **Vercel** means serverless scalability without managing infrastructure.

The backend structure is simple but ready to grow:
```python
# backend/api/index.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://richwellp.github.io"])

@app.get("/")
def root():
    return jsonify(message="Hello from Flask on Vercel!")
```

### Content: Markdown with Gray Matter
Blog posts are stored as markdown files in `public/blog/` with frontmatter metadata. Using `gray-matter` and `markdown-it`, I can write posts in markdown and have them automatically parsed and rendered. The filename convention (`YYYY-MM-DD-slug.md`) keeps posts organized chronologically.

## Development Journey

### Phase 1: Foundation (Nov 6-7, 2024)
The first commits tell the story: starting with a fresh Vue project, setting up GitHub Actions for deployment, and configuring the basic structure. Claude Code helped me scaffold the project correctly from the start, avoiding common pitfalls with routing and deployment configuration.

### Phase 2: Backend Integration (Mid-November)
Restructuring to add the Flask backend required careful thought about deployment. With the frontend going to GitHub Pages and the backend to Vercel, CORS configuration and environment variables needed special attention. Claude Code helped me set up `vercel.json` rewrites and configure CORS properly:

```json
{
  "rewrites": [
    { "source": "/", "destination": "/api" },
    { "source": "/(.*)", "destination": "/api/$1" }
  ]
}
```

### Phase 3: Features and Polish (Late November - Early December)
This phase focused on the user experience:
- **Theming system**: Persistent dark/light mode using localStorage
- **Responsive navigation**: Hamburger menu for mobile devices
- **Content structure**: About, Experience, CV, and Misc sections
- **Album views**: Photo galleries for travel, professional, and sports photos
- **Blog infrastructure**: Markdown parsing and routing for future posts

### Phase 4: Documentation (December 11, 2024)
Today's session focused on making the codebase maintainable for future development. Claude Code analyzed the entire repository and created a comprehensive `CLAUDE.md` file—a guide for future instances of Claude Code (or any developer) to quickly understand the architecture, development commands, and important patterns.

## Working with Claude Code

Claude Code has been more than a code generator—it's been a thoughtful pair programmer. Here's what stood out:

### Context-Aware Suggestions
When I asked Claude to create documentation, it didn't just list files. It read through the codebase, understood the architectural patterns (composables, routing structure, theme system), and documented what actually matters for future development.

### Best Practices by Default
Claude consistently suggested modern patterns: using composables instead of Vuex, proper CORS configuration, responsive design considerations, and performance optimizations like strategic route-based code splitting (if needed in the future).

### Iterative Refinement
Rather than one-shot solutions, Claude would read existing code, understand the context, and make changes that fit the existing patterns. This maintained consistency across the codebase.

## Key Features Implemented

### 1. Theme System
A fully functional dark/light theme system using CSS custom properties:
```javascript
// frontend/src/composables/useTheme.js
export function useTheme() {
  const theme = ref('dark')

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    document.documentElement.setAttribute('data-theme', theme.value)
    localStorage.setItem('theme', theme.value)
  }

  return { theme, toggleTheme }
}
```

### 2. Collapsible Experience Cards
The Experience page features collapsible cards for work experience and projects, all starting expanded by default. This provides quick scanning while keeping the page length manageable.

### 3. Sticky Jump Navigation
A navigation bar that becomes sticky after scrolling, allowing quick jumps between Work Experience and Projects sections without losing context.

### 4. Blog System
A complete blog infrastructure ready for content:
- Markdown files with frontmatter metadata
- Dynamic routing (`/misc/blog/:slug`)
- Gray-matter parsing for metadata extraction
- Markdown-it for content rendering

### 5. Responsive Design
Every component is mobile-first, with careful attention to:
- Hamburger menu navigation on mobile
- Flexible grid layouts that adapt to screen size
- Touch-friendly interactive elements
- Proper spacing and typography scaling

## Deployment Strategy

### Frontend: GitHub Pages
The Vue application builds to a `dist/` folder and deploys to GitHub Pages. While I haven't set up automated GitHub Actions yet, the build process is straightforward:
```bash
cd frontend
npm run build
# Deploy dist/ to GitHub Pages
```

### Backend: Vercel
The Flask backend deploys to Vercel with a simple `vercel.json` configuration. Vercel's serverless functions handle routing automatically, making it a perfect fit for a lightweight API.

### Environment Variables
The frontend connects to the backend via `VITE_API_BASE`, making it easy to switch between local development and production:
```javascript
export const API = import.meta.env.VITE_API_BASE;
```

## Lessons Learned

### 1. Start with Architecture in Mind
Even for a "simple" portfolio, thinking about the architecture upfront paid dividends. Separating concerns (frontend/backend), using composables for state, and planning the routing structure made the project easier to extend.

### 2. Monorepo Benefits
Having both frontend and backend in one repository simplified development. I could iterate on both simultaneously and maintain a single source of truth for the project.

### 3. Documentation Matters
Creating `CLAUDE.md` today reminded me how quickly you forget architectural decisions. Documenting the "why" behind choices (like using composables instead of Vuex) helps future developers—including future me.

### 4. AI as a Thought Partner
Claude Code excelled when I treated it as a collaborator rather than a tool. Asking it to "analyze the codebase and create documentation" produced better results than "list all the files."

## What's Next?

The portfolio is live, but there's always room to grow:

- **GitHub Actions**: Automate the deployment process
- **Analytics**: Add visitor analytics to understand traffic
- **Blog Content**: Write more posts about AI engineering, projects, and technical deep-dives
- **Backend Features**: Leverage the Flask backend for dynamic features like a contact form or project showcase API
- **Performance**: Optimize image loading and implement lazy loading for galleries
- **SEO**: Add meta tags and improve search engine discoverability

## Try It Yourself

The beauty of modern web development is that tools like Vue, Vite, and Vercel make it incredibly accessible to build professional sites. Whether you're building a portfolio, a blog, or a full application, the stack I chose offers a great balance of simplicity and power.

And if you're curious about AI-assisted development, I encourage you to try Claude Code. It's transformed how I approach coding—from initial scaffolding to documentation, it's been an invaluable partner in this project.

---

**Questions or feedback?** Feel free to reach out via [email](mailto:richwell.perez@gmail.com) or [LinkedIn](https://www.linkedin.com/in/richwell-perez).
