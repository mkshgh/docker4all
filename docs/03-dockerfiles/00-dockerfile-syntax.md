# Dockerfile Syntax and Best Practices

**Difficulty:** Intermediate  
**Estimated Time:** 20 minutes

## Overview

A Dockerfile is a text file containing instructions for building a Docker image. This guide covers Dockerfile syntax, common instructions, and best practices for writing efficient, maintainable Dockerfiles.

## Prerequisites

- Understanding of [Images and Containers](../01-getting-started/04-images-containers.md)
- Familiarity with [Basic Commands](../01-getting-started/03-basic-commands.md)
- Basic Linux command-line knowledge

## Dockerfile Basics

### What is a Dockerfile?

A Dockerfile is a script that contains a series of instructions for building a Docker image. Each instruction creates a new layer in the image.

### Basic Structure

```dockerfile
# Comment
INSTRUCTION arguments
```

**Example:**
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
CMD ["nginx", "-g", "daemon off;"]
```

### Building an Image

```bash
docker build -t myimage:v1.0 .
```

**Flags:**
- `-t`: Tag the image with a name
- `.`: Build context (current directory)
- `-f`: Specify Dockerfile name (default: `Dockerfile`)

## Core Instructions

### FROM

Specifies the base image. Every Dockerfile must start with `FROM`.

```dockerfile
FROM ubuntu:22.04
```

**Best practices:**
- Use specific tags, not `latest`
- Prefer official images
- Use minimal base images (Alpine) when possible

**Examples:**
```dockerfile
FROM node:18-alpine
FROM python:3.11-slim
FROM nginx:1.25
```

### RUN

Executes commands during image build. Creates a new layer.

```dockerfile
RUN apt-get update && apt-get install -y curl
```

**Best practices:**
- Chain commands with `&&` to reduce layers
- Clean up in the same layer
- Use `\` for multi-line commands

**Good example:**
```dockerfile
RUN apt-get update && \
    apt-get install -y \
        curl \
        vim \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**Bad example:**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y git
# Creates 4 layers instead of 1
```

### COPY

Copies files from build context to image.

```dockerfile
COPY source destination
```

**Examples:**
```dockerfile
COPY index.html /var/www/html/
COPY package*.json ./
COPY --chown=node:node . /app
```

**Best practices:**
- Copy only what you need
- Use `.dockerignore` to exclude files
- Copy dependency files before application code (for caching)

### ADD

Similar to COPY but with additional features (URL support, auto-extraction).

```dockerfile
ADD archive.tar.gz /app/
```

> **Note:** Prefer `COPY` unless you need `ADD`'s special features.

### WORKDIR

Sets the working directory for subsequent instructions.

```dockerfile
WORKDIR /app
```

**Example:**
```dockerfile
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
```

**Best practices:**
- Use absolute paths
- Create directory if it doesn't exist
- Prefer `WORKDIR` over `RUN cd`

### CMD

Specifies the default command to run when container starts.

```dockerfile
CMD ["executable", "param1", "param2"]
```

**Forms:**
- **Exec form (preferred):** `CMD ["nginx", "-g", "daemon off;"]`
- **Shell form:** `CMD nginx -g "daemon off;"`

**Examples:**
```dockerfile
CMD ["python", "app.py"]
CMD ["node", "server.js"]
CMD ["npm", "start"]
```

> **Note:** Only the last `CMD` in a Dockerfile takes effect.

### ENTRYPOINT

Configures container to run as an executable.

```dockerfile
ENTRYPOINT ["executable"]
```

**Example:**
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
# Runs: python app.py
# Can override CMD: docker run myimage script.py
```

**ENTRYPOINT vs CMD:**
- `ENTRYPOINT`: Defines the executable
- `CMD`: Provides default arguments
- Both can be overridden at runtime

### ENV

Sets environment variables.

```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
```

**Multi-line:**
```dockerfile
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=info
```

**Usage in Dockerfile:**
```dockerfile
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . $APP_HOME
```

### ARG

Defines build-time variables.

```dockerfile
ARG VERSION=1.0
ARG BUILD_DATE
```

**Usage:**
```dockerfile
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine
```

**Build with arguments:**
```bash
docker build --build-arg NODE_VERSION=20 -t myapp .
```

**ARG vs ENV:**
- `ARG`: Available only during build
- `ENV`: Available during build and runtime

### EXPOSE

Documents which ports the container listens on.

```dockerfile
EXPOSE 80
EXPOSE 443
```

> **Note:** `EXPOSE` is documentation only. Use `-p` flag to actually publish ports.

```bash
docker run -p 8080:80 myimage
```

### VOLUME

Creates a mount point for persistent data.

