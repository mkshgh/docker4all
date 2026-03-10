# DockerFiles

Reference: https://docs.docker.com/engine/reference/builder/
Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an automated build that executes several command-line instructions in succession.

## Things to remember:

- Dockerfiles look like shell srcipts.
- Dockerfiles are not shell srcipts.
- Process running on one line line will not be running on the second line.

    - Each line takes the image from previous line and makes a new image.
    - previous image is unchanged.
    - It doesn't edit the change from previous line.
    - If you want to download a large file and do some opertaions and delete it. Do it in one line. This is for space
    - If you have dependent scripts run it in one line as the next line will not have access to previous line.

- Avoid Golden images


## Docker build command

```bash
# location_of_docker_file: . if in current directory
# -t means tag with a image_name

docker build -t <new_image_name> <location_of_docker_file>
```
## Dockerfile Syntax:

The format of the instructions is:

```bash
# Comment
INSTRUCTION arguments
```
## RUN Command

1. Docker treats lines that begin with # as a comment, unless the line is a valid parser directive. A # marker anywhere else in a line is treated as an argument. This allows statements like:


```bash
# Comment
RUN echo 'we are running some # of cool things'
```

1. Comment lines are removed before the Dockerfile instructions are executed. So both are same here

```bash
------------------
RUN echo hello \
# comment
world
```
    ------------------
    RUN echo hello \
    world

3. Whitespaces are ignored, but discouraged.


```bash
------------------------------------------------------
        # this is a comment-line
    RUN echo hello
RUN echo world
```
    ------------------------------------------------------
    # this is a comment-line
    RUN echo hello
    RUN echo world

## Environment Vairables

1. Example

```bash
FROM busybox
ENV FOO=/bar
WORKDIR ${FOO}   # WORKDIR /bar
ADD . $FOO       # ADD . /bar
COPY \$FOO /quux # COPY $FOO /quux
```
2. Environment Vairables are supported by the following instructions in dockerfiles:

- ADD
- COPY
- ENV
- EXPOSE
- FROM
- LABEL
- STOPSIGNAL
- USER
- VOLUME
- WORKDIR
- ONBUILD (when combined with one of the supported instructions above)

3. Environment Vairables inside Environment Vairables

```bash
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```
4. .dockerignore file

It excludes files and directories that match patterns in it.

```bash
# comment
*/temp*
*/*/temp*
temp?
```