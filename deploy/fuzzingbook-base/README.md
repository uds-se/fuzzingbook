# About

This is a minimal docker image to serve all dependencies and tools for the Fuzzingbook.

## Installation

```
docker pull sjust/fuzzingbook
```

## Using the image

```sh
# Create a persistent container using the fuzzingbook image
docker create -p 8080:8080 -p 8000:8000 --name fuzzingbook sjust/fuzzingbook 

# Start the container
docker start --attach fuzzingbook
```

## Building the image yourself

You can use the included Makefile:

```sh
make
```

If you don't have `make` installed, you can build the image manually using:

```sh
docker build -t sjust/fuzzingbook --squash .
```

NOTE: the `--squash` option (Squash newly built layers into a single new layer) 
is optional and requires experimental features turned on in the Docker daemon.


## For the students

You can run `make run-temporary` to get a temporary instance with the required
software pre-installed. Use `make shell` to gain access to this instance. Your
`fuzzingbook` directory will be mounted under root as `/fuzzingbook`.
