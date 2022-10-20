import logging
import time

import discord
import interactions


def check_invalid_user(ctx, config):
    role = discord.utils.get(ctx.guild.roles, name=config['general']['allowedRole'])
    if not str(ctx.channel.id) == str(config['general']['listeningChannelId']) or int(role.id) not in ctx.author.roles:
        raise PermissionError("Invalid User")


def prevent_command_chaining(input: str):
    invalid_characters = ["&", ";"]
    if any(character in input for character in invalid_characters):
        raise PermissionError("Invalid Characters")


def prevent_start_without_token(config):
    while str(config['general']['botToken']) == "":
        print("Bot Token Empty. Restart bot after configuration")
        time.sleep(60)


def get_object_by_name(name, objects):
    for obj in objects:
        if name == obj['name']:
            return obj

    raise KeyError(f'{name} Not Found')


def get_help_message(config):
    output = ""

    output += "Servers:\n"
    for server in config['servers']:
        output += f"\t{server['name']}\n"

    output += "\nCommands:\n"
    for script in config['scripts']:
        output += f"\t{script['name']}\n"

    return output


def initialize_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def log_action(message: str, logger: logging.Logger, ctx: interactions.CommandContext = None):
    if ctx is not None:
        logger.info(f"User: {ctx.user.username} | Channel: {ctx.channel.name} > {message}")
    else:
        logger.info(message)
