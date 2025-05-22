# DevOps CI/CD Pipeline Demo

A fully functional example of a CI/CD pipeline for a Python (Flask) application using Docker, GitHub Actions, automated testing, building, publishing, and deployment.

## Architecture

- **CI:** Code validation, automated testing, Docker image build  
- **CD:** Docker image publishing to Docker Hub and automated deployment via docker-compose  
- **Monitoring:** Example integration with Prometheus + Grafana

See [docs/architecture.md](docs/architecture.md) for details.

## Features

- Flask application with proper logging and error handling
- Docker containerization with best practices
- Health check endpoint for monitoring
- Comprehensive test suite
- Resource limiting and container health checks
- Environment variable configuration

## Quick Start

```bash
# Clone the repository
git clone https://github.com/vmmaltsev/devops-ci-cd-pipeline-demo.git
cd devops-ci-cd-pipeline-demo

# Start with Docker Compose
docker-compose up --build
```

The application will be available at http://localhost:8080

## Development

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Make (optional, for using Makefile commands)

### Setup Local Environment

```bash
# Install dependencies
make setup
# or
pip install -r app/requirements.txt

# Run tests
make test
# or
cd app && pytest -v tests/

# Run the application locally
make run
# or
cd app && python main.py
```

### Available Make Commands

- `make setup` - Install dependencies
- `make run` - Run application locally
- `make test` - Run tests
- `make lint` - Run linter
- `make docker-build` - Build Docker image
- `make docker-run` - Run Docker container
- `make docker-compose-up` - Start with Docker Compose
- `make docker-compose-down` - Stop Docker Compose services
- `make clean` - Clean up cache files
- `make help` - Show available commands

## Environment Variables

The application can be configured using environment variables:

- `FLASK_ENV` - Environment (development/production)
- `FLASK_DEBUG` - Enable debug mode (0/1)
- `PORT` - Application port (default: 8080)
- `HOST` - Application host (default: 0.0.0.0)

## License

See [LICENSE](LICENSE) file.
