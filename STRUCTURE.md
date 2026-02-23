# Project Structure

This document explains the organization of the richwellp.github.io monorepo.

## Overview

```
richwellp.github.io/
├── backend/           # Python/Flask API
├── frontend/          # Vue.js SPA
├── .github/           # CI/CD workflows
├── scripts/           # Build and deployment scripts
└── docs/              # Documentation (if needed)
```

## Backend Structure

```
backend/
├── api/               # API endpoints
│   ├── __init__.py
│   ├── index.py       # Main app entry
│   ├── blog.py        # Blog API routes
│   └── chat.py        # Chat API routes
├── tests/             # Backend tests (pytest)
│   ├── __init__.py
│   └── test_blog.py   # Blog API tests
├── config.py          # Configuration
├── requirements.txt   # Python dependencies
└── vercel.json        # Deployment config
```

**Testing:**
```bash
cd backend
python -m pytest tests/ -v
```

## Frontend Structure

```
frontend/
├── src/
│   ├── components/    # Vue components
│   ├── views/         # Page views
│   ├── composables/   # Composition API logic
│   ├── config/        # Configuration files
│   ├── data/          # Static data
│   └── router/        # Vue Router setup
├── tests/             # Frontend tests (Vitest)
│   └── unit/
│       └── composables/
│           └── useBlog.test.js
├── public/            # Static assets
├── package.json       # Node dependencies
└── vitest.config.js   # Test configuration
```

**Testing:**
```bash
cd frontend
npm test -- --run
```

## CI/CD

```
.github/
└── workflows/
    └── ci.yml         # Automated testing on push/PR
```

The CI pipeline runs:
1. Backend tests (Python 3.11)
2. Frontend tests (Node 20)
3. Frontend build verification

## File Organization Principles

### Tests Stay With Their Module
- **Backend tests** → `backend/tests/` (for Python import system)
- **Frontend tests** → `frontend/tests/` (for JS module resolution)

### Why Not Centralized?
A centralized `tests/` at root would:
- Break Python imports (requires PYTHONPATH hacks)
- Break JS imports (requires complex path rewrites)
- Complicate CI/CD workflows
- Reduce module independence

### Test File Naming
- **Backend:** `test_*.py` (pytest convention)
- **Frontend:** `*.test.js` or `*.spec.js` (Vitest convention)

## Adding New Tests

### Backend Test
```bash
# Create test file
touch backend/tests/test_newfeature.py

# Run specific test
cd backend
python -m pytest tests/test_newfeature.py -v
```

### Frontend Test
```bash
# Create test file
touch frontend/tests/unit/composables/useNewFeature.test.js

# Run specific test
cd frontend
npm test -- useNewFeature
```

## Running All Tests

```bash
# From backend
cd backend && python -m pytest tests/ -v

# From frontend
cd frontend && npm test -- --run

# CI runs both automatically on push
```

## Current Test Coverage

- **Backend:** 18 tests (blog API endpoints)
- **Frontend:** 11 tests (useBlog composable)
- **Total:** 29 tests

## Notes

- Each module (backend/frontend) is self-contained
- Tests can be run independently
- CI/CD verifies both modules on every push
- Structure follows industry best practices for monorepos
