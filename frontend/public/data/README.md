# Dynamic Content for Chatbot

This folder contains JSON files that are loaded dynamically by the chatbot at runtime.

## How to Update Professional Info

**File:** `professionalInfo.json`

### Quick Update Process:

1. **Edit the JSON file** directly in this folder
2. **Commit and push** to GitHub:
   ```bash
   git add frontend/public/data/professionalInfo.json
   git commit -m "Update professional info"
   git push
   ```
3. **Vercel auto-deploys** (~2 minutes)
4. **Chatbot updates automatically** - no rebuild needed!

### What Gets Updated:

- ✅ Personal info (name, email, location, summary)
- ✅ Education history
- ✅ Work experience (add new jobs, update highlights)
- ✅ Projects (add/remove/update)
- ✅ Skills (languages, frameworks, tools)

### Important Notes:

- **No code rebuild required** - just edit JSON and push
- Changes take effect immediately after Vercel deployment
- Resume PDF still provides additional context to the AI
- Blog posts are fetched from Supabase database (fully dynamic)

### JSON Structure:

```json
{
  "personal": { ... },
  "education": [ ... ],
  "experience": [ ... ],
  "projects": [ ... ],
  "skills": { ... }
}
```

See the actual file for complete schema and examples.

### Testing Changes Locally:

1. Edit `professionalInfo.json`
2. Run frontend: `npm run dev`
3. Open chatbot and ask a question
4. Verify AI has your updated info

---

**Questions?** This is much easier than editing code files - just update JSON and push!
