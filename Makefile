.PHONY: setup test run lint docker-build docker-run clean

setup:
	pip install -r app/requirements.txt

run:
	cd app && python main.py

test:
	cd app && pytest -v tests/

lint:
	cd app && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

docker-build:
	docker build -t devops-demo .

docker-run:
	docker run -p 8080:8080 devops-demo

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

help:
	@echo "Available commands:"
	@echo " - setup            : Install dependencies"
	@echo " - run              : Run the application locally"
	@echo " - test             : Run tests"
	@echo " - lint             : Run linter"
	@echo " - docker-build     : Build Docker image"
	@echo " - docker-run       : Run Docker container"
	@echo " - docker-compose-up: Start application with docker-compose"
	@echo " - docker-compose-down: Stop application with docker-compose"
	@echo " - clean            : Clean up cache files"
