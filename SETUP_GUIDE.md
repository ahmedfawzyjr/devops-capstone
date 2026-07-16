# GitHub Secrets Setup Guide
# ─────────────────────────────────────────────────────────────────────────────
# How to configure all required GitHub Actions secrets
# ─────────────────────────────────────────────────────────────────────────────

## Step 1: Go to Your Repository Settings
# Navigate to: https://github.com/YOUR_USERNAME/devops-capstone/settings/secrets/actions
# Click: "New repository secret"

## Secrets to Add:

### 1. DOCKER_USERNAME
# Value: Your Docker Hub username (e.g., ahmedfawzyjr)

### 2. DOCKER_PASSWORD
# Value: Your Docker Hub password OR an Access Token (recommended)
# Create token at: https://hub.docker.com/settings/security
# Click "New Access Token" → "devops-capstone-token"

### 3. EC2_HOST
# Value: Your EC2 instance public IP or DNS
# Example: 54.123.45.67  OR  ec2-54-123-45-67.compute-1.amazonaws.com

### 4. EC2_USER
# Value: The SSH username for your EC2 instance
# Amazon Linux: ec2-user
# Ubuntu:       ubuntu

### 5. EC2_SSH_KEY
# Value: The FULL CONTENT of your .pem key file
# Example — run this in bash to get the value:
#   cat my-key.pem
# Then paste the entire output including -----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY-----

## ─────────────────────────────────────────────────────────────────────────────
## AWS EC2 Setup Commands (run once on your EC2 instance)
## ─────────────────────────────────────────────────────────────────────────────

# 1. Update system packages
sudo apt-get update -y

# 2. Install Docker
sudo apt-get install -y docker.io

# 3. Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 4. Add ubuntu user to docker group (so no sudo needed)
sudo usermod -aG docker ubuntu

# 5. Verify Docker is running
docker --version
docker info

# ─────────────────────────────────────────────────────────────────────────────
## First Manual Deployment (run once on EC2 after Docker is installed)
## ─────────────────────────────────────────────────────────────────────────────

# Pull and run the image manually first time
docker pull YOUR_DOCKERHUB_USERNAME/devops-capstone:latest
docker run -d \
  --name devops-capstone \
  --restart unless-stopped \
  -p 5000:5000 \
  YOUR_DOCKERHUB_USERNAME/devops-capstone:latest

# Test it
curl http://localhost:5000/health
