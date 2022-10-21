# Docker Install (Container)

## Install [Docker](https://github.com/docker/cli)

## Download the desired image

Docker images are stored in our [Docker Hub](https://hub.docker.com/repository/docker/evinrwatson/reso-bot).
You can choose between stable(latest) and dev builds, as well as the system architecture.

Architectures include:
- arm64: Apple M1, AWS Graviton, Raspberry Pi 3/4 (64bit)
- arm: Raspberry Pi (32bit)
- amd64: x86/x64 Compatible CPU's (AMD/Intel)

*Dev builds on Docker Hub only come in the linux/amd64 variety to enable faster build times for testing*

*Alternatively, you can also create your own Docker image by building the Dockerfile yourself. If you wish to do so, then follow [this](https://docs.docker.com/engine/reference/commandline/build/) guide* 

## Run the image
Once the image is running you can access the shell to complete installation

## Edit Configurations
You can set up the bot as outlined in the [Configuration Guide](Configuration.MD) by using the packaged
text editors (vim/nano) to edit the config files.

## Establish SSH Connections
Follow the [SSH Setup](SSH_Setup.MD) guide to set up a connection for each instance in the servers.json file.

## Restart the container
Required for the bot to reload the configuration and connect to Discord

## Enjoy!
