import json
import logging
import os
import subprocess

import discord
import interactions
from interactions.ext.files import command_send

print('Initializing Logger')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

print('Loading Config')
config = json.load(open('config.json'))

print('Loading Servers')
servers = json.load(open('servers.json'))

print('Loading Scripts and Files')
scripts = json.load(open('scripts.json'))
files = json.load(open('fetch_files.json'))

bot = interactions.Client(token=config['general']['botToken'],
                          default_scope=config['general']['guildId'])


@bot.command(
    name='reso',
    description="Command to trigger ReSO Bot interpretation",
    options=[
        interactions.Option(
            name="bot_params",
            description="Parameters",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, bot_params: str):
    await ctx.send(f'Received Command Parameters: {bot_params}')

    invalid_reasons = __check_invalid_use(ctx, bot_params)
    if invalid_reasons != "":
        await ctx.send('Cannot execute command:\n' + invalid_reasons)
        return

    server_name = bot_params.split(" ")[0]
    server_command = bot_params.split(" ")[1]
    command_parameters = bot_params.replace(server_name, '').replace(server_command, '').strip()
    server = __get_server_by_name(server_name)

    for script in scripts['scripts']:
        if script["name"] == server_command:
            await ctx.send(f'Running script: {script["name"]}')
            __call_script(server, script, command_parameters)
            await ctx.send('Complete')
            return

    for file in files['files']:
        if file["name"] == server_command:
            await ctx.send(f'Running File Fetch: {file["name"]}')
            end_file = __fetch_file(server, file)
            await command_send(ctx, file["name"], files=end_file)
            return

    __output_log_console('Command not found: {}')


def __check_invalid_use(ctx, params):
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


def __call_script(server, script, params):
    server_command = f'{script["command"]} "{params.strip()}"'
    subprocess.run(["ssh", f"{server['username']}@{server['host']}", server_command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def __fetch_file(server, file):
    file_location = file['location']
    file_destination = config['file_fetch']['fileDropClientFilePath']

    subprocess.run(["scp", f"{server['username']}@{server['host']}:{file_location}", file_destination])

    file_name = os.path.basename(file_location)
    file_path = f'{file_destination}/{file_name}'

    end_file = interactions.File(file_path)
    return end_file


def __output_log_console(output):
    print(output)
    logger.info(output)


def __get_server_by_name(name):
    for server in servers['servers']:
        if name == server['name']:
            return server


bot.start()
