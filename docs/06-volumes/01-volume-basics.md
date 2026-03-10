# Volumes

1. Share your directory to the docker

```bash
docker run -d -it -v path/to/folder:/folderref alpine
```
2. Share your files to the docker 

Make sure that your file exists before the docker is on. Or else it will assume that it is a directory.

```bash
docker run -d -it -v path/to/file.txt:/file.txt alpine
```
3. Temporary directory that exists only when the container is running.
    
    Use: -v your-temp-foler name

```bash
docker run -it -v /shared-temp-folder adoring_obsidian
```
    # If you ls you can see the shared folder

    / # ls
    bin                 mnt                 shared-temp-folder
    dev                 opt                 srv
    etc                 proc                sys
    home                root                tmp
    lib                 run                 usr
    media               sbin                var



4. Check the NAMES of the container which is sharing the data 


```bash
docker ps -l --format $FORMATID
```
    ID ba9ed5d70cef
    IMAGE   adoring_obsidian
    COMMAND "/bin/sh"
    CREATED 3 minutes ago
    STATUS  Up 3 minutes
    PORTS
    NAMES   musing_bardeen

5. Attach the given folder to a new container i.e. shared folder

    It is not shared to the host device and only shared among the given conatiners

    Use: --volumes-from <name of the container sharing the volume>


```bash
docker run -ti --volumes-from musing_bardeen alpine
```
If you list the disk you can see the shared containers.

```bash
/ # ls
```
    bin                 mnt                 shared-temp-folder
    dev                 opt                 srv
    etc                 proc                sys
    home                root                tmp
    lib                 run                 usr
    media               sbin                var

Any container can create the new files and direcotries in this shared folder.

```bash
/ # echo  "This New File is shared to all the conaiters" > shared-temp-folder/more-data.txt
```

It will be avilable from another conatiner musing_bardeen

```bash
/ # ls shared-temp-folder/
more-data.txt
```
The shared folder will be remvoed when all the conatiners which are accessing the volumes are closed.