# Docker Installation and Setup

**Difficulty:** Beginner  
**Estimated Time:** 15-20 minutes

## Overview

This guide walks you through installing Docker Engine and Docker Compose on your system. We'll cover installation for the major operating systems and verify that everything is working correctly.

## Prerequisites

- A 64-bit operating system
- Administrator/root access to your system
- Basic command-line knowledge

## Minimum Requirements

This tutorial requires:
- **Docker Engine:** 20.10 or later
- **Docker Compose:** v2 (integrated into Docker CLI)

> **Note:** Docker Compose v2 is now integrated into the Docker CLI as `docker compose` (not `docker-compose`). This tutorial uses the modern v2 syntax throughout.

## Installation by Platform

### Linux (Ubuntu/Debian)

1. **Remove old Docker versions** (if any):

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

2. **Update package index and install dependencies**:

```bash
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

3. **Add Docker's official GPG key**:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. **Set up the repository**:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. **Install Docker Engine**:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

6. **Verify installation**:

```bash
sudo docker run hello-world
```

### macOS

1. **Download Docker Desktop** from the [official Docker website](https://www.docker.com/products/docker-desktop)

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file
   - Drag Docker to Applications folder
   - Launch Docker from Applications

3. **Verify installation**:

```bash
docker --version
docker compose version
```

### Windows

1. **Enable WSL 2** (Windows Subsystem for Linux):
   - Open PowerShell as Administrator
   - Run: `wsl --install`
   - Restart your computer

2. **Download Docker Desktop** from the [official Docker website](https://www.docker.com/products/docker-desktop)

3. **Install Docker Desktop**:
   - Run the installer
   - Follow the installation wizard
   - Ensure "Use WSL 2 instead of Hyper-V" is selected

4. **Verify installation**:

```bash
docker --version
docker compose version
```

## Post-Installation Steps (Linux)

### Run Docker without sudo

By default, Docker requires root privileges. To run Docker as a non-root user:

1. **Create the docker group** (if it doesn't exist):

```bash
sudo groupadd docker
```

2. **Add your user to the docker group**:

```bash
sudo usermod -aG docker $USER
```

3. **Log out and log back in** for the changes to take effect, or run:

```bash
newgrp docker
```

4. **Verify you can run docker without sudo**:

```bash
docker run hello-world
```

## Verifying Your Installation

### Check Docker Version

```bash
docker --version
```

Expected output (version may vary):
```
Docker version 24.0.0, build abc1234
```

### Check Docker Compose Version

```bash
docker compose version
```

Expected output:
```
Docker Compose version v2.20.0
```

### Check Docker Info

```bash
docker info
```

This displays comprehensive information about your Docker installation, including:
- Server version
- Storage driver
- Number of containers and images
- System resources

### Run a Test Container

```bash
docker run hello-world
```

If successful, you'll see:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

## Troubleshooting

### Permission Denied Error (Linux)

If you see "permission denied" errors:
- Ensure you've added your user to the docker group
- Log out and log back in
- Try running with `sudo` temporarily

### Docker Daemon Not Running

If you see "Cannot connect to the Docker daemon":
- **Linux:** Start Docker with `sudo systemctl start docker`
- **macOS/Windows:** Ensure Docker Desktop is running

### WSL 2 Issues (Windows)

If Docker Desktop fails to start on Windows:
- Ensure WSL 2 is properly installed: `wsl --status`
- Update WSL: `wsl --update`
- Restart Docker Desktop

## Next Steps

Now that Docker is installed, you're ready to:
- Learn about [Docker Architecture](02-docker-architecture.md)
- Start [Working with Images](../02-fundamentals/01-working-with-images.md)
- Explore [Container Basics](../02-fundamentals/02-container-basics.md)

## Additional Resources

- [Official Docker Installation Guide](https://docs.docker.com/engine/install/)
- [Docker Desktop Documentation](https://docs.docker.com/desktop/)
- [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)
