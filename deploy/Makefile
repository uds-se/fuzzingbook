# Makefile to simplify some local Docker steps

BRANCH:=$(shell git rev-parse --abbrev-ref HEAD)

build:
	docker build --build-arg BRANCH=$(BRANCH) -t 'fuzzing-book' fuzzingbook-base

build-publish:
	docker build --build-arg publish=yes --build-arg BRANCH=$(BRANCH) -t 'fuzzing-book' fuzzingbook-base

# This runs the docker image in a *temporary* container
run-temporary:
	@echo "Starting temporary local docker container..."
	-docker run --rm -d -p 8888:8888 -p 8000:8000 --name fuzzing-book-instance fuzzing-book
	sleep 5
	docker exec -u fuzzingbook -it fuzzing-book-instance jupyter notebook list | grep http
	@echo "Container is running, press CTRL+C to stop and remove container..."
	docker attach fuzzing-book-instance

# Spawn a shell in the running docker container for debugging
shell:
	docker exec -it -u fuzzingbook fuzzing-book-instance bash

rootshell:
	docker exec -it -u root fuzzing-book-instance bash
