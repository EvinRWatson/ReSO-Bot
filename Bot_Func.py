import logging
import time

import discord
import interactions
import yaml


async def respond_and_log(ctx: interactions.CommandContext, message: str):
    log_action(message, ctx)
    await ctx.send(message)


def prevent_invalid_user(ctx: interactions.CommandContext, config: dict):
    role: discord.Role = discord.utils.get(ctx.guild.roles, name=config['general']['allowedRole'])
    if not str(ctx.channel.id) == str(config['general']['listeningChannelId']) or int(role.id) not in ctx.author.roles:
        raise PermissionError("Invalid User")


def prevent_start_without_token(config: dict):
    while str(config['general']['botToken']) == "":
        print("Bot Token Empty. Restart bot after configuration")
        time.sleep(60)


def get_object_by_name(name: str, objects: dict):
    for obj in objects:
        if name == obj['name']:
            return obj

    raise KeyError(f"{name} Not Found")


def get_help_message(config: dict):
    output: str = ""

    output += "Servers:\n"
    for server in config['servers']:
        output += f"\t{server['name']}\n"

    output += "\nCommands:\n"
    for script in config['scripts']:
        output += f"\t{script['name']}\n"

    return output


def initialize_logger():
    logger: logging.Logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler: logging.Handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def log_action(message: str, ctx: interactions.CommandContext = None):
    logger: logging.Logger = initialize_logger()
    if ctx is not None:
        logger.info(f"User: {ctx.user.username} | Channel: {ctx.channel.name} > {message}")
    else:
        logger.info(message)


def get_config():
    return yaml.safe_load(open('config.yml'))


def inject_params(command: str, params: str):
    if not command.__contains__("!param!"):
        raise PermissionError("Parameters not allowed for this action")

    return command.replace('!param!', params)
