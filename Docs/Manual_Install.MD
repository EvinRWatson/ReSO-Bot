# Manual Install (VM or Desktop)

## Download/Clone the repository

## Install:
    
 - [Python](https://www.python.org/downloads/), [PIP](https://pypi.org/project/pip/), and [Discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)

Alternatively run these commands (Debian/Ubuntu based Linux distributions only):
    
~~~
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt-get update
sudo apt-get install python3.9 python3-pip
python3.9 -m pip install -U discord.py
python3 -m pip install -e git+https://github.com/interactions-py/library.git#egg=discord-py-interactions
python3.9 -m pip install -U interactions-files
~~~

## Establish an [SSH Connection](SSH_Setup.MD)

## Edit [configuration](Configuration.MD) files:

## Run the bot

    python3.9 Bot.py


