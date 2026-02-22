# 🚀 CI/CD Automated Workflow - Complete Setup

## Overview
A comprehensive, production-ready CI/CD pipeline has been configured for your MLOps Cat vs Dog Classifier project using GitHub Actions.

---

## 📁 All Created Files

### GitHub Workflows (`.github/workflows/`)
```
.github/
└── workflows/
    ├── ci.yml                  # Code quality, testing, security
    ├── docker-build.yml        # Docker image building & scanning
    ├── cd.yml                  # Production deployment & rollback
    ├── model-training.yml      # Automated ML model retraining
    ├── api-tests.yml           # Integration & performance tests
    └── scheduled-checks.yml    # Dependency & security monitoring
```

### Configuration & Support Files
```
Project Root/
├── docker-compose.yml          # Local dev environment + Prometheus
├── prometheus.yml              # Monitoring configuration
├── pytest.ini                  # Test framework settings
├── Makefile                    # Development helper commands
├── run-local-ci-tests.sh      # Script to test CI locally
└── .github/
    └── WORKFLOWS.md           # Detailed workflow documentation
```

### Documentation Files
```
Project Root/
├── CI_CD_GUIDE.md              # Getting started guide (READ THIS FIRST)
├── CI_CD_SETUP_SUMMARY.md      # This summary file
├── DEPLOYMENT.md               # Production deployment guide
└── README.md                   # (existing - may need updates)
```

---

## 🎯 6 Automated Workflows

### 1️⃣ **CI Pipeline** (`ci.yml`)
**When:** Push to main/develop, Pull Requests
**What it does:**
- Tests Python 3.9 & 3.10 compatibility
- Linting with flake8
- Code formatting check with black
- Import sorting with isort
- Unit tests with pytest
- Coverage reporting to Codecov
- Security scans with bandit and safety

**Artifacts:** Coverage reports, security reports

---

### 2️⃣ **Docker Build & Push** (`docker-build.yml`)
**When:** Push to main, tag creation, PRs
**What it does:**
- Builds Docker image with multi-platform support
- Pushes to GitHub Container Registry (GHCR)
- Tests Docker image
- Scans for vulnerabilities with Trivy
- Uses GitHub Actions cache for speed

**Artifacts:** Docker image, Trivy scan results

---

### 3️⃣ **CD Pipeline - Deployment** (`cd.yml`)
**When:** Push to main branch (requires secrets)
**What it does:**
- Pulls latest Docker image
- Deploys to production via SSH
- Runs health checks (5 retries, 10s intervals)
- Automatically rolls back on failure
- Sends notifications

**Requires Secrets:**
- `DEPLOY_HOST` - Server hostname
- `DEPLOY_USER` - SSH username
- `DEPLOY_KEY` - SSH private key

---

### 4️⃣ **Model Training Pipeline** (`model-training.yml`)
**When:** Weekly (Sunday 2 AM), manual trigger, notebook changes
**What it does:**
- Runs training notebook
- Validates trained models
- Logs metrics with MLflow
- Uploads artifacts (30-day retention)
- Creates PR with new models
- Notifies on failure

**Artifacts:** Trained models (cnn_model.pt, cnn_model_full.pt)

---

### 5️⃣ **API Integration Tests** (`api-tests.yml`)
**When:** Push, PRs, daily at 6 AM
**What it does:**
- Integration tests against live API
- Load testing with Locust (10 users)
- Performance benchmarking
- Response time validation
- Concurrent request testing

**Artifacts:** Test reports, load test results, performance data

---

### 6️⃣ **Scheduled Health Checks** (`scheduled-checks.yml`)
**When:** Every 6 hours
**What it does:**
- Checks for outdated dependencies
- Detects known vulnerabilities
- Code complexity analysis with Radon
- Docker image security scanning
- Test coverage trend analysis
- Alerts on coverage drops below 70%

**Artifacts:** Security reports, coverage data

---

## 🚦 Quick Start (5 Minutes)

### Step 1: Commit Everything
```bash
cd bitsMtech_MLOps_Assignment_2
git add .
git commit -m "Add CI/CD automated workflows"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create new public repository
3. Copy repository URL

### Step 3: Push Code
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bitsMtech_MLOps_Assignment_2.git
git push -u origin main
```

### Step 4: Verify Workflows
1. Go to GitHub repository
2. Click "Actions" tab
3. Watch workflows execute ✅

### Step 5 (Optional): Configure Deployment
For production deployment:
1. Settings → Secrets and variables → Actions
2. Add `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`
3. See DEPLOYMENT.md for detailed setup

---

## 💡 Usage Examples

### Run Tests Locally Before Push
```bash
# Install dev tools
make dev-install

# Run all checks (like CI does)
make test
make lint
make format-check

# Or run everything at once
./run-local-ci-tests.sh
```

### Test Docker Build Locally
```bash
# Build
make docker-build

# Run
make docker-run

# Stop
make docker-stop
```

### Run Makefile Commands
```bash
make help                  # Show all commands
make install               # Install dependencies
make run                   # Run API locally
make test                  # Run tests
make lint                  # Code quality
make format                # Auto-format code
make docker-build          # Build Docker image
make docker-run           # Start with docker-compose
```

