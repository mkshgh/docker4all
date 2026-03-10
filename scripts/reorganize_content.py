#!/usr/bin/env python3
"""
Content Reorganizer
Moves converted markdown files to proper directory structure with descriptive names
"""

import os
import shutil
from pathlib import Path

# Mapping of old files to new locations
FILE_MAPPING = {
    # Fundamentals (from Basic Intro)
    "temp_converted/Basic Intro/1.Images.md": "docs/02-fundamentals/01-working-with-images.md",
    "temp_converted/Basic Intro/2.Containter.md": "docs/02-fundamentals/02-container-basics.md",
    "temp_converted/Basic Intro/3.Run vs Commit.md": "docs/02-fundamentals/03-container-lifecycle.md",
    "temp_converted/Basic Intro/4.Run Processes in Containers.md": "docs/02-fundamentals/04-running-processes.md",
    "temp_converted/Basic Intro/5.Container Logs and Remove.md": "docs/02-fundamentals/05-logs-and-cleanup.md",
    "temp_converted/Basic Intro/6.Docker Ports.md": "docs/02-fundamentals/06-port-mapping.md",
    
    # Networking
    "temp_converted/Basic Intro/7.Container Networking.md": "docs/05-networking/01-networking-basics.md",
    
    # Volumes
    "temp_converted/Basic Intro/8.Volumes.md": "docs/06-volumes/01-volume-basics.md",
    
    # Dockerfiles
    "temp_converted/DockerFiles/README.md": "docs/03-dockerfiles/01-dockerfile-fundamentals.md",
    "temp_converted/DockerFiles/2.BusyBox Example.md": "docs/03-dockerfiles/02-simple-dockerfile.md",
    "temp_converted/DockerFiles/3.InstallingPrograms Example.md": "docs/03-dockerfiles/03-installing-packages.md",
    "temp_converted/DockerFiles/4.UsingNewImageWeCreated Example.md": "docs/03-dockerfiles/04-using-custom-images.md",
    "temp_converted/DockerFiles/5.Using Multiple Images.md": "docs/03-dockerfiles/05-multi-stage-intro.md",
    
    # Production (from HowItWorks)
    "temp_converted/HowItWorks/4.Resource Management.md": "docs/09-production/06-resource-management.md",
    "temp_converted/HowItWorks/5.Storage in Docker.md": "docs/09-production/07-storage-drivers.md",
    
    # Advanced (from HowItWorks)
    "temp_converted/HowItWorks/1.ControlDockerFromDockerContainer.md": "docs/08-security/02-docker-in-docker.md",
    "temp_converted/HowItWorks/2.Networking and Namespaces.md": "docs/05-networking/02-network-internals.md",
    "temp_converted/HowItWorks/3.Processes in Docker.md": "docs/09-production/08-process-management.md",
    
    # Organizing Docker
    "temp_converted/OrganizingDocker/1.Registries in Docker.md": "docs/09-production/09-registry-usage.md",
    "temp_converted/OrganizingDocker/2.Save and Load Containers.md": "docs/09-production/10-container-export-import.md",
    "temp_converted/OrganizingDocker/2.Save and Load Docker Images.md": "docs/09-production/11-image-export-import.md",
    
    # Compose
    "temp_converted/PowerWithCompose/readme.md": "docs/04-compose/01-compose-introduction.md",
}


def reorganize_content():
    """Reorganize converted content into new structure"""
    print("Reorganizing content...")
    
    moved_count = 0
    skipped_count = 0
    
    for source, destination in FILE_MAPPING.items():
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            print(f"  ⚠ Source not found: {source}")
            skipped_count += 1
            continue
        
        # Create destination directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        print(f"  ✓ {source} → {destination}")
        moved_count += 1
    
    print(f"\nReorganization complete!")
    print(f"  Moved: {moved_count} files")
    print(f"  Skipped: {skipped_count} files")
    
    return moved_count, skipped_count


if __name__ == "__main__":
    reorganize_content()
