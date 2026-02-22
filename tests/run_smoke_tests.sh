#!/bin/bash

echo "======================================"
echo "Running Smoke Tests"
echo "======================================"
echo ""

# Navigate to project root
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Run smoke tests with verbose output
echo "Step 1: Running all smoke tests..."
python -m pytest tests/test_smoke.py -v --tb=short

echo ""
echo "Step 2: Running with coverage..."
python -m pytest tests/test_smoke.py --cov=app --cov-report=term-missing

echo ""
echo "======================================"
echo "Smoke Tests Complete"
echo "======================================"