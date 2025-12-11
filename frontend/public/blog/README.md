# Blog System Documentation

## Overview

This blog system uses Markdown (.md) files for blog posts, making it easy to write and manage content without touching code.

## Directory Structure

```
public/blog/
├── README.md (this file)
└── 2025-12-11-building-my-portfolio-with-claude.md
```

## Creating a New Blog Post

### 1. File Naming Convention

Blog posts **must** follow this naming format:
```
YYYY-MM-DD-post-slug.md
```

Examples:
- `2025-01-15-getting-started-with-ai.md`
- `2025-03-20-my-journey-into-llms.md`
- `2024-12-11-reflections-on-2024.md`

**Important:**
- Date format: `YYYY-MM-DD` (4-digit year, 2-digit month, 2-digit day)
- Use hyphens (`-`) to separate words in the slug
- Use lowercase letters for the slug
- No spaces in filenames

### 2. Blog Post Format

Each markdown file should start with **front matter** (metadata) followed by your content:

```markdown
---
title: "My First Blog Post"
date: 2025-01-15
author: "Richwell Perez"
excerpt: "A brief description of what this post is about. This will show in the blog list."
tags: ["AI", "Machine Learning", "Career"]
---

# Your Blog Post Title

Your content starts here. You can use regular Markdown syntax:

## Subheadings

Write paragraphs, add **bold** and *italic* text.

### Code Blocks

\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

### Lists

- Item 1
- Item 2
- Item 3

### Links

[Link to Google](https://google.com)

### Images

![Alt text](/assets/photos/travel/california/photo.jpg)
```

### 3. Front Matter Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `title` | Yes | Post title | "Building RAG Systems" |
| `date` | Yes | Publication date (YYYY-MM-DD) | 2025-01-15 |
| `author` | No | Author name | "Richwell Perez" |
| `excerpt` | Yes | Brief summary (1-2 sentences) | "Learn how I built..." |
| `tags` | No | Category tags (array) | ["AI", "Tutorial"] |

## How Posts Are Sorted

Posts are automatically sorted by **date in descending order** (newest first) using the filename date.

**Sorting Logic:**
1. The system reads all `.md` files from `public/blog/`
2. Extracts the date from the filename (`YYYY-MM-DD` prefix)
3. Sorts posts by date, newest first
4. Displays them in the blog list

**Example Order:**
```
2025-03-20-newest-post.md       ← Shows first
2025-02-15-middle-post.md
2025-01-10-older-post.md
2024-12-25-oldest-post.md       ← Shows last
```

## Workflow for Adding a New Post

1. **Create the file** in `public/blog/` with the date format:
   ```bash
   touch public/blog/2025-03-20-my-new-post.md
   ```

2. **Add front matter** at the top:
   ```markdown
   ---
   title: "My New Post"
   date: 2025-03-20
   excerpt: "This is what my post is about."
   tags: ["AI", "Learning"]
   ---
   ```

3. **Write your content** using Markdown syntax

4. **Save the file**

5. **That's it!** The blog system automatically discovers new posts using Vite's `import.meta.glob`

The blog system will automatically:
- Discover all `.md` files in `public/blog/` at build time
- Parse the markdown file
- Extract front matter
- Convert markdown to HTML
- Sort by date (newest first)
- Display in the blog list

**No code changes required** - just add the markdown file and it will appear!

## Example Blog Posts

### Minimal Example
```markdown
---
title: "Hello World"
date: 2025-01-15
excerpt: "My first blog post!"
---

# Hello World

This is my first post. Welcome to my blog!
```

### Full Example
```markdown
---
title: "Building a RAG Chatbot from Scratch"
date: 2025-03-15
author: "Richwell Perez"
excerpt: "A deep dive into how I built a production RAG system serving 600+ users at Safran."
tags: ["AI", "LLMs", "RAG", "Tutorial"]
---

# Building a RAG Chatbot from Scratch

Last year, I built a full-stack RAG chatbot that now serves over 600 internal users at Safran...

## The Architecture

Here's how the system works:

\`\`\`python
from langchain import ChatOpenAI

def build_rag_pipeline():
    # Your code here
    pass
\`\`\`

## Lessons Learned

1. Performance optimization is crucial
2. Caching reduces latency significantly
3. User feedback drives improvements
```

## Tips

- **Keep filenames consistent**: Always use the `YYYY-MM-DD-slug.md` format
- **Write clear excerpts**: They help readers decide whether to read the full post
- **Use tags wisely**: 2-4 tags per post is ideal
- **Test locally**: Run `npm run dev` to preview before publishing
- **Proofread**: Check your markdown renders correctly

## Technical Details

The blog system uses:
- **Markdown parsing**: Converts `.md` files to HTML
- **Front matter extraction**: Parses YAML metadata
- **Date-based sorting**: Uses filename dates for chronological order
- **Vue Router**: Dynamic routing for individual blog posts

Posts are loaded at build time and rendered as static pages for optimal performance.

## Troubleshooting

**Post not showing up?**
- Check filename format: Must be `YYYY-MM-DD-slug.md`
- Verify front matter is valid YAML (proper quotes, colons, array brackets)
- Ensure the file is in `public/blog/` (not in a subdirectory)
- The file will be auto-discovered - no code changes needed!
- For local dev: The dev server should hot-reload automatically
- For production: Rebuild with `npm run build`

**Wrong sort order?**
- Check the date in your filename (not the front matter date)
- Use correct date format: `YYYY-MM-DD`

**Markdown not rendering?**
- Check for syntax errors in your markdown
- Ensure code blocks use triple backticks (\`\`\`)
- Test in a markdown previewer first
