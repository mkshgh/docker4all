Docker4all
=====================


Installation:
---------------

Reference: `Docker Official Installation Guide <https://docs.docker.com/engine/install/ubuntu>`_ 

1. Uninstall the existing docker

.. code-block:: bash

    sudo apt-get remove docker docker-engine docker.io containerd runc

2. Install and update the dependencies

.. code-block:: bash

    sudo apt-get update

    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

3. Add Docker’s official GPG key:

.. code-block:: bash

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg


4. Use the following command to set up the stable repository, depending on your linux environment

.. code-block:: bash

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

5. Update again and then the real installation begins

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io


6. Info about the Docker installed

.. code-block:: bash

    docker info



7. Kill all docker instances

.. code-block:: bash


    docker kill $(docker ps -q)
    # or
    docker rm $(docker ps -a -q)
    # or
    docker rmi $(docker images -q)

Testing:
---------

1. Run hello-world as usual. Could make it more interesting. I could say good by too.

.. code-block:: bash

    sudo docker run hello-world

    # You will see the Hello from Docker!


Docker for non Sudo users
--------------------------




1. Create the docker group.

.. code-block:: bash

    sudo groupadd docker

2. Add your user to the docker group.

.. code-block:: bash

    sudo usermod -aG docker $USER
    # my user in mkshgh here



Uninstall
------------

.. code-block:: bash

    sudo apt-get remove docker docker-engine docker.io containerd runc

10 Seconds each
----------------

::

    Tuts
    ├── Basic Intro
    │   ├── 1.Images.rst
    │   ├── 1.format.sh
    │   ├── 2.Containter.rst
    │   ├── 3.Run vs Commit.rst
    │   ├── 4.Run Processes in Containers.rst
    │   ├── 5.Container Logs and Remove.rst
    │   ├── 6.Docker Ports.rst
    │   ├── 7.Container Networking.rst
    │   ├── 8.Volumes.rst
    │   └── 9.Search and Download Images
    ├── DockerFiles
    │   ├── 2.BusyBox Example.rst
    │   ├── 3.InstallingPrograms Example.rst
    │   ├── 4.UsingNewImageWeCreated Example.rst
    │   ├── 5.Using Multiple Images.rst
    │   ├── BusyBox
    │   │   └── dockerfile
    │   ├── InstallingPrograms
    │   │   ├── 4.nano_iamge.JPG
    │   │   └── dockerfile
    │   ├── README.rst
    │   ├── UsingExistingFiles
    │   │   ├── 4.nano_image_with_text.JPG
    │   │   ├── dockerfile
    │   │   └── notes.txt
    │   └── UsingMultipleImages
    ├── HowItWorks
    │   ├── 1.ControlDockerFromDockerContainer.rst
    │   ├── 2.Networking and Namespaces.rst
    │   ├── 3.Processes in Docker.rst
    │   ├── 4.Resource Management.rst
    │   ├── 5.Storage in Docker.rst
    │   ├── README.rst
    │   └── mynewdir
    │       ├── directoryinside
    │       │   ├── file1
    │       │   ├── file2
    │       │   └── file3
    │       ├── somefile1
    │       ├── somefile2
    │       └── somefile3
    ├── OrganizingDocker
    │   ├── 1.Registries in Docker
    │   │   └── docker-compose.yml
    │   ├── 1.Registries in Docker.rst
    │   ├── 2.Save and Load Containers.rst
    │   ├── 2.Save and Load Docker Images.rst
    │   └── alpine-image.tar.gz
    └── README.rst

    
