# How to: Install the interactive fuzzing book on a local docker container

## Step 1: Install Docker
Follow the installation procedure recommended at docker.com, or, if you are using Linux, refer to your distribution for information on the installation process.

Once installed, make sure Docker works by typing `docker info` in a shell. If there are no errors, you can proceed to Step 2.

## Step 2: Set up the image
Run the following command to build the docker image for the book container:

```shell
docker build -t 'fuzzing-book' fuzzingbook-dockerenv
```

## Step 3: Creating an instance of the image
Run the following command to start up an instance of the fuzzing book container for the first time and connect it to your local port 8888.

`docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book`

Now just follow the instructions to open the notebook in your browser. You can close the terminal window now, the container will keep running in the background until you stop it.

## Stopping the container
`docker stop fuzzing-book-instance`

## Restarting an existing container
`docker start fuzzing-book-instance`

## Updating the book
You can recreate the container and image to update the book. A more elegant solution is WIP:
```shell
docker stop fuzzing-book-instance
docker rm fuzzing-book-instance
docker rmi fuzzing-book
docker build -t 'fuzzing-book' fuzzingbook-dockerenv
docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book
```

## Uninstalling
To delete the docker container and image, execute the following commands:
```shell
docker stop fuzzing-book-instance
docker rm fuzzing-book-instance
docker rmi fuzzing-book
```
## Compiling the book
*WIP*