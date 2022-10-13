import logging
import time

import discord


def check_invalid_user(ctx, config, params):
    invalid_reasons = ""

    if not str(ctx.channel.id) == config['permissions']['listeningChannelId']:
        invalid_reasons += "Invalid Channel\n"

    role = discord.utils.get(ctx.guild.roles, name=config['permissions']['allowedRole'])
    if int(role.id) not in ctx.author.roles:
        invalid_reasons += "Invalid Role\n"

    invalid_characters = ["&", ";"]
    if any(character in params for character in invalid_characters):
        invalid_reasons += "Invalid Characters\n"

    return invalid_reasons


def get_server_by_name(name, servers):
    for server in servers['servers']:
        if name == server['name']:
            return server
    return None


def initialize_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def prevent_start_without_token(config):
    while config['general']['botToken'] == "":
        print("Bot Token Empty. Restart bot ot after configuration")
        time.sleep(60)
