#!/bin/bash
set -e

cd "$(dirname "$0")/.."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🔍 1. Running Ruff Linter & Formatter..."
ruff check .
ruff format --check . || echo "⚠️ Format check failed. Run 'ruff format .' to fix."

echo "🔍 2. Running Mypy Static Type Check..."
mypy kiwoom_rest kiwoom_playground

echo "🔍 3. Running Pytest..."
pytest test_app.py

echo "✅ All checks passed successfully!"
