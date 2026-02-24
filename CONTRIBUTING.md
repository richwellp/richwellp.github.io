# Contributing to Portfolio Website

Thank you for considering contributing to this project! This guide will help you understand the development workflow and best practices.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/richwellp.github.io.git
   cd richwellp.github.io
   ```
3. **Set up development environment:**
   ```bash
   # Backend
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests

### 2. Make Your Changes

**Code Style:**
- **Python:** Follow PEP 8 guidelines
- **JavaScript/Vue:** Use ES6+ syntax, 2-space indentation
- **Comments:** Write clear comments for complex logic only
- **Functions:** Keep them small and focused (single responsibility)

**File Organization:**
- New components → `frontend/src/components/`
- New pages → `frontend/src/views/`
- New API endpoints → `backend/api/`
- Tests → Mirror the source file structure in `tests/`

### 3. Write Tests

**Every new feature or bug fix MUST include tests.**

```bash
# Backend tests
cd backend
python -m pytest tests/test_your_feature.py -v

# Frontend tests
cd frontend
npm test tests/unit/yourFeature.test.js
```

**Test Guidelines:**
- Test both success and error cases
- Use descriptive test names: `test_create_post_requires_admin_auth`
- Mock external dependencies (API calls, file system)
- Keep tests isolated (no shared state between tests)

### 4. Run All Tests

```bash
# Backend
cd backend && python -m pytest -v

# Frontend
cd frontend && npm test -- --run

# Both must pass before committing!
```

### 5. Commit Your Changes

**Commit Message Format:**

```
type: Short description (50 chars max)

Longer explanation if needed (wrap at 72 chars).
Explain WHAT and WHY, not HOW (code shows how).

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code restructuring (no functional change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build config)

**Examples:**

```bash
git commit -m "feat: Add dark mode toggle to navbar

Allows users to switch between light and dark themes.
Theme preference is saved to localStorage.

Closes #45"
```

```bash
git commit -m "fix: Resolve chatbot rate limit error

Changed rate limit from 5 to 10 messages per minute
to prevent false positives for legitimate users.

Fixes #78"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- Screenshots/GIFs for UI changes
- Checklist of what was tested

## Best Practices

### Code Quality

**DO:**
- ✅ Write self-documenting code (clear variable/function names)
- ✅ Keep functions small (< 50 lines)
- ✅ Use const/let instead of var
- ✅ Handle errors gracefully
- ✅ Add input validation
- ✅ Write tests for new code

**DON'T:**
- ❌ Leave console.log/print debugging statements (use for development only)
- ❌ Commit commented-out code
- ❌ Hard-code configuration values (use environment variables)
- ❌ Ignore linting warnings
- ❌ Push broken tests
- ❌ Commit large binary files

### Security

**NEVER commit:**
- API keys or passwords
- `.env` files
- Database credentials
- Private keys

**Always:**
- Validate user input (both frontend and backend)
- Use parameterized queries (prevent SQL injection)
- Sanitize data before rendering (prevent XSS)
- Implement rate limiting on API endpoints
- Keep dependencies updated

### Performance

**Frontend:**
- Lazy-load routes: `component: () => import('./views/Page.vue')`
- Use computed properties for derived data
- Avoid unnecessary re-renders (use v-once, v-memo when appropriate)
- Optimize images (WebP format, responsive sizes)

**Backend:**
- Cache expensive operations (database queries, API calls)
- Use pagination for large datasets
- Limit query results
- Index database columns used in WHERE clauses

### Accessibility

- Use semantic HTML (`<nav>`, `<main>`, `<article>`)
- Add alt text to images
- Ensure keyboard navigation works
- Use ARIA labels when needed
- Maintain color contrast ratios

## Testing Guidelines

### Unit Tests

Test individual functions/components in isolation.

**Backend Example:**
```python
def test_create_post_validates_title():
    """Post creation should reject empty titles."""
    response = client.post('/blog/posts', json={
        'title': '',  # Empty title
        'content': 'Some content'
    })
    assert response.status_code == 400
    assert 'title' in response.json['error'].lower()
```

**Frontend Example:**
```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatAssistant from './ChatAssistant.vue'

describe('ChatAssistant', () => {
  it('shows welcome message when opened', () => {
    const wrapper = mount(ChatAssistant)
    wrapper.find('.chat-toggle').trigger('click')
    expect(wrapper.text()).toContain('Hi! I\'m Richwell\'s virtual assistant')
  })
})
```

### Integration Tests

Test how components/endpoints work together.

### Test Coverage

Aim for:
- **80%+ code coverage** for new features
- **100% coverage** for critical paths (authentication, data validation, payments)

## Documentation

Update documentation when you:
- Add a new feature
- Change existing behavior
- Add environment variables
- Modify API endpoints
- Update dependencies

**Update:**
- `README.md` - User-facing changes
- Code comments - Complex logic only
- This file (`CONTRIBUTING.md`) - Development workflow changes

## Code Review

All contributions go through code review:
1. Automated tests must pass (GitHub Actions CI/CD)
2. Code reviewed by maintainer
3. Changes requested if needed
4. Approved and merged

**Review Checklist:**
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] Performance considered
- [ ] Security implications reviewed

## Questions or Problems?

- **Bug:** Open an issue with steps to reproduce
- **Feature Request:** Open an issue describing the feature and use case
- **Question:** Check README.md first, then open a discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
