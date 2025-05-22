# Deployment Guide

This document provides instructions for deploying the application in different environments.

## Prerequisites

Before deploying the application, ensure you have the following prerequisites:

- Docker and Docker Compose installed
- Git for version control
- Access to Docker Hub (for pulling images)
- SSH access to deployment servers (for automated deployments)

## Local Development Deployment

### Using Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/vmmaltsev/devops-ci-cd-pipeline-demo.git
   cd devops-ci-cd-pipeline-demo
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application at http://localhost:8080

### Manual Development

1. Clone the repository:
   ```bash
   git clone https://github.com/vmmaltsev/devops-ci-cd-pipeline-demo.git
   cd devops-ci-cd-pipeline-demo
   ```

2. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

3. Run the application:
   ```bash
   cd app
   python main.py
   ```

4. Access the application at http://localhost:8080

## Production Deployment

### Using Docker Compose

1. Clone the repository on your production server:
   ```bash
   git clone https://github.com/vmmaltsev/devops-ci-cd-pipeline-demo.git
   cd devops-ci-cd-pipeline-demo
   ```

2. Create a `.env` file with production settings:
   ```bash
   echo "FLASK_ENV=production" > .env
   echo "FLASK_DEBUG=0" >> .env
   ```

3. Deploy with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the application at http://your-server-ip:8080

### Automated CI/CD Deployment

The CI/CD pipeline will automatically deploy to production when:
- A commit is pushed to the main branch
- A new version tag is created

Prerequisites for automated deployment:
1. Configure GitHub repository secrets:
   - `DOCKERHUB_USERNAME`: Docker Hub username
   - `DOCKERHUB_TOKEN`: Docker Hub access token
   - `DEPLOY_HOST`: Production server hostname/IP
   - `DEPLOY_USERNAME`: SSH username
   - `DEPLOY_KEY`: SSH private key

2. Ensure the target server has:
   - Docker and Docker Compose installed
   - The repository cloned at `~/devops-demo`
   - Proper permissions for the deployment user

## Monitoring Deployment

### Deploy Monitoring Stack

1. Navigate to the monitoring directory:
   ```bash
   cd devops-ci-cd-pipeline-demo/monitoring
   ```

2. Deploy the monitoring stack:
   ```bash
   docker-compose -f docker-compose.monitoring.yml up -d
   ```

3. Access monitoring interfaces:
   - Prometheus: http://your-server-ip:9090
   - Grafana: http://your-server-ip:3000 (username: admin, password: admin)
   - Alertmanager: http://your-server-ip:9093

## Configuration Options

The application can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Application environment | production |
| FLASK_DEBUG | Enable debug mode (0/1) | 0 |
| PORT | Application port | 8080 |
| HOST | Host to bind | 0.0.0.0 |

Set these variables in your `.env` file or in the Docker Compose file.

## Scaling the Application

To scale the application horizontally:

1. Edit the `docker-compose.yml` file to add a load balancer (like Nginx or Traefik)
2. Scale the web service:
   ```bash
   docker-compose up -d --scale web=3
   ```

## Updating the Application

### Manual Update

1. Pull the latest code:
   ```bash
   cd devops-ci-cd-pipeline-demo
   git pull
   ```

2. Rebuild and restart:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

### Automated Update via CI/CD

The CI/CD pipeline automatically updates the application when new code is pushed. The update process:

1. Builds a new Docker image
2. Pushes the image to Docker Hub
3. Connects to the production server via SSH
4. Pulls the latest code and Docker image
5. Restarts the application with the new version

## Rollback Procedure

If you need to rollback to a previous version:

1. Identify the tag or commit to rollback to
2. On the production server:
   ```bash
   cd devops-ci-cd-pipeline-demo
   git checkout <tag-or-commit-hash>
   docker-compose down
   docker-compose up -d --build
   ```

Alternatively, specify an exact image version in `docker-compose.yml`:
```yaml
services:
  web:
    image: username/devops-demo:v1.0.0
```

## Maintenance

### Database Backups

This application currently doesn't include a database. If you add one, implement a backup strategy:

```bash
# Example PostgreSQL backup
docker exec -t db pg_dumpall -c -U postgres > backup.sql
```

### Log Management

Application logs are stored in Docker's json-file driver with rotation:
- Max file size: 10MB
- Max files: 3

To view logs:
```bash
docker-compose logs -f web
```

### Monitoring Alerts

Configure alerting rules in Prometheus and notification channels in Alertmanager to receive alerts for:
- Service downtime
- High error rates
- Resource constraints

## Troubleshooting

### Container Won't Start

Check container logs:
```bash
docker-compose logs web
```

### Health Checks Failing

Verify the health check endpoint:
```bash
curl http://localhost:8080/health
```

### High Memory Usage

Check container resource usage:
```bash
docker stats
```

Consider adjusting the resource limits in `docker-compose.yml`.
