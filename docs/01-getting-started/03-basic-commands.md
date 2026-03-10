# Docker Basic Commands

**Difficulty:** Beginner  
**Estimated Time:** 15 minutes

## Overview

This guide covers essential Docker commands you'll use daily. By the end, you'll be comfortable running containers, managing images, and performing basic Docker operations.

## Prerequisites

- Docker installed and running
- Completed [Installation and Setup](01-installation-setup.md)
- Basic understanding of [Docker Architecture](02-docker-architecture.md)

## Essential Commands

### Working with Images

#### List Images

View all images on your system:

```bash
docker images
```

Or use the newer syntax:

```bash
docker image ls
```

**Output example:**
```
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
nginx         latest    abc123def456   2 weeks ago    142MB
ubuntu        22.04     def456abc789   3 weeks ago    77.8MB
```

#### Pull an Image

Download an image from Docker Hub:

```bash
docker pull nginx
```

Pull a specific version:

```bash
docker pull nginx:1.25
docker pull ubuntu:22.04
```

> **Note:** If you don't specify a tag, Docker pulls the `latest` tag by default.

#### Remove an Image

Delete an image from your system:

```bash
docker rmi nginx
```

Or use the image ID:

```bash
docker rmi abc123def456
```

Remove multiple images:

```bash
docker rmi nginx ubuntu alpine
```

### Working with Containers

#### Run a Container

Start a new container from an image:

```bash
docker run nginx
```

**Common flags:**
- `-d`: Run in detached mode (background)
- `-it`: Interactive mode with terminal
- `--name`: Assign a name to the container
- `-p`: Publish ports
- `--rm`: Automatically remove container when it stops

**Examples:**

Run in background:
```bash
docker run -d nginx
```

Run with a custom name:
```bash
docker run -d --name webserver nginx
```

Run interactively:
```bash
docker run -it ubuntu bash
```

Run and remove after exit:
```bash
docker run --rm -it alpine sh
```

#### List Containers

View running containers:

```bash
docker ps
```

View all containers (including stopped):

```bash
docker ps -a
```

**Output example:**
```
CONTAINER ID   IMAGE     COMMAND                  STATUS         PORTS     NAMES
abc123def456   nginx     "/docker-entrypoint.…"   Up 2 minutes   80/tcp    webserver
```

#### Stop a Container

Stop a running container:

```bash
docker stop webserver
```

Or use the container ID:

```bash
docker stop abc123def456
```

Stop multiple containers:

```bash
docker stop webserver database cache
```

#### Start a Stopped Container

Restart a stopped container:

```bash
docker start webserver
```

#### Restart a Container

Restart a running container:

```bash
docker restart webserver
```

#### Remove a Container

Delete a stopped container:

```bash
docker rm webserver
```

Force remove a running container:

```bash
docker rm -f webserver
```

Remove all stopped containers:

```bash
docker container prune
```

### Container Interaction

#### Execute Commands in Running Container

Run a command in a running container:

```bash
docker exec webserver ls /usr/share/nginx/html
```

Open an interactive shell:

```bash
docker exec -it webserver bash
```

> **Tip:** Use `sh` instead of `bash` for Alpine-based images.

#### View Container Logs

See container output:

```bash
docker logs webserver
```

Follow logs in real-time:

```bash
docker logs -f webserver
```

Show last 100 lines:

```bash
docker logs --tail 100 webserver
```

#### Inspect Container

View detailed container information:

```bash
docker inspect webserver
```

Get specific information using format:

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' webserver
```

#### View Container Stats

Monitor resource usage:

```bash
docker stats
```

For a specific container:

```bash
docker stats webserver
```

## Practical Examples

### Example 1: Run a Web Server

```bash
# Pull nginx image
docker pull nginx

# Run nginx in background with port mapping
docker run -d --name mynginx -p 8080:80 nginx

# Verify it's running
docker ps

# Test in browser or with curl
curl http://localhost:8080

# View logs
docker logs mynginx

# Stop and remove
docker stop mynginx
docker rm mynginx
```

### Example 2: Interactive Ubuntu Container

```bash
# Run Ubuntu interactively
docker run -it --name myubuntu ubuntu bash

# Inside the container, try some commands:
apt-get update
apt-get install -y curl
curl --version

# Exit the container
exit

# Container is stopped but not removed
docker ps -a

# Restart and attach
docker start myubuntu
docker attach myubuntu

# Clean up
docker rm myubuntu
```

### Example 3: Temporary Container

```bash
# Run a container that auto-removes after exit
docker run --rm -it alpine sh

# Inside container
echo "This container will be removed on exit"
exit

# Container is automatically removed
docker ps -a  # Won't show the alpine container
```

## Bulk Operations

### Remove All Stopped Containers

```bash
docker container prune
```

### Remove All Unused Images

```bash
docker image prune
```

### Remove Everything (Containers, Images, Networks, Volumes)

```bash
docker system prune -a
```

> **Warning:** This removes all stopped containers, unused networks, dangling images, and build cache. Use with caution!

### Stop All Running Containers

```bash
docker stop $(docker ps -q)
```

### Remove All Containers

```bash
docker rm $(docker ps -a -q)
```

### Remove All Images

```bash
docker rmi $(docker images -q)
```

## Command Cheat Sheet

| Task | Command |
|------|---------|
| Pull image | `docker pull <image>` |
| List images | `docker images` |
| Remove image | `docker rmi <image>` |
| Run container | `docker run <image>` |
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| Stop container | `docker stop <container>` |
| Start container | `docker start <container>` |
| Remove container | `docker rm <container>` |
| View logs | `docker logs <container>` |
| Execute command | `docker exec <container> <command>` |
| Interactive shell | `docker exec -it <container> bash` |
| Container stats | `docker stats` |
| Inspect container | `docker inspect <container>` |

## Tips and Best Practices

1. **Use meaningful names:** Always name your containers with `--name` for easier management
2. **Clean up regularly:** Use `docker system prune` to free up disk space
3. **Use --rm for temporary containers:** Automatically remove containers you don't need to keep
4. **Check logs first:** When troubleshooting, always check `docker logs` first
5. **Use specific tags:** Avoid `latest` in production; use specific version tags

## Common Issues

### "Container name already in use"

```bash
# Remove the existing container first
docker rm old-container-name
# Or use a different name
docker run --name new-container-name nginx
```

### "Port already allocated"

```bash
# Use a different host port
docker run -p 8081:80 nginx
# Or stop the container using that port
docker ps  # Find the container
docker stop <container-name>
```

### "Cannot remove running container"

```bash
# Stop it first
docker stop <container>
docker rm <container>
# Or force remove
docker rm -f <container>
```

## Next Steps

Now that you know the basic commands:
- Learn about [Working with Images](../02-fundamentals/01-working-with-images.md) in detail
- Explore [Container Basics](../02-fundamentals/02-container-basics.md)
- Understand [Port Mapping](../02-fundamentals/06-port-mapping.md)

## Additional Resources

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Docker Exec Reference](https://docs.docker.com/engine/reference/commandline/exec/)
