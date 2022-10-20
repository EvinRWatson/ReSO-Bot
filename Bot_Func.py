import logging
import time

import discord
import interactions


def check_invalid_user(ctx, config):
    if not str(ctx.channel.id) == str(config['general']['listeningChannelId']):
        raise PermissionError("Invalid Channel")

    role = discord.utils.get(ctx.guild.roles, name=config['general']['allowedRole'])
    if int(role.id) not in ctx.author.roles:
        raise PermissionError("Invalid Role")


def prevent_command_chaining(input: str):
    invalid_characters = ["&", ";"]
    if any(character in input for character in invalid_characters):
        raise PermissionError("Invalid Characters")


def get_object_by_name(name, objects):
    for obj in objects:
        if name == obj['name']:
            return obj

    raise KeyError(f'{name} Not Found')


def initialize_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def prevent_start_without_token(config):
    while str(config['general']['botToken']) == "":
        print("Bot Token Empty. Restart bot after configuration")
        time.sleep(60)


def get_help_message(config):
    output = "-Help Info-\n" \
             "Command Format:\t/reso <server-name> <command-name> <parameters>\n\n"

    output += "Servers:\n"
    for server in config['servers']:
        output += f"\t{server['name']}\n"

    output += "\nScripts:\n"
    for script in config['scripts']:
        output += f"\t{script['name']}\n"

    return output


def log_action(message: str, logger: logging.Logger, ctx: interactions.CommandContext = None):
    if ctx is not None:
        logger.info(f"User: {ctx.user.username} | Channel: {ctx.channel.name} > {message}")
    else:
        logger.info(message)
