# Makefile

# Image name and version
IMAGE_NAME ?= adapted-work
IMAGE_VERSION ?= 0.0.1

DOCKERFILE_PATH = ./docker/Dockerfile

CONTEXT = .

.PHONY: docker-build

docker-build:
	docker build -f $(DOCKERFILE_PATH) -t $(IMAGE_NAME):$(IMAGE_VERSION) $(CONTEXT)
