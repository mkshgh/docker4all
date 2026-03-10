# Hello World Example

The simplest possible Docker example.

## What This Demonstrates

- Basic Dockerfile syntax
- Using Alpine Linux (minimal base image)
- Running a simple script in a container

## How to Run

```bash
# Build the image
docker build -t hello-world-example .

# Run the container
docker run hello-world-example

# Run multiple times to see different container IDs
docker run hello-world-example
docker run hello-world-example
```

## Expected Output

```
Hello from Docker!
Container ID: abc123def456
Current time: Sat Mar  8 12:00:00 UTC 2026
```

## What's Happening

1. `FROM alpine:latest` - Uses Alpine Linux as base (only ~5MB)
2. `RUN echo ...` - Creates a shell script during build
3. `CMD ["/hello.sh"]` - Runs the script when container starts

## Next Steps

- Try modifying the script to print different messages
- Explore [Simple Dockerfile](../../docs/03-dockerfiles/02-simple-dockerfile.md)
- Learn about [Dockerfile Syntax](../../docs/03-dockerfiles/00-dockerfile-syntax.md)
