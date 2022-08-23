import discord
import logging
import json
import subprocess

print('Initializing Logger')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

print('Initializing Discord Client')
client = discord.Client()

print('Loading Config')
config = json.load(open('config.json'))

print('Loading Scripts and Files')
scripts = json.load(open('scripts.json'))
files = json.load(open('fetch_files.json'))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if not __valid_command(message):
        return

    flag = message.content.split(" ")[0];
    command = message.content.split(" ")[1];
    params = message.content.replace(f'{flag} {command}', '')

    for script in scripts['scripts']:
        if script["name"] == command:
            await message.channel.send(f'Running script: {script["name"]}')
            await __call_script(command, params)
            await message.channel.send('Complete')

    for file in files['files']:
        if file["name"] == command:
            await message.channel.send(f'Running File Fetch: {file["name"]}')
            end_file = __fetch_file(file)
            send_channel = client.get_channel(int(config['file_fetch']['fileDropLocationChannelId']))
            await send_channel.send(file=end_file)
            await message.channel.send('Complete')


def __valid_command(message):
    if message.author == client.user:
        return False
    if not message.content.startswith(config['general']['listeningCommand']):
        return False
    if not str(message.channel.id) == config['permissions']['listeningChannelId']:
        return False
    if not config['permissions']['allowedRole'] in [y.name for y in message.author.roles]:
        return False

    return True


async def __call_script(command, params):
    server_command = f'{command["command"]} "{params.strip()}"'
    username = config['ssh']['Username']
    host = config['ssh']['Host']
    subprocess.run(["ssh", f"{username}@{host}", server_command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def __fetch_file(file):
    file_location = file['location']
    file_destination = config['file_fetch']['fileDropClientFilePath']
    username = config['ssh']['Username']
    host = config['ssh']['Host']

    subprocess.run(["scp", f"{username}@{host}:{file_location}", file_destination])

    file_path = f'{file_destination}/latest.log'
    end_file = discord.File(file_path)
    return end_file


client.run(config['general']['botToken'])