### Manual Model Retraining
1. Go to Actions tab
2. Select "Model Training Pipeline"
3. Click "Run workflow"
4. Check results in artifacts

---

## 📊 What Gets Tested/Scanned

### Code Quality ✅
- Style: flake8 + black
- Imports: isort
- Complexity: Radon
- Linting: pylint

### Security ✅
- Code vulnerabilities: bandit
- Dependency vulnerabilities: safety, pip-audit
- Container vulnerabilities: Trivy
- Software composition analysis

### Testing ✅
- Unit tests: pytest
- Integration tests: FastAPI TestClient
- Performance tests: benchmarking
- Load tests: Locust
- Code coverage: pytest-cov

### Coverage Tracking ✅
- Per-commit coverage
- Coverage history
- Coverage badges
- Trend analysis

---

## 🔐 Security & Secrets

### No Secrets Exposed
- ✅ SSH keys in GitHub Secrets, not in code
- ✅ Environment variables not in workflows
- ✅ Credentials never logged

### How to Add Secrets
1. GitHub repository → Settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `SECRET_NAME`
5. Value: `secret_value`
6. Use in workflows as: `${{ secrets.SECRET_NAME }}`

### Pre-configured Secrets
For deployment (optional):
- `DEPLOY_HOST` - Production server
- `DEPLOY_USER` - SSH username  
- `DEPLOY_KEY` - SSH private key

---

## 📈 Metrics & Monitoring

### What's Monitored
- Build times
- Test execution times
- Test coverage percentage
- Code complexity
- Dependency versions
- Security vulnerabilities
- Deployment health
- API response times

### Access Metrics
- **GitHub Actions:** Repository → Actions tab
- **Codecov:** Links in PRs, artifacts
- **Prometheus:** `http://server:9090` (if deployed)
- **Security:** Repository → Security tab

---

## 🛠️ Customization Options

### Change Workflow Triggers
Edit the `on:` section in workflow files to trigger on different events:
```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'app/**'    # Only trigger on app changes
```

### Adjust Test Thresholds
In `ci.yml`, modify coverage requirements:
```yaml
--cov-fail-under=80  # Fail if coverage < 80%
```

### Change Scheduled Times
Use cron syntax (minute hour day month day-of-week):
```yaml
schedule:
  - cron: '0 2 * * 0'  # Sunday at 2 AM UTC
```

### Add Custom Steps
Add new jobs or steps in any workflow file

---

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflows not running | Push to main branch, check Actions enabled |
| Tests fail locally | Run `make dev-install`, check Python 3.9+ |
| Docker build fails | Check `requirements_fastapi.txt`, test locally |
| Deployment fails | Configure GitHub Secrets, check SSH access |
| Coverage drops | Add tests, see PR comments for coverage diff |

See detailed troubleshooting in CI_CD_GUIDE.md

---

## 📚 Documentation Map

| Need | Read |
|------|------|
| Overview & quick start | **CI_CD_GUIDE.md** ← START HERE |
| All workflow details | .github/WORKFLOWS.md |
| Production deployment | DEPLOYMENT.md |
| Development commands | Makefile (use `make help`) |
| Setup summary | CI_CD_SETUP_SUMMARY.md |

---

## ✨ Key Features

🟢 **Continuous Integration**
- Every push triggers tests
- Multi-version compatibility
- Code quality enforcement
- Security scanning
- Coverage reporting

🔵 **Continuous Deployment**
- Automatic deployment to production
- Health checks with auto-rollback
- Zero-downtime deployments
- Secure SSH-based deployment

🟡 **Model Training Automation**
- Weekly retraining
- Automatic validation
- Artifact management
- MLflow integration
- PR creation for review

🟠 **Monitoring & Observability**
- Prometheus metrics collection
- Scheduled health checks
- Dependency monitoring
- Performance tracking
- Security alerts

🟣 **Security & Compliance**
- Code vulnerability scanning
- Dependency vulnerability checks
- Container image scanning
- Secret management
- Audit trails

---

## 🎓 Learning Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [Pytest Guide](https://docs.pytest.org/)

---

## 🚀 Next Steps

1. **✅ Push code to GitHub** (if not done)
   ```bash
   git push origin main
   ```

2. **✅ Monitor first run** 
   - Actions tab → See workflows execute

3. **✅ (Optional) Setup deployment**
   - Follow DEPLOYMENT.md
   - Configure GitHub Secrets

4. **✅ Customize for your needs**
   - Adjust test triggers
   - Add custom checks
   - Fine-tune thresholds

5. **✅ Share with team**
   - CI_CD_GUIDE.md for team members
   - Explain workflow stages
   - Document any custom procedures

---

## 📞 Support

For detailed information:
- **Getting started:** CI_CD_GUIDE.md
- **Workflow details:** .github/WORKFLOWS.md  
- **Deployment:** DEPLOYMENT.md
- **Development:** Makefile (`make help`)

---

**🎉 Your CI/CD pipeline is ready!**

All automation is in place. Code changes will automatically be tested, built, and deployed (if configured).

Happy deploying! 🚀
