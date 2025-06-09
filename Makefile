# Makefile

# Image name and version
IMAGE_NAME ?= adapted-work
IMAGE_VERSION ?= 0.0.1

DOCKERFILE_PATH = ./docker/Dockerfile

CONTEXT = .

TRIVY_FORMAT ?= table
TRIVY_SEVERITY ?= HIGH,CRITICAL

.PHONY: docker-build docker-security

docker-build:
	docker build -f $(DOCKERFILE_PATH) -t $(IMAGE_NAME):$(IMAGE_VERSION) $(CONTEXT)

docker-security: docker-build
	@echo "Escaneando imagen con Trivy..."
	trivy image $(IMAGE_NAME):$(VERSION)
