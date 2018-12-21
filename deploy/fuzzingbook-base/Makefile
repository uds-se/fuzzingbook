repository = fuzzingbook
image = base
instance = fuzzing-book-instance
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

tag = $(repository)/$(image)
deps = $(wildcard fuzzingbook*.txt)

all: $(tag)

.DEFAULT: all
.PHONY: clean mrproper container debug start

# Build the docker image
$(tag): Dockerfile $(deps) check-env
	$(info Building image with tag $(tag))
	@docker build --build-arg branch=$(BRANCH) -t $(tag) --squash .

# Deploy the image to docker.io
push: $(tag)
	$(info Deploying image with tag $(tag))
	@docker push $(tag)

# Delete all images for $(tag)
mrproper: clean
	$(info Removing images for tag $(tag) and pruning related images.)
	-docker rmi $(tag) >/dev/null 2>&1
	-docker rmi $(shell docker images -a --filter=dangling=true -q) >/dev/null 2>&1

container: $(tag)
	$(info Creating container with name $(image))
	docker create -p 8080:8080 -p 8000:8000 --name $(image) $(tag)

debug: $(tag)
	$(info Starting temporary container with image $(image))
	@docker run --rm -it -p 8080:8080 -p 8000:8000 --user root $(tag) /bin/bash

start: container
	$(info Attaching to persistent container with name $(image))
	@docker start --attach $(image)

run-temporary: $(tag)
	@echo "Starting temporary local docker container..."
	@docker run --rm -d -p 8888:8888 -p 8000:8000 --name $(instance) $(tag)
	@while ! docker exec -u fuzzingbook -it $(instance) jupyter notebook list | grep http; do sleep 1; done
	@echo "Container is running, run 'docker stop $(instance)' to stop and remove container..."

# Spawn a shell for a currently running instance
shell:
	docker exec -it -u fuzzingbook $(instance) bash

rootshell:
	docker exec -it -u root $(instance) bash

# Stop the instance started with run-temporary
stop:
	docker stop $(instance)

# Check environment variables
check-env:
# ifndef GITUSER
# $(error GITUSER is undefined)
# endif
# ifndef GITPASSWORD
# $(error GITPASSWORD is undefined)
# endif
ifndef HOST
HOST = localhost
endif
