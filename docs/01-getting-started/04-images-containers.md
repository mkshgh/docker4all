# Images and Containers Fundamentals

**Difficulty:** Beginner  
**Estimated Time:** 15 minutes

## Overview

Understanding the relationship between images and containers is fundamental to working with Docker. This guide explains what images and containers are, how they relate to each other, and how to work with them effectively.

## Prerequisites

- Docker installed and running
- Familiarity with [Basic Commands](03-basic-commands.md)
- Understanding of [Docker Architecture](02-docker-architecture.md)

## What is a Docker Image?

A Docker image is a **read-only template** that contains:
- Application code
- Runtime environment
- System libraries
- Dependencies
- Configuration files

Think of an image as a **blueprint** or **recipe** for creating containers.

### Image Characteristics

- **Immutable:** Once created, images don't change
- **Layered:** Built from multiple layers stacked on top of each other
- **Portable:** Can be shared via registries
- **Versioned:** Tagged with versions (e.g., `nginx:1.25`, `ubuntu:22.04`)

### Image Layers

Images are composed of layers. Each layer represents a set of filesystem changes:

```
┌─────────────────────────────┐
│   Application Layer         │  ← Your app code
├─────────────────────────────┤
│   Dependencies Layer        │  ← npm install, pip install
├─────────────────────────────┤
│   Runtime Layer             │  ← Node.js, Python
├─────────────────────────────┤
│   Base OS Layer             │  ← Ubuntu, Alpine
└─────────────────────────────┘
```

**Benefits of layers:**
- **Efficiency:** Layers are cached and reused
- **Speed:** Only changed layers need to be downloaded/uploaded
- **Storage:** Shared layers save disk space

### Viewing Image Layers

```bash
docker history nginx:latest
```

Output shows each layer with its size and creation command.

## What is a Docker Container?

A container is a **runnable instance** of an image. It's what you get when you execute an image.

Think of a container as a **running application** created from the image blueprint.

### Container Characteristics

- **Isolated:** Has its own filesystem, network, and process space
- **Ephemeral:** Data is lost when container is removed (unless using volumes)
- **Lightweight:** Shares the host OS kernel
- **Mutable:** Can be modified while running (but changes are lost on removal)

### Image vs Container Analogy

| Concept | Image | Container |
|---------|-------|-----------|
| Programming | Class | Object/Instance |
| Cooking | Recipe | Prepared dish |
| Construction | Blueprint | Building |
| Music | Sheet music | Performance |

## The Relationship

```
┌──────────────┐
│    Image     │  (Read-only template)
│   nginx:1.25 │
└──────┬───────┘
       │ docker run
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────────┐ ┌──────────────┐
│  Container 1 │ │  Container 2 │  (Running instances)
│   webserver  │ │   api-server │
└──────────────┘ └──────────────┘
```

**Key points:**
- One image can create many containers
- Containers are independent of each other
- Removing a container doesn't affect the image
- Removing an image doesn't affect running containers

## Working with Images

### Pulling Images

Download an image from a registry:

```bash
docker pull ubuntu:22.04
```

### Listing Images

View all local images:

```bash
docker images
```

Output:
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       22.04     abc123def456   2 weeks ago    77.8MB
nginx        latest    def456abc789   1 week ago     142MB
```

### Image Naming

Images follow this naming convention:

```
[registry/][username/]repository[:tag]
```

**Examples:**
- `nginx` → Docker Hub official image, latest tag
- `nginx:1.25` → Docker Hub official image, version 1.25
- `ubuntu:22.04` → Ubuntu version 22.04
- `myusername/myapp:v1.0` → User image with version tag
- `ghcr.io/owner/repo:latest` → GitHub Container Registry image

### Tagging Images

Create a new tag for an existing image:

```bash
docker tag nginx:latest mynginx:v1.0
```

### Removing Images

Remove an image:

```bash
docker rmi ubuntu:22.04
```

> **Note:** You cannot remove an image if containers (even stopped ones) are using it.

## Working with Containers

### Creating Containers

Create a container from an image:

```bash
docker run nginx
```

With options:

```bash
docker run -d --name webserver -p 8080:80 nginx
```

### Container Lifecycle

```
┌─────────┐
│ Created │  ← docker create
└────┬────┘
     │ docker start
     ▼
┌─────────┐
│ Running │  ← docker run (create + start)
└────┬────┘
     │ docker stop
     ▼
┌─────────┐
│ Stopped │
└────┬────┘
     │ docker rm
     ▼
