Generate SSH Key (Recommended to leave passphrase empty)

    ssh-keygen -t rsa

Copy the key out to the server

    ssh-copy-id -i ~/.ssh/id_rsa.pub <username>@<host>

Test SSH Connection

    ssh <username>@<host>