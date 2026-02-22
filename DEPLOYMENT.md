# DEPLOYMENT GUIDE

## Overview
This guide covers deploying the MLOps Cat vs Dog Classifier API to production using the automated CD pipeline.

---

## Prerequisites

### 1. Production Server Requirements
- Ubuntu 20.04 LTS or later
- Docker and Docker Compose installed
- SSH access configured
- Minimum 4GB RAM, 2 CPU cores
- Port 8000 available (or configure alternative)

### 2. GitHub Configuration
- Repository with CI/CD workflows enabled
- GitHub Container Registry access

### 3. SSH Key Setup
Generate a deployment SSH key on your local machine:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mlops_deploy -N ""
```

Add public key to production server:
```bash
# On production server
cat ~/.ssh/mlops_deploy.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

## GitHub Secrets Configuration

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

| Secret | Value | Example |
|--------|-------|---------|
| `DEPLOY_HOST` | Production server hostname/IP | `api.example.com` |
| `DEPLOY_USER` | SSH user | `ubuntu` |
| `DEPLOY_KEY` | Content of private SSH key | (entire key content) |

**Steps to add secrets:**
1. Go to Repository → Settings
2. Left sidebar → Secrets and variables → Actions
3. Click "New repository secret"
4. Enter name and value
5. Click "Add secret"

---

## Production Server Setup

### 1. Install Docker & Docker Compose
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Create Application Directory
```bash
sudo mkdir -p /app
sudo chown $USER:$USER /app
cd /app
```

### 3. Configure SSH for Deployments
```bash
# Create .ssh directory if not exists
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# The deployment key will be pasted by the CD pipeline
# Verify it works:
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### 4. Create Environment File
```bash
cat > /app/.env << EOF
API_TITLE=Cat vs Dog Classifier API
API_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO
EOF
```

---

## Initial Deployment

### Option 1: Automatic Deployment (Recommended)
Push to main branch with configured secrets:

```bash
git push origin main
```

The GitHub Actions CD workflow will automatically:
1. Build Docker image
2. Push to registry
3. SSH into server
4. Pull latest image
5. Run health checks
6. Rollback on failure

### Option 2: Manual Deployment
SSH into production server and run:

```bash
cd /app

# Pull latest image
docker pull ghcr.io/YOUR_USERNAME/mlops-classifier:latest

# Start services
docker-compose up -d

# Check status
docker-compose logs -f api
```

---

## Monitoring Deployment

### Check Workflow Status
1. Go to GitHub repository → Actions tab
2. Look for "CD Pipeline" workflow
3. Click run to see logs

### Common Deployment Statuses
- 🟢 **Success** - Application deployed and healthy
- 🟡 **In Progress** - Building or deploying
- 🔴 **Failed** - Deployment failed; check logs

### View Application Logs
```bash
# SSH into server
ssh -i ~/.ssh/mlops_deploy ubuntu@your-server.com

# View logs
docker-compose logs -f api

# Check running containers
docker-compose ps
```

---

## Health Checks

The CD pipeline automatically checks:
- ✅ Container starts successfully
- ✅ API responds to HTTP requests
- ✅ Health check endpoint returns 200 OK
- ✅ No critical errors in logs

If any check fails:
- Deployment is automatically rolled back
- Previous version is restored
- GitHub notification is sent

---

## Rollback Procedures

### Automatic Rollback
Triggered automatically if health checks fail:
```bash
# Stops containers and rolls back
docker-compose down
```

### Manual Rollback
```bash
# SSH into server
ssh -i ~/.ssh/mlops_deploy ubuntu@your-server.com

cd /app

# Stop current version
docker-compose down

# Restart previous version
docker-compose pull
docker-compose up -d
```

---

## Database & Persistent Storage

### Create Volume for Models
```bash
# On production server
mkdir -p /app/data/models
mkdir -p /app/data/logs

# Update docker-compose.yml volumes:
# volumes:
#   - ./data/models:/app/artifacts
#   - ./data/logs:/app/logs
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt with Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt-get install -y nginx

# Create Nginx config
sudo cat > /etc/nginx/sites-available/api << 'EOF'
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/

# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d api.example.com
```

---

## Environment-Specific Configuration

### Development
```env
DEBUG=True
LOG_LEVEL=DEBUG
WORKERS=1
```

### Production
```env
DEBUG=False
LOG_LEVEL=INFO
WORKERS=4
```

Update in docker-compose.yml:
```yaml
environment:
  - DEBUG=${DEBUG:-False}
  - LOG_LEVEL=${LOG_LEVEL:-INFO}
```

---

## Scaling Considerations

### Multiple Replicas
```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
```

### Load Balancing
Use Nginx or cloud load balancer to:
- Distribute requests across replicas
- Health check instances
- Implement sticky sessions if needed

---

## Performance Optimization

### Container Limits
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Worker Count
```bash
# In docker-compose.yml or startup
CMD ["gunicorn", "app.main:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker"]
```

---

## Backup & Recovery

### Backup Models
```bash
# On production server
cd /app
tar -czf backups/models_$(date +%Y%m%d_%H%M%S).tar.gz artifacts/
```

### Backup Database (if applicable)
```bash
# Add to crontab for daily backups
0 2 * * * cd /app && tar -czf backups/db_$(date +\%Y\%m\%d).tar.gz data/
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs api

# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Deployment Secret Issues
```bash
# Test SSH connection manually
ssh -i ~/.ssh/mlops_deploy -v ubuntu@your-server.com

# Check GitHub Actions logs for exact error
```

### Out of Disk Space
```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Check disk usage
df -h
du -sh /app/*
```

---

## Monitoring & Alerts

### Setup Prometheus Monitoring
Already configured in `docker-compose.yml` and `prometheus.yml`

Access at: `http://your-server:9090`

### View Metrics
1. Open Prometheus dashboard
2. Go to Graph tab
3. Example queries:
   - `rate(http_requests_total[5m])` - Request rate
   - `http_request_duration_seconds` - Response time
   - `container_memory_usage_bytes` - Memory usage

### Setup Alerting
Add to `prometheus.yml`:
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093
```

---

## Update Procedure

### Regular Updates
```bash
# 1. Git push triggers workflow
git push origin main

# 2. GitHub Actions:
#    - Builds new image
#    - Runs tests
#    - Pushes to registry
#    - Deploys to production
#    - Health checks
#    - Rollback if fails

# Monitor at: github.com/YOUR_USERNAME/repo/actions
```

### Emergency Hotfix
```bash
# Fix issue locally
git checkout -b hotfix/critical-issue
# Make changes
git commit -m "Fix: critical production issue"
git push origin hotfix/critical-issue

# Create PR, review, merge
# Automatic deployment follows
```

---

## Security Best Practices

1. ✅ Use SSH keys, not passwords
2. ✅ Keep container images updated
3. ✅ Run security scans in CI/CD
4. ✅ Use secrets for sensitive data
5. ✅ Enable firewall rules
6. ✅ Monitor access logs
7. ✅ Use HTTPS in production
8. ✅ Implement rate limiting

---

## Reference

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [GitHub Actions CD](https://docs.github.com/en/actions/deployment)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)
- [FastAPI Production](https://fastapi.tiangolo.com/deployment/)
