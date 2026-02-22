# CI/CD Workflow Documentation

This directory contains GitHub Actions workflows that automate the build, test, and deployment processes for the MLOps Cat vs Dog Classification API.

## Workflows Overview

### 1. **CI Pipeline** (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests
**Purpose:** Continuous Integration - code quality, testing, and security checks

**Jobs:**
- **Lint and Test**
  - Tests Python 3.9 and 3.10 compatibility
  - Code quality checks with flake8
  - Code formatting validation with black
  - Import sorting check with isort
  - Unit tests with pytest and coverage reporting
  - Uploads coverage reports to Codecov

- **Security Scan**
  - Bandit for code security vulnerabilities
  - Safety for dependency vulnerability checks
  - Uploads security reports as artifacts

### 2. **Docker Build & Push** (`docker-build.yml`)
**Triggers:** Push to main, Tag creation, Pull Requests
**Purpose:** Build, test, and push Docker images to container registry

**Jobs:**
- **Build and Push**
  - Sets up Docker Buildx for multi-platform builds
  - Extracts metadata and generates appropriate tags
  - Builds Docker image and pushes to GHCR (GitHub Container Registry)
  - Tests Docker image locally
  - Uses GitHub Actions cache for faster builds

- **Scan Image**
  - Runs Trivy vulnerability scanning on Docker image
  - Uploads results to GitHub Security tab (SARIF format)

### 3. **CD Pipeline** (`cd.yml`)
**Triggers:** Push to main, Tag creation, Workflow completion
**Purpose:** Continuous Deployment - deploys to production

**Requirements:**
- `DEPLOY_KEY` - SSH private key for deployment server
- `DEPLOY_HOST` - Deployment server hostname/IP
- `DEPLOY_USER` - SSH user for deployment

**Jobs:**
- **Deploy**
  - Pulls latest Docker image
  - Stops old containers and starts new ones
  - Waits for container to be ready

- **Health Check**
  - Validates deployment with HTTP requests
  - Retries up to 5 times with 10s intervals

- **Rollback**
  - Automatically triggered on deployment failure
  - Reverts to previous deployment state
  - Sends notification on rollback

### 4. **Model Training Pipeline** (`model-training.yml`)
**Triggers:** Weekly schedule (Sunday 2 AM), Manual dispatch, Training notebook changes
**Purpose:** Automated model retraining and validation

**Jobs:**
- Converts and runs training notebook
- Logs metrics with MLflow
- Validates saved models can be loaded
- Uploads trained models as artifacts (30-day retention)
- Creates pull request with updated models
- Notifies on failure

### 5. **API Integration Tests** (`api-tests.yml`)
**Triggers:** Push, Pull Requests, Daily schedule (6 AM)
**Purpose:** Integration and performance testing

**Jobs:**
- **Integration Tests**
  - Runs complete deployment tests
  - Tests API endpoints
  - Performs load testing with Locust (10 users, 2/s ramp-up time)
  - Generates performance reports

- **Performance Tests**
  - Benchmarks endpoint response times
  - Memory profiling
  - Warns if response times exceed thresholds

### 6. **Scheduled Health Checks** (`scheduled-checks.yml`)
**Triggers:** Every 6 hours
**Purpose:** Continuous monitoring and dependency management

**Jobs:**
- **Dependency Check**
  - Checks for outdated packages
  - Detects known vulnerabilities
  - Validates dependency compatibility

- **Code Quality Scan**
  - Pylint analysis
  - Radon code complexity metrics

- **Docker Image Scan**
  - Trivy vulnerability scanning
  - Base image security checks

- **Coverage Trend**
  - Tracks test coverage over time
  - Comments coverage on PRs
  - Warns if coverage drops below 70%

---

## Setup Instructions

### 1. Prerequisites
- GitHub repository with Actions enabled
- Push access to repository
- (Optional) Container registry access (GHCR requires no setup for public repos)

### 2. Configure Secrets for CD Pipeline
Add these to your repository Settings → Secrets and variables → Actions:

