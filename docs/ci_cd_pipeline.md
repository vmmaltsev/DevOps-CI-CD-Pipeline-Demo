# CI/CD Pipeline Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline implemented in this project.

## Overview

The CI/CD pipeline automates the following processes:

1. Code validation and testing
2. Security scanning
3. Building Docker images
4. Publishing images to a container registry
5. Deploying to target environments

The pipeline is implemented using GitHub Actions, which provides workflow automation directly integrated with GitHub repositories.

## CI Pipeline

The Continuous Integration pipeline is defined in `.github/workflows/ci.yml` and runs on every push to the main branch and on pull requests.

### CI Pipeline Steps

#### 1. Setup Environment

```yaml
- name: Checkout code
  uses: actions/checkout@v4

- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
```

This step:
- Checks out the repository code
- Sets up Python 3.12
- Configures pip caching to speed up dependencies installation

#### 2. Install Dependencies

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r app/requirements.txt
    pip install flake8 pytest-cov bandit safety
```

This step:
- Upgrades pip to the latest version
- Installs application dependencies
- Installs testing and security tools

#### 3. Code Quality Checks

```yaml
- name: Run linting
  run: flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

This step checks code quality using flake8, looking for critical errors:
- E9: Syntax errors
- F63: Assertion errors
- F7: Semantic errors
- F82: Undefined variables

#### 4. Security Scanning

```yaml
- name: Run security scan
  run: |
    bandit -r app/ -c pyproject.toml || true
    safety check -r app/requirements.txt || true
```

This step:
- Runs Bandit to detect common security issues in Python code
- Uses Safety to check for vulnerabilities in dependencies
- Uses the `|| true` flag to prevent pipeline failure, treating findings as warnings

#### 5. Run Tests with Coverage

```yaml
- name: Run tests with coverage
  run: pytest app/tests/ --cov=app --cov-report=xml

- name: Upload coverage report
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: false
```

This step:
- Runs the test suite with pytest
- Generates code coverage reports
- Uploads coverage data to Codecov for tracking over time

#### 6. Build and Scan Docker Image

```yaml
- name: Build Docker image
  run: docker build -t demo-app .

- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'demo-app'
    format: 'table'
    exit-code: '0'
    severity: 'CRITICAL,HIGH'
```

This step:
- Builds a Docker image from the Dockerfile
- Scans the Docker image for vulnerabilities using Trivy
- Focuses on CRITICAL and HIGH severity issues

## CD Pipeline

The Continuous Deployment pipeline is defined in `.github/workflows/cd.yml` and runs on successful completion of the CI pipeline or directly on pushes to the main branch and tags.

### CD Pipeline Steps

#### 1. Docker Hub Authentication

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

This step authenticates with Docker Hub using repository secrets.

#### 2. Set Up Docker Buildx

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```

This step sets up Docker Buildx for multi-platform building capabilities.

#### 3. Image Metadata

```yaml
- name: Extract metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: ${{ secrets.DOCKERHUB_USERNAME }}/devops-demo
    tags: |
      type=semver,pattern={{version}}
      type=semver,pattern={{major}}.{{minor}}
      type=ref,event=branch
      type=sha,format=short
      latest
```

This step:
- Configures image tagging based on Git information
- Supports semantic versioning from tags
- Creates branch-based and commit SHA tags
- Always updates the 'latest' tag

#### 4. Build and Push

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    cache-from: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/devops-demo:buildcache
    cache-to: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/devops-demo:buildcache,mode=max
```

This step:
- Builds the Docker image
- Pushes it to Docker Hub with the configured tags
- Uses registry caching to speed up builds

#### 5. Deployment

```yaml
- name: Deploy to production server
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USERNAME }}
    key: ${{ secrets.DEPLOY_KEY }}
    script: |
      cd ~/devops-demo
      git pull
      docker-compose pull
      docker-compose up -d
      docker system prune -af --volumes
```

This step:
- Connects to the deployment server using SSH
- Updates the application code
- Pulls the latest Docker image
- Restarts the application with docker-compose
- Cleans up unused resources

## Pipeline Triggers

### CI Pipeline Triggers

- **Push to main branch**: Runs on every commit to the main branch
- **Pull Request**: Runs when a pull request targets the main branch

### CD Pipeline Triggers

- **Successful CI Run**: Triggered when the CI workflow completes successfully
- **Push to main branch**: Direct deployment from main branch
- **Tagged Releases**: Triggered when a tag is pushed (format: v*)

## Required Secrets

For the pipelines to work properly, the following secrets must be configured in the GitHub repository:

- `DOCKERHUB_USERNAME`: Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token
- `DEPLOY_HOST`: Hostname/IP of the deployment server
- `DEPLOY_USERNAME`: SSH username for the deployment server
- `DEPLOY_KEY`: SSH private key for authentication

## Pipeline Flow Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Code Changes   │────▶│   CI Pipeline   │────▶│   CD Pipeline   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │  Quality Gates  │     │   Deployment    │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
                               │                        │
                               ▼                        ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │ Security Checks │     │   Monitoring    │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
```

## Adding New Pipeline Steps

To extend the pipeline with new steps:

1. Edit the appropriate workflow file (`.github/workflows/ci.yml` or `.github/workflows/cd.yml`)
2. Add the new step in the desired position
3. Commit and push the changes
4. The new step will be included in the next pipeline run