┌─────────┐
│ Removed │
└─────────┘
```

### Container States

Check container status:

```bash
docker ps -a
```

**Possible states:**
- **Created:** Container created but not started
- **Running:** Container is executing
- **Paused:** Container processes are paused
- **Exited:** Container stopped (exit code shown)
- **Dead:** Container failed to stop properly

### Inspecting Containers

Get detailed information:

```bash
docker inspect webserver
```

Get specific field:

```bash
docker inspect --format='{{.State.Status}}' webserver
```

## Practical Examples

### Example 1: Understanding Image Reuse

```bash
# Pull an image once
docker pull nginx

# Create multiple containers from the same image
docker run -d --name web1 -p 8081:80 nginx
docker run -d --name web2 -p 8082:80 nginx
docker run -d --name web3 -p 8083:80 nginx

# All three containers share the same image layers
docker ps

# Clean up
docker stop web1 web2 web3
docker rm web1 web2 web3
```

### Example 2: Container Modifications Don't Affect Image

```bash
# Run a container
docker run -it --name myubuntu ubuntu bash

# Inside container, make changes
apt-get update
apt-get install -y curl
curl --version

# Exit container
exit

# Start a new container from the same image
docker run -it --name myubuntu2 ubuntu bash

# Inside new container, curl is NOT installed
curl --version  # Command not found

# Exit and clean up
exit
docker rm myubuntu myubuntu2
```

### Example 3: Creating an Image from a Container

```bash
# Run and modify a container
docker run -it --name customubuntu ubuntu bash
# Inside: apt-get update && apt-get install -y curl
exit

# Create a new image from the modified container
docker commit customubuntu ubuntu-with-curl

# Now you can create containers with curl pre-installed
docker run --rm ubuntu-with-curl curl --version

# Clean up
docker rm customubuntu
docker rmi ubuntu-with-curl
```

> **Note:** Using `docker commit` is not recommended for production. Use Dockerfiles instead (covered in [Dockerfile Fundamentals](../03-dockerfiles/01-dockerfile-fundamentals.md)).

## Image Layers in Detail

### Viewing Layers

```bash
docker history nginx:latest
```

Output shows:
- Layer size
- Creation date
- Command that created the layer

### Layer Caching

Docker caches layers to speed up builds and pulls:

```bash
# First pull downloads all layers
docker pull nginx:1.25

# Pulling a similar image reuses shared layers
docker pull nginx:1.24  # Only downloads different layers
```

### Storage Drivers

Docker uses storage drivers to manage image layers:
- **overlay2:** Most common, recommended for Linux
- **aufs:** Older driver
- **devicemapper:** For older systems

Check your storage driver:

```bash
docker info | grep "Storage Driver"
```

## Container Filesystem

### Read-Only Image Layers

All image layers are read-only. When you run a container, Docker adds a thin writable layer on top:

```
┌─────────────────────────────┐
│  Writable Container Layer   │  ← Changes made here
├─────────────────────────────┤
│  Read-Only Image Layers     │  ← Shared, immutable
└─────────────────────────────┘
```

### Copy-on-Write

When a container modifies a file from an image layer:
1. Docker copies the file to the writable layer
2. Modifications happen in the copy
3. Original file in image layer remains unchanged

## Best Practices

1. **Use official images:** Start with official images from Docker Hub
2. **Specify tags:** Use specific version tags, not `latest`
3. **Keep images small:** Use minimal base images like Alpine
4. **One process per container:** Each container should run one main process
5. **Don't store data in containers:** Use volumes for persistent data
6. **Clean up regularly:** Remove unused images and containers

## Common Patterns

### Running Temporary Containers

```bash
# Auto-remove after exit
docker run --rm -it alpine sh
```

### Background Services

```bash
# Run as daemon
docker run -d --name database postgres
```

### Interactive Development

```bash
# Mount local code, run interactively
docker run -it --rm --mount type=bind,source=$(pwd),target=/app -w /app node:18 bash
```

## Troubleshooting

### "No space left on device"

```bash
# Clean up unused images and containers
docker system prune -a
```

### "Image not found"

```bash
# Pull the image first
docker pull <image-name>
```

### "Container name already exists"

```bash
# Remove the old container
docker rm <container-name>
# Or use a different name
```

## Next Steps

Now that you understand images and containers:
- Learn to create custom images with [Dockerfile Fundamentals](../03-dockerfiles/01-dockerfile-fundamentals.md)
- Explore [Container Lifecycle](../02-fundamentals/03-container-lifecycle.md)
- Understand [Port Mapping](../02-fundamentals/06-port-mapping.md)
- Learn about [Volumes](../06-volumes/01-volume-basics.md) for persistent data

## Additional Resources

- [Docker Images Documentation](https://docs.docker.com/engine/reference/commandline/images/)
- [Docker Containers Documentation](https://docs.docker.com/engine/reference/commandline/container/)
- [Image Layer Documentation](https://docs.docker.com/storage/storagedriver/)
