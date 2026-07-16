# DevOps Capstone Project

[![CI/CD Pipeline](https://github.com/ahmedfawzyjr/devops-capstone-project/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmedfawzyjr/devops-capstone-project/actions/workflows/ci.yml)
[![Tests](https://github.com/ahmedfawzyjr/devops-capstone-project/actions/workflows/test.yml/badge.svg)](https://github.com/ahmedfawzyjr/devops-capstone-project/actions/workflows/test.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/ahmedfawzyjr/devops-capstone)](https://hub.docker.com/r/ahmedfawzyjr/devops-capstone)
[![GitHub release](https://img.shields.io/github/v/release/ahmedfawzyjr/devops-capstone-project)](https://github.com/ahmedfawzyjr/devops-capstone-project/releases)

## 📖 About This Project

A **Food Delivery API** built with Python Flask, fully containerized with Docker, and deployed automatically via a GitHub Actions CI/CD pipeline to AWS EC2. This project was developed as a DevOps capstone showcasing end-to-end automation from code commit to production deployment.

**Application Features:**
- 🍅 **Ingredient Management** — Add, update, and delete ingredients for food delivery
- 👤 **Account Management** — Full CRUD for user accounts
- 🗺️ **Zone Management** — Delivery zone creation and management
- 🏥 **Health Check** — `/health` endpoint for container orchestration

---

## 👥 Team Members & Task Assignment

| Team Member | Tasks Assigned | GitHub Username |
|---|---|---|
| Ahmed Fawzy | CI/CD Pipeline, Docker, GitHub Actions, Python App | @ahmedfawzyjr |

---

## 🔗 Project Links

- **GitHub Repository:** `https://github.com/ahmedfawzyjr/devops-capstone-project`
- **GitHub Actions (CICD):** `https://github.com/YOUR_USERNAME/devops-capstone/actions`
- **Docker Hub Image:** `https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/devops-capstone`
- **GitHub Board:** `https://github.com/YOUR_USERNAME/devops-capstone/projects`
- **GitHub Releases:** `https://github.com/YOUR_USERNAME/devops-capstone/releases`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CI/CD Pipeline Flow                         │
│                                                                 │
│  Developer  ──push──▶  GitHub  ──trigger──▶  GitHub Actions    │
│                                                                 │
│  GitHub Actions:                                                │
│    [1] Greet & Echo   ──▶  echo "Your name is Ahmed Fawzy"     │
│    [2] Lint           ──▶  flake8 / black                       │
│    [3] Test           ──▶  pytest (ingredient story ✅)         │
│    [4] Build          ──▶  docker build                         │
│    [5] Push           ──▶  Docker Hub                           │
│    [6] Deploy         ──▶  AWS EC2 via SSH                      │
│                                                                 │
│  AWS EC2:  docker pull ──▶  docker run ──▶  /health ✅         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
devops-capstone/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Main CI/CD pipeline (build, test, push, deploy)
│       ├── test.yml        # Automated test runner
│       └── release.yml     # Versioned release workflow
├── app/
│   ├── __init__.py
│   ├── main.py             # Flask API application
│   └── tests/
│       ├── __init__.py
│       └── test_main.py    # pytest test suite
├── curl-commands/
│   ├── curl-create-zone.txt   # Task: POST /zones
│   ├── curl-read-done.txt     # Task: GET /ingredients
│   ├── curl-update-goals.txt  # Task: PUT /accounts/:id
│   └── curl-delete-all.txt    # Task: DELETE /accounts
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Run Locally (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python -m flask --app app.main run --port 5000
```

### Run with Docker
```bash
# Build the image
docker build -t devops-capstone .

# Run the container
docker run -d -p 5000:5000 --name devops-capstone devops-capstone

# Health check
curl http://localhost:5000/health
```

### Run with Docker Compose
```bash
# Start the app
docker-compose up -d

# Run tests
docker-compose --profile test run test
```

### Pull from Docker Hub
```bash
docker pull YOUR_DOCKERHUB_USERNAME/devops-capstone:latest
docker run -d -p 5000:5000 YOUR_DOCKERHUB_USERNAME/devops-capstone:latest
```

---

## 🧪 Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest app/tests/ -v

# Run with coverage
python -m pytest app/tests/ -v --cov=app --cov-report=term-missing

# Run specific story test
python -m pytest app/tests/test_main.py::TestIngredients::test_add_ingredient_to_food_delivery_app -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Story |
|--------|----------|-------------|-------|
| GET | `/` | Welcome message | — |
| GET | `/health` | Health check | — |
| GET | `/accounts` | Get all accounts | — |
| POST | `/accounts` | Create account | — |
| GET | `/accounts/:id` | Get account by ID | — |
| PUT | `/accounts/:id` | Update account | curl-update-goals |
| DELETE | `/accounts` | Delete ALL accounts | "Delete all accounts" |
| DELETE | `/accounts/:id` | Delete one account | — |
| GET | `/ingredients` | Get all ingredients | curl-read-done |
| POST | `/ingredients` | Add ingredient | "Add ingredient to food delivery app" |
| GET | `/ingredients/:id` | Get ingredient by ID | curl-read-done |
| PUT | `/ingredients/:id` | Update ingredient | — |
| DELETE | `/ingredients/:id` | Delete ingredient | — |
| GET | `/zones` | Get all zones | — |
| POST | `/zones` | Create zone | curl-create-zone |
| GET | `/zones/:id` | Get zone by ID | — |
| DELETE | `/zones/:id` | Delete zone | — |

---

## 🔒 GitHub Secrets Required

Add these secrets in `Settings > Secrets and variables > Actions`:

| Secret Name | Description |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token |
| `EC2_HOST` | Public IP/DNS of your AWS EC2 instance |
| `EC2_USER` | SSH username (e.g., `ubuntu` or `ec2-user`) |
| `EC2_SSH_KEY` | Private SSH key content (.pem file) |

---

## 🔄 CI/CD Pipeline Details

### Workflow: `ci.yml`
Triggered on push to `main` or `develop`, and on pull requests.

```
greet → lint → test → build → push (main only) → deploy (main only)
```

### Workflow: `test.yml`
Runs on every push to any branch. Executes all pytest tests.

### Workflow: `release.yml`
Triggered when a version tag is pushed (e.g., `v1.0.0`).
Creates a GitHub Release named: **"Release v1.0.0 — Add Ingredient to Food Delivery App"**

```bash
# Create a release
git tag v1.0.0
git push origin v1.0.0
```

---

## 🐳 Docker Hub

The image is automatically built and pushed on every push to `main`:

```
YOUR_DOCKERHUB_USERNAME/devops-capstone:latest
YOUR_DOCKERHUB_USERNAME/devops-capstone:sha-<commit_sha>
YOUR_DOCKERHUB_USERNAME/devops-capstone:v1.0.0  (on release)
```

---

## 📋 CURL Commands Reference

All curl commands are documented in the `curl-commands/` folder:

### Create Zone
```bash
curl -X POST http://localhost:5000/zones \
  -H "Content-Type: application/json" \
  -d '{"name": "Zone-A", "region": "North"}'
```

### Read Ingredients (Read Done)
```bash
curl -X GET http://localhost:5000/ingredients
```

### Update Account Goals
```bash
curl -X PUT http://localhost:5000/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahmed Fawzy Jr", "email": "updated@example.com"}'
```

### Delete All Accounts
```bash
curl -X DELETE http://localhost:5000/accounts
```

---

## 📸 Screenshots

> Screenshots of GitHub Actions runs, Docker Hub, and AWS EC2 deployment are available in the project's GitHub Actions tab.

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.
