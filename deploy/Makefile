# Makefile to simplify some local Docker steps

BRANCH:=$(shell git rev-parse --abbrev-ref HEAD)

build:
	docker build --build-arg branch=$(BRANCH) -t 'fuzzing-book' fuzzingbook-dockerenv

build-publish:
	docker build --build-arg publish=yes --build-arg branch=$(BRANCH) -t 'fuzzing-book' fuzzingbook-dockerenv
