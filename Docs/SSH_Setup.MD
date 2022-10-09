# Establish an SSH connection to desired server

### Generate SSH Key (Use Defaults)

    ssh-keygen -t rsa

### Copy the key out to the server

- Manual install:
    ~~~
    ssh-copy-id -i ~/.ssh/id_rsa.pub <username>@<host>
    ~~~
- Docker install:
    ~~~
    ssh-copy-id -i /root/.ssh/id_rsa.pub <username>@<host>
    ~~~
### Test SSH Connection

    ssh <username>@<host>