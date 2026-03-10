# Docker Architecture

**Difficulty:** Beginner  
**Estimated Time:** 10 minutes

## Overview

Understanding Docker's architecture helps you grasp how containers work and how Docker components interact. This guide explains the core components and their relationships.

## Docker Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Client                        │
│                   (docker CLI)                          │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Docker Daemon                          │
│                  (dockerd)                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Container Runtime                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │  │
│  │  │Container │  │Container │  │Container │       │  │
│  │  │    1     │  │    2     │  │    3     │       │  │
│  │  └──────────┘  └──────────┘  └──────────┘       │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Docker Registry                        │
│                  (Docker Hub, etc.)                     │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### Docker Client

The Docker client (`docker`) is the primary way users interact with Docker. When you run commands like `docker run`, the client sends these commands to the Docker daemon via the REST API.

**Key characteristics:**
- Command-line interface (CLI)
- Communicates with daemon via REST API
- Can connect to remote daemons
- Includes `docker compose` for multi-container applications

**Example:**
```bash
docker run nginx
docker compose up
docker build -t myapp .
```

### Docker Daemon

The Docker daemon (`dockerd`) is the background service that manages Docker objects like images, containers, networks, and volumes.

**Responsibilities:**
- Listens for Docker API requests
- Manages container lifecycle
- Handles image building and storage
- Manages networks and volumes
- Communicates with other daemons

**Key features:**
- Runs as a system service
- Can be configured via `/etc/docker/daemon.json`
- Supports remote API access
- Manages BuildKit for image builds

### Docker Registry

A Docker registry stores Docker images. Docker Hub is the default public registry, but you can run private registries.

**Functions:**
- Stores and distributes images
- Supports image versioning (tags)
- Provides access control
- Enables image sharing

**Common registries:**
- Docker Hub (hub.docker.com)
- GitHub Container Registry
- Amazon ECR
- Google Container Registry
- Private registries

## Docker Objects

### Images

An image is a read-only template with instructions for creating a container. Images are built from a Dockerfile and can be based on other images.

**Characteristics:**
- Immutable (read-only)
- Composed of layers
- Stored in registries
- Identified by name and tag

**Example:**
```bash
docker pull nginx:latest
docker images
```

### Containers

A container is a runnable instance of an image. You can create, start, stop, move, or delete containers using the Docker API or CLI.

**Characteristics:**
- Isolated from other containers and host
- Has its own filesystem, networking, and process space
- Ephemeral by default (data lost when removed)
- Can be connected to networks and storage

**Example:**
```bash
docker run -d --name webserver nginx
docker ps
docker stop webserver
```

### Networks

Docker networks enable containers to communicate with each other and with external systems.

**Network types:**
- **bridge:** Default network for containers on same host
- **host:** Container uses host's network directly
- **overlay:** Enables communication across multiple Docker hosts
- **none:** Disables networking

**Example:**
```bash
docker network create mynetwork
docker run --network mynetwork nginx
```

### Volumes

Volumes are the preferred mechanism for persisting data generated and used by Docker containers.

**Benefits:**
- Data persists after container removal
- Can be shared between containers
- Easier to back up and migrate
- Work on both Linux and Windows

**Example:**
```bash
docker volume create mydata
docker run --mount source=mydata,target=/data nginx
```

## How Docker Works

### Container Lifecycle

1. **Pull Image:** Docker pulls the image from a registry
2. **Create Container:** Docker creates a container from the image
3. **Start Container:** Docker starts the container process
4. **Run:** Container executes its main process
5. **Stop:** Container process is stopped
6. **Remove:** Container is deleted (image remains)

### Image Layers

Docker images are built in layers. Each instruction in a Dockerfile creates a new layer:

```dockerfile
FROM ubuntu:22.04        # Layer 1: Base image
RUN apt-get update       # Layer 2: Update packages
RUN apt-get install -y nginx  # Layer 3: Install nginx
COPY index.html /var/www/html/  # Layer 4: Copy file
```

**Benefits of layers:**
- Efficient storage (shared layers)
- Faster builds (cached layers)
- Smaller image transfers

### BuildKit

Modern Docker uses BuildKit as the default build engine, providing:
- Parallel build execution
- Build cache optimization
- Secrets management during builds
- Better error messages

## Docker vs Virtual Machines

| Feature | Docker Containers | Virtual Machines |
|---------|------------------|------------------|
| Startup time | Seconds | Minutes |
| Size | Megabytes | Gigabytes |
| Performance | Near-native | Overhead from hypervisor |
| Isolation | Process-level | Hardware-level |
| OS | Shares host kernel | Full OS per VM |

## Security Considerations

Docker provides multiple layers of security:

- **Namespaces:** Isolate container processes
- **Control groups (cgroups):** Limit resource usage
- **Union file systems:** Provide isolated filesystems
- **Security profiles:** AppArmor, SELinux support
- **User namespaces:** Map container users to host users

> **Tip:** Always run containers as non-root users when possible using the `USER` instruction in Dockerfiles.

## Next Steps

Now that you understand Docker's architecture:
- Learn about [Working with Images](../02-fundamentals/01-working-with-images.md)
- Explore [Container Basics](../02-fundamentals/02-container-basics.md)
- Try [Basic Commands](03-basic-commands.md)

## Additional Resources

- [Docker Architecture Documentation](https://docs.docker.com/get-started/overview/)
- [Docker Engine Documentation](https://docs.docker.com/engine/)
- [Container Runtime Documentation](https://docs.docker.com/engine/reference/run/)
