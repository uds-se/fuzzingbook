# Run with Docker

The first step is to download and install [Docker](https://www.docker.com/). Follow the installation procedure recommended at docker.com, or, if you are using Linux, refer to your distribution for information on the installation process.

Once installed, make sure Docker works by typing `docker info` in a shell.

## Running with our precompiled image

We recommend that you use our precompiled image to run the fuzzingbook locally. Our precompiled image is available in the DockerHub servers and you can pull it with the following command.

```bash
docker pull fuzzingbook/student
```

Once the download is complete you can run the image with:

```bash
docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzingbook/student
```

And copy the link from the terminal into your browser to execute it. If you don’t see a link you can execute: 

```bash
docker exec -it fuzzing-book-instance jupyter notebook list
```

Once the container is started it will keep running in the background until you stop it.

## Build the Docker image yourself

Run the following command to build the docker image for the book container:

```bash
docker build --build-arg publish=no -t 'fuzzing-book' fuzzingbook-dockerenv
```

If you want to contribute to the book or generate static builds of the book (HTML, slides, etc.) please use the publish argument:

```bash
docker build --build-arg publish=yes -t 'fuzzing-book' fuzzingbook-dockerenv
```

These commands are also available as scripts in `bin/create-(publish/student)-build`.

Finally, run the following command to start up an instance of the fuzzing book container for the first time and connect it to your local port 8888. You can then follow the instructions to open the notebook in your browser.

```bash
docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book
```

Now just follow the instructions to open the notebook in your browser. You can close the terminal window now, the container will keep running in the background until you stop it. If you can't find the link, run:
```bash
docker exec -it fuzzing-book-instance jupyter notebook list
```

# Deploy a JupyterHub to local server

If you want to install the fuzzingbook in a server, to be used by multiple users during a lecture we recommend you to use the official [jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker)

We provide a precompiled image which works with this setup.

First, pull our precompiled `user` image with the following command:

```bash
docker pull fuzzingbook/user
```

Then configure the `DOCKER_NOTEBOOK_IMAGE` environment variable to point to `fuzzingbook/user`. This variable is used by the Docker spawner process. 
Finally, follow [these instructions](https://github.com/jupyterhub/jupyterhub-deploy-docker/blob/master/README.md) to finish setting up the server.

__Note:__ We recommend you to add a redirection from the default HTTP port (80) to the HTTPS port (443). You can use a Docker container to  

### Notes

#### `bin` directory
The bin folder contains many of the instructions here as shorthand-scripts.

#### Stopping the container
```bash
docker stop fuzzing-book-instance
```

#### Restarting an existing container
```bash
docker stop fuzzing-book-instance
docker start fuzzing-book-instance
```

#### Updating the book
The book auto-updates every time the container is started, but if you made changes that prevent an update due to merge conflicts, you will have to manually resolve them in a console:
```bash
docker exec -it fuzzing-book-instance bash
cd fuzzingbook
<pull and solve merge conflicts>
```

or toss your changes and reset the repository:
```bash
docker exec -it fuzzing-book-instance bash
cd fuzzingbook
git reset --hard
git pull
```

#### Uninstalling
To delete the docker container and image, execute the following commands:
```shell
docker stop fuzzing-book-instance
docker rm fuzzing-book-instance
docker rmi fuzzing-book
```

#### Making the book/ Generating static book
If you have a container built with the publish option, you can use the `bin/make` script to obtain the HTML, Markdown, Word, Slides and static code versions of the book. A folder called build-output will be generated containing the items.