```
DEPLOY_HOST=your-server.example.com
DEPLOY_USER=deployment-user
DEPLOY_KEY=<paste-your-ssh-private-key>
```

To generate SSH key for deployment:
```bash
ssh-keygen -t rsa -b 4096 -f deploy_key -N ""
# Upload deploy_key.pub to your server's ~/.ssh/authorized_keys
# Add deploy_key content to DEPLOY_KEY secret
```

### 3. (Optional) Codecov Integration
Add `CODECOV_TOKEN` secret for automatic coverage uploads

### 4. Update Docker Image References
Edit `docker-build.yml` and `cd.yml` if using a different registry (e.g., Docker Hub, ECR):

```yaml
REGISTRY: docker.io  # For Docker Hub
# or
REGISTRY: 123456789.dkr.ecr.us-east-1.amazonaws.com  # For ECR
```

---

## Local Development Workflow

### Run Tests Locally
```bash
# Install dependencies
pip install -r requirements_fastapi.txt
pip install pytest pytest-cov flake8 black isort

# Run all checks
pytest tests/ -v --cov=app
flake8 app/ tests/
black app/ tests/
isort app/ tests/
```

### Build and Run Docker Locally
```bash
# Build image
docker build -t mlops-classifier:latest .

# Run container
docker-compose up

# Run tests against container
python tests/testDeployment.py
```

### Test Model Training
```bash
# Convert and run training notebook
jupyter nbconvert --to script modelTraining.ipynb --output train_script.py
python train_script.py
```

---

## Monitoring and Troubleshooting

### View Workflow Status
1. Go to Repository → Actions tab
2. Click on specific workflow to see execution details
3. Each job shows logs and artifacts

### Common Issues

**Docker Push Fails:**
- Check GitHub Token permissions
- Verify `secrets.GITHUB_TOKEN` is available

**Deployment Fails:**
- Verify `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY` secrets
- Test SSH connection: `ssh -i deploy_key user@host`
- Check deployment server Docker/docker-compose setup

**Tests Fail Locally but Pass in CI:**
- Check Python version (CI tests 3.9 and 3.10)
- Verify all dependencies installed: `pip install -r requirements_fastapi.txt`
- Check file paths are absolute or relative correctly

**Slow Build Times:**
- Docker layer caching should improve on subsequent runs
- Consider splitting test jobs if they run serially

---

## Customization

### Modify Trigger Conditions
Edit the `on:` section in any workflow file:

```yaml
on:
  push:
    branches: [ main, develop ]
    paths:
      - 'app/**'  # Only trigger on app/ changes
  pull_request:
    branches: [ main ]
```

### Adjust Test Coverage Threshold
In `ci.yml`:
```yaml
--cov-fail-under=80  # Add this to pytest command
```

### Change Schedule Timings
Cron syntax: `minute hour day month day-of-week`

```yaml
schedule:
  - cron: '0 2 * * 0'  # Every Sunday at 2 AM UTC
  - cron: '0 */6 * * *'  # Every 6 hours
```

---

## Best Practices

1. **Keep workflows lean** - Combine related steps to reduce runtime
2. **Use caching** - GitHub Actions caches pip dependencies
3. **Secrets management** - Never commit secrets; use GitHub Secrets
4. **Branch protection** - Require CI to pass before merging
5. **Artifacts retention** - Set appropriate retention periods
6. **Monitoring** - Set up notifications for workflow failures
7. **Documentation** - Keep this file updated with workflow changes

---

## Environment Variables

Set in GitHub workflow files or in `docker-compose.yml`:

```yaml
API_TITLE: "Cat vs Dog Classifier API"
API_VERSION: "1.0.0"
DEBUG: "False"
LOG_LEVEL: "INFO"
MODEL_PATH: "artifacts/cnn_model.pt"
```

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Trivy Scanner](https://aquasecurity.github.io/trivy/)
- [Locust Load Testing](https://locust.io/)
