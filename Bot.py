import discord
import interactions
import logging
import json
import subprocess

print('Initializing Logger')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

print('Loading Config')
config = json.load(open('config.json'))

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
            name="params",
            description="Parameters",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, params: str):
    await ctx.send(f'Received Command Parameters: {params}')

    if not __valid_command(ctx):
        await ctx.send('Invalid Command')
        return

    command = params.split(" ")[0]
    params = params.replace(f'{command} ', '')

    for script in scripts['scripts']:
        if script["name"] == command:
            await ctx.send(f'Running script: {script["name"]}')
            __call_script(script, params)
            await ctx.send('Complete')
            return

    for file in files['files']:
        if file["name"] == command:
            await ctx.send(f'Running File Fetch: {file["name"]}')
            end_file = __fetch_file(file)
            #send_channel = client.get_channel(int(config['file_fetch']['fileDropLocationChannelId']))
            #await send_channel.send(file=end_file)
            await ctx.send('Complete')
            return

    __output_log_console('Command not found: {}')


def __valid_command(ctx):
    if ctx.author == bot.me.name:
        return False
    if not str(ctx.channel.id) == config['permissions']['listeningChannelId']:
        return False

    role = discord.utils.get(ctx.guild.roles, name=config['permissions']['allowedRole'])
    if int(role.id) not in ctx.author.roles:
        return False

    return True


def __call_script(script, params):
    server_command = f'{script["command"]} "{params.strip()}"'
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


def __output_log_console(output):
    print(output)
    logger.info(output)


bot.start()