```dockerfile
VOLUME /data
```

**Example:**
```dockerfile
VOLUME /var/lib/mysql
VOLUME /var/log/nginx
```

### USER

Sets the user for subsequent instructions.

```dockerfile
USER node
```

**Best practice example:**
```dockerfile
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs
WORKDIR /app
COPY --chown=nodejs:nodejs . .
CMD ["node", "server.js"]
```

> **Security:** Always run containers as non-root users in production.

### LABEL

Adds metadata to image.

```dockerfile
LABEL version="1.0"
LABEL description="My application"
LABEL maintainer="dev@example.com"
```

**Multi-line:**
```dockerfile
LABEL version="1.0" \
      description="My application" \
      maintainer="dev@example.com"
```

## Instruction Ordering

Order matters for build cache efficiency:

```dockerfile
# 1. Base image
FROM node:18-alpine

# 2. Metadata
LABEL maintainer="dev@example.com"

# 3. Install system dependencies (changes rarely)
RUN apk add --no-cache python3 make g++

# 4. Set working directory
WORKDIR /app

# 5. Copy dependency files (changes less frequently)
COPY package*.json ./

# 6. Install dependencies
RUN npm ci --only=production

# 7. Copy application code (changes frequently)
COPY . .

# 8. Set runtime configuration
ENV NODE_ENV=production
EXPOSE 3000

# 9. Set user
USER node

# 10. Define startup command
CMD ["node", "server.js"]
```

**Principle:** Place instructions that change less frequently at the top.

## Layer Optimization

### Understanding Layers

Each instruction creates a layer:

```dockerfile
FROM ubuntu:22.04          # Layer 1
RUN apt-get update         # Layer 2
RUN apt-get install -y curl # Layer 3
COPY app.py /app/          # Layer 4
```

### Reducing Layers

Combine related commands:

```dockerfile
# Bad: 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good: 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Build Cache

Docker caches layers. If a layer hasn't changed, Docker reuses it:

```dockerfile
FROM node:18-alpine
WORKDIR /app

# This layer is cached if package.json hasn't changed
COPY package*.json ./
RUN npm install

# This layer rebuilds when code changes
COPY . .
```

**Cache invalidation:** Any change invalidates that layer and all subsequent layers.

## Best Practices

### 1. Use .dockerignore

Create a `.dockerignore` file to exclude unnecessary files:

```
node_modules
npm-debug.log
.git
.env
*.md
.vscode
```

### 2. Minimize Layer Count

Combine related operations:

```dockerfile
RUN apt-get update && \
    apt-get install -y package1 package2 && \
    apt-get clean
```

### 3. Leverage Build Cache

Order instructions from least to most frequently changing:

```dockerfile
COPY package.json .    # Changes rarely
RUN npm install        # Cached if package.json unchanged
COPY . .              # Changes frequently
```

### 4. Use Multi-Stage Builds

Separate build and runtime environments (covered in [Multi-Stage Builds](03-multi-stage-builds.md)):

```dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]
```

### 5. Run as Non-Root User

```dockerfile
USER node
# or create a custom user
RUN adduser -D appuser
USER appuser
```

### 6. Use Specific Tags

```dockerfile
# Bad
FROM node:latest

# Good
FROM node:18.17-alpine3.18
```

### 7. Clean Up in Same Layer

```dockerfile
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Complete Example

```dockerfile
# Use specific base image
FROM node:18.17-alpine3.18

# Add metadata
LABEL maintainer="dev@example.com" \
      version="1.0.0" \
      description="Node.js web application"

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++

# Create app directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000

# Expose port
EXPOSE 3000

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node healthcheck.js

# Start application
CMD ["node", "server.js"]
```

## Common Patterns

### Node.js Application

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

### Python Application

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER nobody
EXPOSE 8000
CMD ["python", "app.py"]
```

### Static Website

```dockerfile
FROM nginx:1.25-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Troubleshooting

### Build Fails at RUN Instruction

Check the command works locally first:
```bash
docker run -it ubuntu:22.04 bash
# Test your command here
```

### Cache Not Working

Force rebuild without cache:
```bash
docker build --no-cache -t myimage .
```

### Image Too Large

- Use Alpine base images
- Clean up in same layer
- Use multi-stage builds
- Check with `docker history myimage`

## Next Steps

- Learn about [BuildKit Features](02-buildkit.md)
- Explore [Multi-Stage Builds](03-multi-stage-builds.md)
- See [Simple Dockerfile Examples](02-simple-dockerfile.md)
- Understand [Image Optimization](../07-optimization/01-optimization-techniques.md)

## Additional Resources

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Best Practices Guide](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
