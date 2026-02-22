# MLOps Assignment 2 - CI/CD Pipeline Guide

## Overview

This project includes a comprehensive Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions. The pipeline automates:

- ✅ Code quality checks (linting, formatting)
- 🔒 Security scanning
- 🧪 Automated testing (unit, integration, performance)
- 🐳 Docker image building and scanning
- 🚀 Automatic deployment to production
- 📊 Model retraining and monitoring

## Quick Start

### 1. Initialize Git Repository (if not already done)
```bash
cd bitsMtech_MLOps_Assignment_2
git init
git add .
git commit -m "Initial commit with CI/CD workflows"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bitsMtech_MLOps_Assignment_2.git
git push -u origin main
```

### 2. Run Local CI Tests
```bash
chmod +x run-local-ci-tests.sh
./run-local-ci-tests.sh
```

### 3. Configure GitHub Secrets (for deployment)
Go to GitHub repository → Settings → Secrets and variables → Actions:

```
DEPLOY_HOST        = your-server.example.com
DEPLOY_USER        = ubuntu
DEPLOY_KEY         = <your-ssh-private-key>
```

### 4. Push to GitHub
```bash
git push origin main
```

The workflows will automatically trigger!

---

## Pipeline Architecture

```
┌─────────────────┐
│   Git Push      │
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
    ▼          ▼
  CI        Docker Build
  Pipeline   & Push
    │          │
    └────┬─────┘
         │
    ┌────┴──────────────┐
    │                   │
    ▼                   ▼
 Approval         Health Check
    │                   │
    ├───────┬───────────┘
    │       │
    ▼       ▼
    CD  Rollback
 Deploy   (on failure)
    │
    ▼
 Production
```

## Workflow Files

| File | Purpose | Trigger |
|------|---------|---------|
| `ci.yml` | Code quality, testing, security | Push, PR |
| `docker-build.yml` | Build & push Docker images | Push to main, tags |
| `cd.yml` | Deploy to production | Push to main, workflow completion |
| `model-training.yml` | Retrain models | Weekly, manual trigger, code changes |
| `api-tests.yml` | Integration & performance tests | Push, PR, daily |
| `scheduled-checks.yml` | Dependency & security monitoring | Every 6 hours |

---

## Features

### 🧪 Testing
- Multi-version Python compatibility (3.9, 3.10)
- Code coverage reporting with Codecov
- Integration tests against live API
- Performance benchmarking
- Load testing with Locust

### 🔒 Security
- Bandit for code vulnerabilities
- Safety for dependency vulnerabilities
- Trivy for Docker image scanning
- pip-audit for dependency audits

### 📊 Code Quality
- Flake8 for style checking
- Black for code formatting
- isort for import sorting
- Pylint for code analysis
- Radon for complexity metrics

### 🐳 Docker
- Multi-stage builds for optimization
- Layer caching for faster builds
- Vulnerability scanning
- Automated registry push to GHCR

### 🚀 Deployment
- Blue-green style deployment
- Health checks with retries
- Automatic rollback on failure
- SSH-based secure deployment

### 🤖 ML Pipeline
- Weekly model retraining
- Model validation
- Metric logging with MLflow
- Automatic PR creation for new models

---

## Local Development

### Run Tests Locally
```bash
# Install dev dependencies
pip install -r requirements_fastapi.txt
pip install pytest pytest-cov flake8 black isort

# Run all tests
pytest tests/ -v --cov=app

# Check code quality
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
```

### Run with Docker Compose
```bash
# Build and start
docker-compose up --build

# Test API
curl http://localhost:8000/
curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" -d '{"features": [1.0, 2.0]}'

# Stop
docker-compose down
```

### Manual Model Training
```bash
pip install -r requirements.txt
jupyter nbconvert --to script modelTraining.ipynb --output train.py
python train.py
```

---

## Monitoring & Logs

### GitHub Actions
1. Go to repository → **Actions** tab
2. Select workflow to view run history
3. Click specific run to see logs
4. View artifacts from individual jobs

### Coverage Reports
- Uploaded to Codecov automatically
- Available as GitHub artifact
- Coverage badge can be added to README

### Security Scanning
- Bandit reports in artifacts
- Trivy results in GitHub Security tab (SARIF format)
- Dependency alerts in Security tab

---

## Troubleshooting

### Workflow Won't Start
- Push to main branch (not other branches initially)
- Check `.github/workflows/` files are committed
- Verify GitHub Actions is enabled in Settings

### Tests Failing in CI but Passing Locally
```bash
# Run in Python 3.9 or 3.10 (same as CI)
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements_fastapi.txt
pytest tests/
```

### Docker Build Fails
```bash
# Check Dockerfile syntax
docker build --no-cache .

# Check dependencies in requirements_fastapi.txt
pip install -r requirements_fastapi.txt
```

### Deployment Secrets Not Configured
```bash
# Generate SSH key for deployment
ssh-keygen -t rsa -b 4096 -f ~/.ssh/deploy_key -N ""

# Add to GitHub secrets:
# DEPLOY_KEY = contents of ~/.ssh/deploy_key (private key)
# DEPLOY_HOST = your.server.com
# DEPLOY_USER = ubuntu
```

---

## Customization

### Modify Test Triggers
Edit trigger conditions in workflow files:

```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'app/**'      # Only trigger on app changes
      - '!app/logs/**' # Exclude logs
```

### Change Scheduled Timings
```bash
# Cron syntax: minute hour day month day-of-week
# Examples:
0 2 * * 0   - Every Sunday at 2 AM
0 */6 * * * - Every 6 hours
0 9 * * 1-5 - Weekdays at 9 AM
```

### Add Slack/Email Notifications
```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Workflow failed!'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Best Practices

1. **Branch Protection Rules**
   - Require CI to pass before PR merge
   - Require code review
   - Dismiss approvals on new commits

2. **Keep Secrets Secure**
   - Use GitHub Secrets, not environment variables
   - Rotate deployment keys regularly
   - Use minimal permissions for service accounts

3. **Optimize Pipeline Performance**
   - Use caching for dependencies
   - Run jobs in parallel where possible
   - Remove unused steps

4. **Monitor Costs**
   - GitHub Actions has 2000 minutes/month free for public repos
   - Optimize build cache to reduce runs
   - Consider self-hosted runners for large projects

5. **Documentation**
   - Update WORKFLOWS.md when adding new workflows
   - Document secret requirements
   - Keep deployment guide current

---

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Docs](https://docs.docker.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pytest Docs](https://docs.pytest.org/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)

---

## Support

For issues or questions:
1. Check GitHub Actions logs
2. Review `.github/WORKFLOWS.md` documentation
3. Test locally with `run-local-ci-tests.sh`
4. Check application logs and error messages
