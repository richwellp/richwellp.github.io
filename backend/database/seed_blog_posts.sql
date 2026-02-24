-- Seed Blog Posts Data
-- This provides sample blog posts for demonstration
-- Run this AFTER running blog_schema.sql

-- ============================================
-- 1. Sample Published Blog Posts
-- ============================================

-- Sample Post 1: Technical Blog Post
INSERT INTO blog_posts (slug, title, content, excerpt, author, tags, published, published_at) VALUES
(
  'getting-started-with-vue-3',
  'Getting Started with Vue 3',
  E'# Getting Started with Vue 3\n\nVue 3 is the latest major version of Vue.js, bringing significant improvements in performance, TypeScript support, and composition API.\n\n## Why Vue 3?\n\nVue 3 introduces several key features:\n\n- **Composition API**: Better code organization and reusability\n- **Improved Performance**: Faster rendering and smaller bundle size\n- **Better TypeScript Support**: First-class TypeScript integration\n- **Fragments**: Multiple root elements in components\n\n## Getting Started\n\nInstall Vue 3 using npm:\n\n```bash\nnpm create vue@latest\ncd your-project\nnpm install\nnpm run dev\n```\n\n## Composition API Example\n\nHere''s a simple counter component:\n\n```vue\n<script setup>\nimport { ref } from ''vue''\n\nconst count = ref(0)\nconst increment = () => count.value++\n</script>\n\n<template>\n  <button @click="increment">Count: {{ count }}</button>\n</template>\n```\n\n## Conclusion\n\nVue 3 is a powerful framework for building modern web applications. Give it a try!',
  'Learn the basics of Vue 3 and its powerful new features including Composition API, improved performance, and better TypeScript support.',
  'Richwell Perez',
  ARRAY['vue', 'javascript', 'frontend'],
  TRUE,
  NOW() - INTERVAL '30 days'
);

-- Sample Post 2: Career/Experience Blog Post
INSERT INTO blog_posts (slug, title, content, excerpt, author, tags, published, published_at) VALUES
(
  'my-internship-experience-at-amazon',
  'My Internship Experience at Amazon',
  E'# My Internship Experience at Amazon\n\nThis summer, I had the incredible opportunity to work as a Software Development Engineer Intern at Amazon Web Services.\n\n## The Team\n\nI worked on the AWS Lambda team, focusing on improving cold start performance for containerized applications.\n\n## Key Projects\n\n### Project 1: Cold Start Optimization\n\nI developed a caching mechanism that reduced cold start times by 40%:\n\n- Analyzed existing cold start bottlenecks\n- Designed and implemented a multi-tier caching solution\n- Validated improvements with A/B testing\n\n### Project 2: Monitoring Dashboard\n\nBuilt an internal dashboard for tracking Lambda metrics:\n\n- React frontend with TypeScript\n- Python backend using Flask\n- Real-time data visualization\n\n## What I Learned\n\n1. **Scale Matters**: Designing for millions of requests per second\n2. **Code Reviews**: Importance of thorough code review process\n3. **Documentation**: Clear documentation is critical for team success\n\n## Advice for Future Interns\n\n- Ask questions early and often\n- Network with other interns and full-time employees\n- Take advantage of learning resources\n- Document your work and accomplishments\n\n## Conclusion\n\nThis internship was a transformative experience that taught me valuable skills in distributed systems, cloud computing, and professional software development.',
  'Reflecting on my summer internship at Amazon Web Services, working on AWS Lambda cold start optimization and building internal tools.',
  'Richwell Perez',
  ARRAY['career', 'internship', 'aws', 'cloud'],
  TRUE,
  NOW() - INTERVAL '15 days'
);

-- Sample Post 3: Tutorial/Guide
INSERT INTO blog_posts (slug, title, content, excerpt, author, tags, published, published_at) VALUES
(
  'building-rest-api-with-flask-and-supabase',
  'Building a REST API with Flask and Supabase',
  E'# Building a REST API with Flask and Supabase\n\nLearn how to build a production-ready REST API using Flask and Supabase as your database.\n\n## Prerequisites\n\n- Python 3.8+\n- Basic knowledge of Flask\n- Supabase account (free tier works fine)\n\n## Setup\n\nFirst, install the required packages:\n\n```bash\npip install flask supabase\n```\n\n## Project Structure\n\n```\nproject/\n├── api/\n│   ├── __init__.py\n│   ├── blog.py\n│   └── auth.py\n├── config.py\n└── requirements.txt\n```\n\n## Creating the Flask App\n\n```python\nfrom flask import Flask, Blueprint\nfrom supabase import create_client\nimport os\n\napp = Flask(__name__)\nsupabase = create_client(\n    os.environ.get(''SUPABASE_URL''),\n    os.environ.get(''SUPABASE_KEY'')\n)\n```\n\n## Building Endpoints\n\n### GET Endpoint\n\n```python\n@app.route(''/posts'', methods=[''GET''])\ndef list_posts():\n    result = supabase.table(''posts'')\\\n        .select(''*'')\\\n        .eq(''published'', True)\\\n        .execute()\n    return jsonify(result.data)\n```\n\n### POST Endpoint\n\n```python\n@app.route(''/posts'', methods=[''POST''])\ndef create_post():\n    data = request.json\n    result = supabase.table(''posts'')\\\n        .insert(data)\\\n        .execute()\n    return jsonify(result.data), 201\n```\n\n## Error Handling\n\nAlways implement proper error handling:\n\n```python\ntry:\n    result = supabase.table(''posts'').select(''*'').execute()\n    return jsonify(result.data)\nexcept Exception as e:\n    return jsonify(error=str(e)), 500\n```\n\n## Deployment\n\nDeploy to Vercel for free hosting:\n\n```bash\nvercel --prod\n```\n\n## Conclusion\n\nYou now have a fully functional REST API with Flask and Supabase!',
  'Step-by-step guide to building a REST API using Flask and Supabase, from setup to deployment.',
  'Richwell Perez',
  ARRAY['python', 'flask', 'supabase', 'backend', 'tutorial'],
  TRUE,
  NOW() - INTERVAL '7 days'
);

-- ============================================
-- 2. Sample Draft Blog Post
-- ============================================

-- Draft Post: Future Content
INSERT INTO blog_posts (slug, title, content, excerpt, author, tags, published, published_at) VALUES
(
  'advanced-typescript-patterns',
  'Advanced TypeScript Patterns',
  E'# Advanced TypeScript Patterns\n\n[DRAFT] This post covers advanced TypeScript patterns for building scalable applications.\n\n## Generic Constraints\n\nTODO: Add examples\n\n## Conditional Types\n\nTODO: Add examples\n\n## Mapped Types\n\nTODO: Add examples',
  'Exploring advanced TypeScript patterns including generic constraints, conditional types, and mapped types.',
  'Richwell Perez',
  ARRAY['typescript', 'javascript', 'advanced'],
  FALSE,
  NULL
);

-- ============================================
-- 3. Verify Seeded Data
-- ============================================
-- Run these queries to verify:

-- Count total posts
SELECT COUNT(*) AS total_posts FROM blog_posts;

-- Count published vs draft
SELECT
  CASE WHEN published THEN 'Published' ELSE 'Draft' END AS status,
  COUNT(*) AS count
FROM blog_posts
GROUP BY published;

-- View all posts with key fields
SELECT id, slug, title, tags, published, published_at, created_at
FROM blog_posts
ORDER BY COALESCE(published_at, created_at) DESC;

-- View posts by tag
SELECT slug, title, tags
FROM blog_posts
WHERE 'vue' = ANY(tags)
ORDER BY published_at DESC;
