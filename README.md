# Remote Server Operation Bot (ReSO-Bot)

Highly configurable client bot designed to be used by Discord server admins to allow them to interface with a server utilizing the SSH protocol.

Recommended use case for this bot it between your discord server and another server that resides within your home network, such as a home gaming or automation server. This is not meant to be a replacement for setting up a legitimate production server using indiustry standard server communication protocols such as: RPC or HTTP(s).

### Functionality:
- Call pre-configured commands and scripts
- Grab files from pre-designated locations

### Limitations:
- Can only connect to one server per bot instance (Multi-server configurations coming later)
- Can only use commands that the server user has permissions to run
- Can only grab files from directories that the server user has access to

## Docs
[Setup Documentation](/SETUP.MD)
