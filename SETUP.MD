# Initial Setup

### Download or Clone the ReSO-Bot repository

### Install:
    
[Python](https://www.python.org/downloads/), [PIP](https://pypi.org/project/pip/), and [Discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)

Alternatively run these commands (Debian/Ubuntu based Linux distributions only):
    
~~~
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
python3.9 get-pip.py
python3.9 -m pip install -U discord.py
~~~

### Establish an SSH connection between the client and the intended server

### Configure file(s):

[Configuration]() 

[Scripts]()

[Files]()

### Run the bot
~~~
python3.9 Bot.py
~~~



# Configuration options (config.json):

## General:

### botToken:
The access token for your Discord Bot instance. Bots can be created through the
[Discord Dev Portal](https://discord.com/developers/). For more detailed instructions,
follow this guide by [Discord.py](https://discordpy.readthedocs.io/en/stable/discord.html)!

### listeningCommand:
The prefix to your given command in the listening channel. This tells the bot that this message
is a command to process. Default is !RESO, but can be changed to whatever you want, ex: /RESO, 
!SERVER, /TROLL.

## Permissions:

### listeningChannelId:
The ID of the channel you want the bot to listen for commands in. You can get the channel ID
by first enabling developer mode in your discord User Settings, and then right-clicking on the
desired channel and clicking 'Copy ID' at the bottom. For greater security, this channel should 
be restricted to only those who you want to operate the bot.

### allowedRole:
The role that you assign to others to allow them to operate the bot. Examples include: Admin,
Moderator, BotOperator, etc. This setting in conjunction with properly configuring the listening
channel will ensure that no one who isn't explicitly allowed can operate the bot.

## File Fetch:

### fileDropLocationChannelId:
The ID of the channel that you want files to be dropped when using the file fetching functionality.
You may want this to be different to the listening channel because you might have Admins who are
able to use the bot, and some that aren't. So you can have a bot operator use the file fetch command
to grab a log file, and send it to a channel that all admins can view.

### fileDropClientFilePath:
The temporary location of the fetched file in the bot client's operating system. This location
is arbitrary, but make sure that the bot has permissions to access that directory. Examples:

~~~
/home/bob/fetch
C:/Users/Bob/fetch
/home/bob/temp
~~~
## SSH

### Host:
The host or IP of the server you are connecting to through the bot. This can be an IP address
or a host name if specified in your local hosts file, or network DNS.

### Username:
The username of the intended user on the server. It is not advised to use the root user, instead
set up a user specifically for the bot and assign permissions accordingly to prevent malicious actors
from doing some real damage to your server.

### Passwd (Not currently supported):
The password corresponding to the Username above. Instead of storing the password here in plain
text. Set up a password-less key when setting up your initial SSH connection.

# Scripts (scripts.json)

## Parameters

### name
Name of the bot command you want to use to trigger the command below. No spaces are allowed. 

Example:

    backup

### command
Command to run on the server. Make sure the bot user on the server has
permissions to run that command, or it will not work.

Example:

    sh /home/bob/backup.sh

## File Structure
The file follows basic JSON formatting. To add a command, simply add a comma after the closing
'}' bracket of the previous command and copy the formatting to declare a new command.

Example File:

~~~
{
  "scripts" : [
    {
      "name": "example",
      "command": "sh /temp/example.sh"
    },
    {
      "name": "backup",
      "command": "sh /home/bob/backup.sh"
    }
  ]
}
~~~

# File Fetch (fetch_files.json)

## Parameters

### name
Name of the bot command you want to use to trigger the fetch of the 
specified file below. No spaces are allowed.

Example:

    game_log

### command
Location of the file you want to grab associated with the above name.
Make sure the bot user on the server has permissions to access to the
specified directory/file, or it will not work 

Example:

    /home/bob/minecraft/logs/latest.log

