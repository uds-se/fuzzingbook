# How to: Install the interactive fuzzing book on a local docker container

## Step 1: Install Docker
Follow the installation procedure recommended at docker.com, or, if you are using Linux, refer to your distribution for information on the installation process.

Once installed, make sure Docker works by typing `docker info` in a shell. If there are no errors, you can proceed to Step 2.

## Step 2: Set up the image
Run the following command to build the docker image for the book container:
```bash
docker build --build-arg publish=no -t 'fuzzing-book' fuzzingbook-dockerenv
```

If you want to contribute to the book or generate static builds of the book (HTML, slides, etc.) please use the publish argument:
```bash
docker build --build-arg publish=yes -t 'fuzzing-book' fuzzingbook-dockerenv
```

These commands are also available as scripts in `bin/create-(publish/student)-build`.

## Step 3: Creating an instance of the image
Run the following command to start up an instance of the fuzzing book container for the first time and connect it to your local port 8888.

```bash
docker run -d -p 8888:8888 --name fuzzing-book-instance fuzzing-book
```

Now just follow the instructions to open the notebook in your browser. You can close the terminal window now, the container will keep running in the background until you stop it. If you can't find the link, run:
```bash
docker exec -it fuzzing-book-instance jupyter notebook list
```

# Notes
--------------------------------------
## `bin` directory
The bin folder contains many of the instructions here as shorthand-scripts.

## Stopping the container
```bash
docker stop fuzzing-book-instance
```

## Restarting an existing container
```bash
docker stop fuzzing-book-instance
```

```bash
docker start fuzzing-book-instance
```

## Updating the book
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

## Uninstalling
To delete the docker container and image, execute the following commands:
```shell
docker stop fuzzing-book-instance
docker rm fuzzing-book-instance
docker rmi fuzzing-book
```

## 'Make'ing the book/ Generating static book
If you have a container built with the publish option, you can use the `bin/make` script to obtain the HTML, Markdown, Word, Slides and static code versions of the book. A folder called build-output will be generated containing the items.