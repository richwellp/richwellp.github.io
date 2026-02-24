# Issues Found in Source Detection System

## Critical Issues

### 1. ❌ SKILLS Source Mapping Missing

**Problem:** The AI prompt contains a "TECHNICAL SKILLS" section, but there's no corresponding source in the SOURCE TRACKING instructions.

**Evidence:**
```python
# AI Prompt sections:
- NAME & CONTACT
- SUMMARY
- EDUCATION
- WORK EXPERIENCE
- TECHNICAL SKILLS  ← No source mapping!
- NOTABLE PROJECTS
- BLOG POSTS

# But SOURCE TRACKING only defines:
- "resume" = PDF resume content
- "profile" = personal info (name, summary, education)  ← doesn't mention skills
- "experience" = work experience
- "projects" = projects
- "blog" = blog posts
```

**Impact:**
- When AI cites TECHNICAL SKILLS section, it doesn't know which source to use
- Ambiguous whether skills belong to "profile" or "resume"
- User asks "What are your skills?" → Shows ALL sources (generic fallback)

**Fix Options:**
1. Add "skills" as 6th source (cleaner but more complex)
2. Update "profile" description to include skills: `"profile" = personal info (name, summary, education, skills)`
3. Update "resume" description to include skills (since PDF resume has skills section)

---

### 2. ❌ Skills Keyword Detection Missing

**Problem:** No 'skills' question type in keyword matching.

**Evidence:**
```python
question_types = {
    'blog': ...,
    'projects': ...,
    'experience': ...,
    'education': ...,
    'resume': ...,
    # 'skills' is missing!
}
```

**Impact:**
```
Q: "What are your skills?"
→ Shows: ['resume', 'profile', 'projects', 'blog'] (all sources)
Expected: Should show specific source(s) related to skills

Q: "What technologies do you know?"
→ Shows: all sources (generic fallback)
Expected: Should be more specific
```

**Fix:**
Add 'skills' question type with keywords:
```python
'skills': any(kw in message_lower for kw in [
    'skill', 'skills', 'technology', 'technologies', 'tech stack',
    'language', 'languages', 'framework', 'frameworks', 'tool', 'tools'
])
```

---

## Medium Issues

### 3. ⚠️ Incomplete Project Keyword Coverage

**Problem:** Common project-related terms are missing from keyword list.

**Evidence:**
```python
# Current keywords:
['project', 'built', 'created', 'developed', 'portfolio', 'github', 'code']

# Missing variations:
- 'coding' (only has 'code')
- 'build' (only has 'built')
- 'create' (only has 'created')
- 'develop' (only has 'developed')
- 'programming', 'programmed'
- 'engineer', 'engineering' (in project context)
- 'app', 'application'
- 'software'
```

**Impact:**
```
Q: "What coding work have you done?"
→ Current: ['resume', 'experience'] (misses projects!)
→ Expected: ['resume', 'experience', 'projects']

Reason: "coding" doesn't match "code", so projects not detected
```

**Fix:**
```python
'projects': any(kw in message_lower for kw in [
    'project', 'projects',
    'built', 'build', 'building',
    'created', 'create', 'creating',
    'developed', 'develop', 'developing',
    'portfolio', 'github', 'code', 'coding',
    'programming', 'programmed',
    'app', 'application', 'applications',
    'software', 'system', 'systems'
])
```

---

### 4. ⚠️ Incomplete Experience Keyword Coverage

**Problem:** Some work-related terms missing.

**Current:**
```python
['work', 'experience', 'job', 'company', 'employer', 'role', 'position', 'career']
```

**Missing:**
- 'worked', 'working'
- 'employment', 'employed'
- 'professional' (in context of experience)

**Fix:**
```python
'experience': any(kw in message_lower for kw in [
    'work', 'worked', 'working',
    'experience', 'experienced',
    'job', 'jobs',
    'company', 'companies',
    'employer', 'employment', 'employed',
    'role', 'roles',
    'position', 'positions',
    'career', 'professional experience'
])
```

---

## Minor Issues

### 5. ℹ️ AI Prompt SOURCE TRACKING Could Be Clearer

