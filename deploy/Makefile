# Makefile to simplify some local Docker steps

BRANCH:=$(shell git rev-parse --abbrev-ref HEAD)

build:
	docker build --build-arg BRANCH=$(BRANCH) -t 'fuzzing-book' fuzzingbook-base

build-publish:
	docker build --build-arg publish=yes --build-arg BRANCH=$(BRANCH) -t 'fuzzing-book' fuzzingbook-base

# This runs the docker image in a *temporary* container
run-temporary:
	@echo "Starting temporary local docker container..."
	@docker run --rm -d -p 8888:8888 -p 8000:8000 --name fuzzing-book-instance fuzzing-book
	@while ! docker exec -u fuzzingbook -it fuzzing-book-instance jupyter notebook list | grep http; do sleep 1; done
	@echo "Container is running, run 'docker stop fuzzing-book-instance' to stop and remove container..."

# Spawn a shell in the running docker container for debugging
shell:
	docker exec -it -u fuzzingbook fuzzing-book-instance bash

rootshell:
	docker exec -it -u root fuzzing-book-instance bash
