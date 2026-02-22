#!/bin/bash
# Deploy script for local testing of CI/CD pipeline

set -e

echo "🚀 MLOps CI/CD Local Test Script"
echo "================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check Python version
echo -e "\n${YELLOW}1. Checking Python version...${NC}"
python --version || (echo -e "${RED}Python not found${NC}" && exit 1)

# Test 2: Create virtual environment (optional)
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}2. Creating virtual environment...${NC}"
    python -m venv venv
    source venv/bin/activate
else
    source venv/bin/activate
fi

# Test 3: Install dependencies
echo -e "\n${YELLOW}3. Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements_fastapi.txt
pip install pytest pytest-cov flake8 black isort bandit safety

# Test 4: Lint checks
echo -e "\n${YELLOW}4. Running lint checks...${NC}"
echo "   - flake8..."
flake8 app/ tests/ --count --exit-zero --max-line-length=127 || true

echo "   - black..."
black --check app/ tests/ || true

echo "   - isort..."
isort --check-only app/ tests/ || true

# Test 5: Security checks
echo -e "\n${YELLOW}5. Running security checks...${NC}"
echo "   - bandit..."
bandit -r app/ -f txt || true

echo "   - safety..."
safety check || true

# Test 6: Run unit tests
echo -e "\n${YELLOW}6. Running unit tests...${NC}"
pytest tests/ -v --cov=app --cov-report=term-missing || true

# Test 7: Docker build
echo -e "\n${YELLOW}7. Building Docker image...${NC}"
docker build -t mlops-classifier:test .

# Test 8: Docker test
echo -e "\n${YELLOW}8. Testing Docker image...${NC}"
docker run --rm mlops-classifier:test python -c "from app.main import app; print('✓ App imported successfully')"

# Test 9: Application startup
echo -e "\n${YELLOW}9. Testing application startup...${NC}"
timeout 10 python -m app.main &
sleep 3
curl -s http://localhost:8000/ || true
pkill -f "python -m app.main" || true

echo -e "\n${GREEN}✅ All local tests completed!${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Review linting output and fix issues"
echo "2. Ensure all tests pass"
echo "3. Commit changes and push to GitHub"
echo "4. Check GitHub Actions for automated pipeline"
