# Configuration options (config.yml):

It is recommended to set up the configuration from top to bottom.

## General:

### botToken:
The access token for your Discord Bot instance. Bots can be created through the
[Discord Dev Portal](https://discord.com/developers/). For more detailed instructions,
follow this guide by [Discord.py](https://discordpy.readthedocs.io/en/stable/discord.html)!

When setting up the bot, ensure to add the 'bot' scope and within that you will need these permissions:
- Read Messages/View Channels
- Send Messages
- Attach Files
- Use Slash Commands

### guildId
The ID for the server the bot will be running on. You can get this by right-clicking on the server
name on the top-left side of the discord window and clicking 'Copy ID' at the bottom.

### listeningChannelId:
The ID of the channel you want the bot to listen for commands in. You can get the channel ID
by first enabling developer mode in your discord User Settings, and then right-clicking on the
desired channel and clicking 'Copy ID' at the bottom. For greater security, this channel should 
be restricted to only those who you want to operate the bot.

### allowedRole:
The role that you assign to others to allow them to operate the bot. Examples include: Admin,
Moderator, BotOperator, etc. This setting in conjunction with properly configuring the listening
channel will ensure that no one who isn't explicitly allowed can operate the bot.

### fileDropClientFilePath:
The temporary location of the fetched file in the bot client's operating system. This location
is arbitrary, but make sure that the bot has permissions to access that directory. When using Docker,
the recommended location is '/tmp'.

### azureCredentialsJson (Optional)
The credentials used by Azure CLI. Not required if you are not using Azure CLI. Documentation on 
generating the credentials JSON can be found [here](https://github.com/Azure/login?tab=readme-ov-file#login-with-a-service-principal-secret).

# Servers

### name:
The name you assign the server, this determines which location the desired command gets send to when using the bot

### username:
The username of the intended user on the server. It is not advised to use the root user, instead
set up a user specifically for the bot and assign permissions accordingly to prevent malicious actors
from doing some real damage to your server.

### host:
The host or IP of the server you are connecting to through the bot. This can be an IP address
or a host name if specified in your hosts file, or DNS.



# Scripts

### name
Name of the bot command you want to use to trigger the command below. Spaces are not allowed

Example:

    backup

### type
Type of command used, options are:
- command: To run the command specified in the following 'command' variable
- fetch: To retrieve the file, specified in the following 'location' variable

### command (when 'type' is 'command')
Command to run on the server. Make sure the bot user on the server has
permissions to run that command, or it will not work.

Example:

    sh /home/bob/backup.sh

#### Parameters (Optional)
In order to pass parameters to your command, you need to set a parameter flag
in the command string. The designated parameter flag is **!param!**.
An example example of calling a script that takes in a parameter may look 
this.

    sh /home/bob/ban_user.sh !param!

Doing this will allow you to pass in whatever you want through the Discord
client as a replacement for **!param!**. If you pass parameters to a command that 
does not have an explicit parameter flag you will get an error, and the command
will not run.

### location (when 'type' is 'fetch')
Location of the file you want to fetch, associated with this command.

Example:

    /home/bob/App/logs/latest.log
