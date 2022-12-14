# Remote Server Operation Bot (ReSO-Bot)

Highly configurable client bot designed for Discord server admins, allowing them to interface with any server utilizing the SSH protocol.

<p align="center">
  <img src="https://raw.githubusercontent.com/EvinRWatson/ReSO-Bot/master/ReSO_Bot_Logo.jpg" width="300" height="300"/>
</p>

Recommended setup for this application is containerized on a centralized server, acting as a layer between your Discord and another server that resides within your network, such as a gaming or automation server.

### Functionality:
- Call pre-configured commands and scripts
- Grab files from pre-designated locations

### Limitations:
- Can only use commands that the server user has permissions to run
- Can only grab files from directories that the server user has access to

## Installation

### Setup 

[Docker](/Docs/Docker_Install.MD) (Recommended)

[Manual](/Docs/Manual_Install.MD)

### Reference

[Configuration](/Docs/Configuration.MD)

[SSH](/Docs/SSH_Setup.MD)

## Using the bot

After completing installation, using the bot requires using the '/reso' command

Commands:

- /reso run <server_name> <command_name> <parameters?>
- /reso ping <server_name>
- /reso reload
- /reso help

#### Have a problem, or want to request a feature? [Open an issue!](https://github.com/EvinRWatson/ReSO-Bot/issues/new)