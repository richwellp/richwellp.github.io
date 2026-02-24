#!/bin/bash
# Quick test script to verify local setup

set -e  # Exit on error

echo "🧪 Testing Local Setup..."
echo ""

# Test backend
echo "1️⃣ Testing Backend..."
cd backend
if python -m pytest -v --tb=short; then
  echo "✅ Backend tests passed (46/46)"
else
  echo "❌ Backend tests failed"
  exit 1
fi
cd ..

# Test frontend
echo ""
echo "2️⃣ Testing Frontend..."
cd frontend
if npm test -- --run; then
  echo "✅ Frontend tests passed (43/43)"
else
  echo "❌ Frontend tests failed"
  exit 1
fi
cd ..

echo ""
echo "✅ All tests passed!"
echo ""
echo "📝 Next steps:"
echo "1. Run database migrations in Supabase (see docs/DEPLOYMENT.md)"
echo "2. Start backend: cd backend && flask run"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Visit http://localhost:5173"
