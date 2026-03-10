# BuildKit: Modern Docker Builds

**Difficulty:** Intermediate  
**Estimated Time:** 15 minutes

## Overview

BuildKit is Docker's modern build engine that provides improved performance, better caching, and advanced features. Since Docker 23.0, BuildKit is the default builder. This guide covers BuildKit's key features and how to use them effectively.

## Prerequisites

- Understanding of [Dockerfile Syntax](00-dockerfile-syntax.md)
- Docker Engine 20.10 or later
- Familiarity with building images

## What is BuildKit?

BuildKit is a toolkit for converting source code to build artifacts in an efficient, expressive, and repeatable manner.

**Key improvements over legacy builder:**
- Parallel build execution
- Advanced caching mechanisms
- Build secrets management
- SSH agent forwarding
- Better error messages
- Automatic garbage collection

## Enabling BuildKit

### Check if BuildKit is Active

```bash
docker buildx version
```

### Enable BuildKit (if needed)

BuildKit is enabled by default in Docker 23.0+. For older versions:

**Temporary (single build):**
```bash
DOCKER_BUILDKIT=1 docker build -t myimage .
```

**Permanent (Linux/macOS):**
```bash
export DOCKER_BUILDKIT=1
```

**Permanent (Windows PowerShell):**
```powershell
$env:DOCKER_BUILDKIT=1
```

**Configuration file** (`~/.docker/config.json`):
```json
{
  "features": {
    "buildkit": true
  }
}
```

## BuildKit Features

### 1. Parallel Build Execution

BuildKit automatically parallelizes independent build stages:

```dockerfile
FROM node:18 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM node:18 AS backend
WORKDIR /app/backend
COPY backend/package*.json ./
RUN npm install
COPY backend/ .
RUN npm run build

FROM node:18-alpine
COPY --from=frontend /app/frontend/dist ./frontend
COPY --from=backend /app/backend/dist ./backend
CMD ["node", "backend/server.js"]
```

BuildKit builds `frontend` and `backend` stages in parallel!

### 2. Advanced Caching

#### Cache Mounts

Persist cache between builds:

```dockerfile
FROM node:18-alpine
WORKDIR /app

# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm install

# Cache pip packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Benefits:**
- Faster builds (reuse downloaded packages)
- Reduced network usage
- Persistent across builds

#### Bind Mounts

Mount files from build context without copying:

```dockerfile
FROM golang:1.21-alpine
WORKDIR /app

# Mount go modules cache
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=bind,source=go.mod,target=go.mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o app .
```

### 3. Build Secrets

Securely pass secrets during build without storing them in layers:

```dockerfile
FROM alpine
RUN --mount=type=secret,id=github_token \
    apk add --no-cache git && \
    git clone https://$(cat /run/secrets/github_token)@github.com/user/repo.git
```

**Build with secret:**
```bash
docker build --secret id=github_token,src=$HOME/.github-token -t myimage .
```

**Or from environment:**
```bash
docker build --secret id=github_token,env=GITHUB_TOKEN -t myimage .
```

> **Security:** Secrets are never stored in image layers or build cache.

### 4. SSH Agent Forwarding

Forward SSH agent for private repository access:

```dockerfile
FROM alpine
RUN apk add --no-cache git openssh-client
RUN mkdir -p -m 0700 ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

# Use SSH agent
RUN --mount=type=ssh \
    git clone git@github.com:user/private-repo.git
```

**Build with SSH:**
```bash
docker build --ssh default -t myimage .
```

### 5. Build Context from Git

Build directly from a Git repository:

```bash
docker build https://github.com/user/repo.git#main
```

With subdirectory:
```bash
docker build https://github.com/user/repo.git#main:subdirectory
```

### 6. Multiple Build Contexts

Use files from multiple locations:

```dockerfile
FROM alpine
COPY --from=project1 /app/config.json /config/
COPY --from=project2 /app/data.json /data/
```

**Build command:**
```bash
docker build \
  --build-context project1=../project1 \
  --build-context project2=../project2 \
  -t myimage .
```

### 7. Heredoc Syntax

Write multi-line content directly in Dockerfile:

```dockerfile
FROM alpine

# Create file with heredoc
RUN <<EOF
cat > /app/config.json <<'INNER_EOF'
{
  "server": {
    "port": 3000,
    "host": "0.0.0.0"
  }
}
INNER_EOF
EOF

# Multi-line RUN command
RUN <<EOF
apk add --no-cache \
    curl \
    vim \
    git
