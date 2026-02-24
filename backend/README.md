# Backend Documentation

**⚠️ This README has been merged into the root-level documentation.**

Please see the main README at the repository root for complete documentation:

**[📖 View Complete Documentation](../README.md)**

## Quick Links

- **Backend Setup:** [../README.md#backend-setup](../README.md#backend-setup)
- **Database Setup:** [../README.md#backend-setup](../README.md#backend-setup)
- **API Endpoints:** See `api/blog.py` for blog endpoints
- **Deployment:** [../README.md#backend-vercel](../README.md#backend-vercel)
- **Testing:** [../README.md#-testing](../README.md#-testing)

## Quick Start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export BLOG_ADMIN_KEY="your-admin-key"
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export GEMINI_API_KEY="your-gemini-key"

# Run server
flask run
```

Visit `http://localhost:5000`


