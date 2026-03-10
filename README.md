# Docker Tutorial: From Beginner to Production

![Docker Version](https://img.shields.io/badge/Docker-20.10%2B-blue)
![Compose Version](https://img.shields.io/badge/Compose-v2-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Maintenance](https://img.shields.io/badge/maintained-yes-brightgreen)

A comprehensive, modern Docker tutorial that takes you from installation to production-ready containerized applications. This tutorial reflects 2025+ best practices, including Docker Engine 20.10+, Compose v2, BuildKit, and modern security practices.

## 🎯 Learning Objectives

By completing this tutorial, you will:

- Understand Docker architecture and core concepts
- Build, run, and manage containers confidently
- Write efficient Dockerfiles using modern syntax
- Leverage BuildKit for faster, more secure builds
- Create multi-stage builds for optimized images
- Orchestrate multi-container applications with Docker Compose v2
- Implement container networking and data persistence
- Apply security best practices and optimization techniques
- Deploy production-ready containerized applications

## 📋 Prerequisites

- **Operating System:** Linux, macOS, or Windows with WSL 2
- **Docker Engine:** 20.10 or later
- **Docker Compose:** v2 (integrated into Docker CLI)
- **Knowledge:** Basic command-line skills and Linux fundamentals

> **Note:** This tutorial uses modern Docker syntax throughout, including `docker compose` (not `docker-compose`) and `--mount` flags.

## 🚀 Quick Start

### 1. Install Docker

Follow the [Installation Guide](docs/01-getting-started/01-installation-setup.md) for your platform.

### 2. Verify Installation

```bash
docker --version
docker compose version
docker run hello-world
```

### 3. Start Learning

Begin with [Docker Architecture](docs/01-getting-started/02-docker-architecture.md) to understand the fundamentals.

## 📚 Learning Path

This tutorial is organized into progressive difficulty levels. Follow the path sequentially for the best learning experience.

### 🟢 Beginner: Getting Started

Start here if you're new to Docker.

1. [Installation and Setup](docs/01-getting-started/01-installation-setup.md) - Install Docker on your system
2. [Docker Architecture](docs/01-getting-started/02-docker-architecture.md) - Understand how Docker works
3. [Basic Commands](docs/01-getting-started/03-basic-commands.md) - Essential Docker CLI commands
4. [Images and Containers](docs/01-getting-started/04-images-containers.md) - Core concepts explained

### 🟡 Beginner: Fundamentals

Build on the basics with hands-on practice.

5. [Working with Images](docs/02-fundamentals/01-working-with-images.md) - Pull, tag, and manage images
6. [Container Basics](docs/02-fundamentals/02-container-basics.md) - Create and manage containers
7. [Container Lifecycle](docs/02-fundamentals/03-container-lifecycle.md) - Understand container states
8. [Running Processes](docs/02-fundamentals/04-running-processes.md) - Execute commands in containers
9. [Logs and Cleanup](docs/02-fundamentals/05-logs-and-cleanup.md) - View logs and clean up resources
10. [Port Mapping](docs/02-fundamentals/06-port-mapping.md) - Expose container services

### 🟠 Intermediate: Building Images

Learn to create custom Docker images.

11. [Dockerfile Syntax](docs/03-dockerfiles/00-dockerfile-syntax.md) - Write Dockerfiles with best practices
12. [Simple Dockerfile](docs/03-dockerfiles/02-simple-dockerfile.md) - Your first custom image
13. [Installing Packages](docs/03-dockerfiles/03-installing-packages.md) - Add software to images
14. [Using Custom Images](docs/03-dockerfiles/04-using-custom-images.md) - Build on your own images
15. [Multi-Stage Builds Intro](docs/03-dockerfiles/05-multi-stage-intro.md) - Introduction to multi-stage builds
16. [BuildKit Features](docs/03-dockerfiles/06-buildkit.md) - Modern build engine capabilities

### 🟠 Intermediate: Orchestration

Manage multi-container applications.

17. [Docker Compose Introduction](docs/04-compose/01-compose-introduction.md) - Orchestrate multiple containers

### 🟠 Intermediate: Networking

Connect containers and services.

18. [Networking Basics](docs/05-networking/01-networking-basics.md) - Container networking fundamentals
19. [Network Internals](docs/05-networking/02-network-internals.md) - Deep dive into Docker networking

### 🟠 Intermediate: Data Persistence

Store and manage data.

20. [Volume Basics](docs/06-volumes/01-volume-basics.md) - Persist data with volumes

### 🔴 Advanced: Optimization (⌛Pending)

Build smaller, faster images.

21. [Optimization Techniques](docs/07-optimization/01-optimization-techniques.md) - Reduce image size and build time

### 🔴 Advanced: Security

Secure your containers.

22. [Docker-in-Docker](docs/08-security/02-docker-in-docker.md) - Run Docker inside containers
23. [Container Security](docs/08-security/01-container-security.md) - Security best practices

### 🔴 Production: Deployment

Deploy containers to production.

24. [Resource Management](docs/09-production/06-resource-management.md) - Limit CPU and memory
25. [Storage Drivers](docs/09-production/07-storage-drivers.md) - Understand storage backends
26. [Process Management](docs/09-production/08-process-management.md) - Manage container processes
27. [Registry Usage](docs/09-production/09-registry-usage.md) - Work with image registries
28. [Container Export/Import](docs/09-production/10-container-export-import.md) - Backup and restore containers
29. [Image Export/Import](docs/09-production/11-image-export-import.md) - Share images offline

## 🎓 Learning Tips

### For Beginners

- **Follow the order:** Start with Getting Started and progress sequentially
- **Practice each concept:** Run the examples in your terminal
- **Don't skip fundamentals:** Understanding basics prevents confusion later
- **Use the cheat sheets:** Reference command tables when needed

### For Intermediate Learners

- **Focus on Dockerfiles:** Writing good Dockerfiles is crucial
- **Experiment with BuildKit:** Modern features improve your workflow
- **Learn Compose:** Multi-container apps are the norm in production
- **Understand networking:** Container communication is essential

### For Advanced Users

- **Optimize everything:** Smaller images = faster deployments
- **Security first:** Always run as non-root, use secrets properly
- **Automate builds:** Use CI/CD with BuildKit cache
- **Monitor resources:** Set limits and health checks

## 💡 Key Concepts

### Modern Docker Syntax

This tutorial uses current Docker best practices:

```bash
# ✅ Modern (use this)
docker compose up
docker run --mount type=bind,source=/host,target=/container nginx

# ❌ Legacy (avoid this)
docker-compose up
docker run -v /host:/container nginx
```

### Docker Compose v2

Compose v2 is integrated into the Docker CLI:

```bash
# Compose v2 (modern)
docker compose up
docker compose down

# File naming
compose.yaml  # Preferred
```

### BuildKit

BuildKit is the default build engine (Docker 23.0+):

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18-alpine
RUN --mount=type=cache,target=/root/.npm \
    npm install
```

## 📁 Repository Structure

```
docker-tutorial/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── .gitignore                   # Git ignore rules
├── docs/                        # All tutorial content
│   ├── 01-getting-started/      # Beginner: Installation and basics
│   ├── 02-fundamentals/         # Beginner: Core concepts
│   ├── 03-dockerfiles/          # Intermediate: Building images
│   ├── 04-compose/              # Intermediate: Multi-container apps
│   ├── 05-networking/           # Intermediate: Container networking
│   ├── 06-volumes/              # Intermediate: Data persistence
│   ├── 07-optimization/         # Advanced: Image optimization
│   ├── 08-security/             # Advanced: Security practices
│   └── 09-production/           # Production: Deployment topics
├── examples/                    # Working code examples
│   ├── basic/                   # Simple examples
│   ├── multi-stage/             # Multi-stage build examples
│   ├── compose/                 # Docker Compose examples
│   ├── networking/              # Networking examples
│   └── production/              # Production-ready examples
└── scripts/                     # Utility scripts
```

## 🛠️ Working Examples

All examples are in the `examples/` directory and are ready to run:

```bash
# Basic hello-world
cd examples/basic/hello-world
docker build -t hello .
docker run hello

# Multi-stage Node.js app
cd examples/multi-stage/node-app
docker build -t node-app .
docker run -p 3000:3000 node-app

# Compose application
cd examples/compose/web-database
docker compose up
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to contribute
- Documentation standards
- Code example requirements
- Pull request process

## 📖 Additional Resources

### Official Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

### Community

- [Docker Community Forums](https://forums.docker.com/)
- [Docker GitHub](https://github.com/docker)
- [Docker Blog](https://www.docker.com/blog/)

### Best Practices

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Security Best Practices](https://docs.docker.com/engine/security/)

## ❓ Troubleshooting

### Common Issues

**"Cannot connect to Docker daemon"**
- Ensure Docker is running
- Check Docker Desktop is started (macOS/Windows)
- Verify Docker service: `sudo systemctl status docker` (Linux)

**"Permission denied"**
- Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and log back in
- Or use `sudo` temporarily

**"No space left on device"**
- Clean up: `docker system prune -a`
- Remove unused volumes: `docker volume prune`
- Check disk space: `df -h`

**"Port already allocated"**
- Use different port: `-p 8081:80` instead of `-p 8080:80`
- Stop conflicting container: `docker ps` then `docker stop <container>`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Docker community for excellent documentation
- Contributors who helped improve this tutorial
- Open source projects that inspired examples

## 📬 Feedback

Found an issue or have a suggestion? Please:

1. Check existing issues
2. Open a new issue with details
3. Or submit a pull request

---
