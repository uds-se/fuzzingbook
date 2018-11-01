# How to: Install the interactive fuzzing book on a local docker container

## Step 1: Install Docker
Follow the installation procedure recommended at docker.com, or, if you are using Linux, refer to your distribution for information on the installation process.

Once installed, make sure Docker works by typing `docker info` in a shell. If there are no errors, you can proceed to Step 2.

## Step 2: Set up the image
If you are a Linux or Mac user, you can just run the setup_docker.sh script provided in this directory.

If you are on Windows we will provide an install script soon. For now, set up manually with the following command (executed in this directory):

`docker build -t 'fuzzing-book' fuzzingbook-dockerenv`

## Step 3: Run an instance of the image
If you are a Linux or Mac user, you can just run the run_docker.sh script provided in this directory.

If you are on Windows we will provide an run script soon. For now, set up manually with the following command (executed in this directory):

`docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book`

Now just follow the instructions to open the notebook in your browser. You can close the terminal window now, the container will keep running in the background until you stop it.

## Compiling the book
*WIP*