**Current:**
```
- Use "profile" if you used personal info (name, summary, education)
```

**Could be more explicit:**
```
- Use "profile" if you used personal info (name, email, location, summary, education, skills)
```

---

### 6. ℹ️ No Test for Skills Questions

**Current test coverage:**
- ✅ Blog questions
- ✅ Project questions
- ✅ Experience questions
- ✅ Education questions
- ✅ Resume questions
- ❌ Skills questions (missing)

**Add test:**
```python
def test_skills_questions():
    """Skills questions should show appropriate sources."""
    questions = [
        "What are your skills?",
        "What technologies do you know?",
        "Tell me your tech stack"
    ]
    # Should show specific source(s), not all sources
```

---

## Summary

| Issue | Severity | Impact | Fix Complexity |
|-------|----------|--------|----------------|
| Skills source mapping missing | 🔴 High | Ambiguous AI behavior | Medium |
| Skills keyword detection missing | 🔴 High | Shows all sources unnecessarily | Low |
| Incomplete project keywords | 🟡 Medium | Misses project questions | Low |
| Incomplete experience keywords | 🟡 Medium | Minor edge cases | Low |
| AI prompt clarity | 🟢 Low | Minor confusion | Low |
| Missing skills tests | 🟢 Low | Test coverage gap | Low |

---

## Recommended Fix Priority

### Phase 1: Critical Fixes (Do First)
1. **Add skills question type** to keyword matching
2. **Clarify skills mapping** in AI prompt (add to "profile" or "resume" description)
3. **Expand project keywords** to include common variations

### Phase 2: Enhancement (Do Second)
4. Expand experience keywords
5. Add skills question tests
6. Update documentation

### Phase 3: Optional
7. Consider adding "skills" as dedicated 6th source (if skills questions are common)

---

## Code Changes Needed

### File: `backend/api/gemini.py`

**1. Update keyword detection (line ~340):**
```python
question_types = {
    'blog': any(kw in message_lower for kw in [
        'blog', 'post', 'article', 'wrote', 'written', 'published'
    ]),
    'projects': any(kw in message_lower for kw in [
        'project', 'projects', 'built', 'build', 'building',
        'created', 'create', 'creating', 'developed', 'develop', 'developing',
        'portfolio', 'github', 'code', 'coding', 'programming', 'programmed',
        'app', 'application', 'software', 'system'
    ]),
    'experience': any(kw in message_lower for kw in [
        'work', 'worked', 'working', 'experience', 'experienced',
        'job', 'jobs', 'company', 'companies', 'employer', 'employment',
        'role', 'roles', 'position', 'positions', 'career'
    ]),
    'education': any(kw in message_lower for kw in [
        'education', 'degree', 'school', 'university', 'studied', 'study', 'major', 'college'
    ]),
    'resume': any(kw in message_lower for kw in [
        'resume', 'cv', 'qualification', 'certification'
    ]),
    'skills': any(kw in message_lower for kw in [  # NEW
        'skill', 'skills', 'technology', 'technologies', 'tech stack',
        'programming language', 'languages', 'framework', 'frameworks',
        'tool', 'tools', 'proficient', 'expertise'
    ])
}
```

**2. Add skills detection logic (line ~361):**
```python
# Single-topic questions
elif question_types['skills'] and sum(question_types.values()) == 1:
    if has_professional:
        sources = ['profile']  # Or ['resume'] depending on decision
```

**3. Update AI prompt SOURCE TRACKING (line ~168):**
```python
- Use "profile" if you used personal info (name, email, summary, education, skills)
```

### File: `backend/tests/test_gemini.py`

**Add skills test class:**
```python
def test_skills_questions_only():
    """Skills questions should show profile (or resume) source."""
    questions = [
        "What are your skills?",
        "What technologies do you know?",
        "Tell me your tech stack",
        "What programming languages do you use?"
    ]

    for question in questions:
        sources = determine_relevant_sources(question, FULL_CONTEXT)
        assert 'profile' in sources or 'resume' in sources
        assert len(sources) <= 2  # Should be specific, not all sources
```