EOF
```

### 8. Improved Error Messages

BuildKit provides clearer error messages with context:

```
#8 [3/4] RUN npm install
#8 0.234 npm ERR! code ENOTFOUND
#8 0.234 npm ERR! errno ENOTFOUND
#8 0.234 npm ERR! network request to https://registry.npmjs.org/express failed
#8 ERROR: process "/bin/sh -c npm install" did not complete successfully: exit code: 1
```

## BuildKit Syntax

Enable BuildKit-specific features with syntax directive:

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache python3
```

**Syntax versions:**
- `docker/dockerfile:1` - Latest stable
- `docker/dockerfile:1.4` - Specific version
- `docker/dockerfile:labs` - Experimental features

## Practical Examples

### Example 1: Node.js with Cache Mounts

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18-alpine
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install with npm cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy application
COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
```

**Build:**
```bash
docker build -t node-app .
```

### Example 2: Python with Secrets

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.11-slim
WORKDIR /app

# Install from private PyPI with secret
RUN --mount=type=secret,id=pypi_token \
    --mount=type=cache,target=/root/.cache/pip \
    pip install --index-url https://$(cat /run/secrets/pypi_token)@pypi.company.com/simple \
    -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

**Build:**
```bash
docker build --secret id=pypi_token,env=PYPI_TOKEN -t python-app .
```

### Example 3: Go with Module Cache

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.21-alpine AS builder
WORKDIR /app

# Download dependencies with cache
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Build with cache
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o app .

FROM alpine:latest
COPY --from=builder /app/app /app
CMD ["/app"]
```

### Example 4: Multi-Platform Build

Build for multiple architectures:

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

In Dockerfile:
```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.21-alpine AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Building on $BUILDPLATFORM for $TARGETPLATFORM"
```

## Build Cache Management

### View Build Cache

```bash
docker buildx du
```

### Prune Build Cache

Remove unused cache:
```bash
docker buildx prune
```

Remove all cache:
```bash
docker buildx prune -a
```

### Cache Backends

#### Inline Cache

Store cache in image:
```bash
docker build --cache-to=type=inline -t myimage .
docker build --cache-from=myimage -t myimage .
```

#### Registry Cache

Store cache in registry:
```bash
docker build \
  --cache-to=type=registry,ref=myregistry.com/myapp:cache \
  --cache-from=type=registry,ref=myregistry.com/myapp:cache \
  -t myapp .
```

#### Local Cache

Store cache locally:
```bash
docker build \
  --cache-to=type=local,dest=/tmp/cache \
  --cache-from=type=local,src=/tmp/cache \
  -t myapp .
```

## BuildKit Configuration

### Daemon Configuration

Edit `/etc/docker/daemon.json`:

```json
{
  "features": {
    "buildkit": true
  },
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "10GB"
    }
  }
}
```

### Builder Instance

Create custom builder:

```bash
docker buildx create --name mybuilder --driver docker-container
docker buildx use mybuilder
docker buildx inspect --bootstrap
```

## Best Practices

1. **Use cache mounts** for package managers (npm, pip, go mod)
2. **Use secrets** for sensitive data (tokens, passwords)
3. **Enable BuildKit syntax** with `# syntax=docker/dockerfile:1`
4. **Leverage parallel builds** with multi-stage Dockerfiles
5. **Use specific syntax versions** for reproducibility
6. **Clean cache regularly** to free disk space
7. **Use registry cache** for CI/CD pipelines

## Performance Tips

### Before BuildKit

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install  # Downloads every build
COPY . .
```

**Build time:** ~60 seconds

### With BuildKit

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm install  # Cached between builds
COPY . .
```

**Build time:** ~5 seconds (subsequent builds)

## Troubleshooting

### BuildKit Not Available

```bash
# Check Docker version
docker version

# Update Docker to 20.10+
```

### Cache Not Working

```bash
# Check cache usage
docker buildx du

# Clear and rebuild
docker buildx prune -a
docker build --no-cache -t myimage .
```

### Secret Not Found

```bash
# Verify secret file exists
ls -la ~/.github-token

# Check secret ID matches
docker build --secret id=github_token,src=$HOME/.github-token .
```

## Next Steps

- Explore [Multi-Stage Builds](03-multi-stage-builds.md)
- Learn about [Image Optimization](../07-optimization/01-optimization-techniques.md)
- Understand [.dockerignore](../07-optimization/01-optimization-techniques.md#dockerignore)
- See [Simple Dockerfile Examples](02-simple-dockerfile.md)

## Additional Resources

- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Dockerfile Frontend Syntax](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md)
- [Build Cache Documentation](https://docs.docker.com/build/cache/)
- [BuildX Documentation](https://docs.docker.com/buildx/working-with-buildx/)
