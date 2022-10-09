# Docker Install (Container)

## Download/Clone the repository

## Install

- [Docker]() or [Docker Desktop]()

## Edit Configurations

- Follow the [Configuration Guide](Configuration.MD)

## Build the image

- From within the ReSO-bot folder that contains the Dockerfile, run this command
    ~~~
    docker build -t reso-bot .
    ~~~
## Run the image

- Replace the <container_name> in the following command with whichever name you want 
    ~~~
    docker run -d --name <container_name> reso-bot
    ~~~
## Establish an SSH connection

- Get the user and IP address or hostname of the server you wish to manage

- Access the shell of the Docker container:
  ~~~
    docker exec -it <container_name> sh
  ~~~
  
- Once in the shell follow the [SSH](SSH_Setup.MD) guide
- Exit the shell

## Restart the container

## Enjoy!
