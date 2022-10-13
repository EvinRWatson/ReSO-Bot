import json

import interactions
from interactions.ext.files import command_send

import Bot_Func
import Server_Func

print('Loading:')
print('\tLogger')
logger = Bot_Func.initialize_logger()

print('\tConfig')
config = json.load(open('config.json'))

print('\tServers')
servers = json.load(open('servers.json'))

print('\tScripts')
scripts = json.load(open('scripts.json'))

print('Finished Loading')
Bot_Func.prevent_start_without_token(config)

print('Initialize Client')
bot = interactions.Client(token=config['general']['botToken'],
                          default_scope=config['general']['guildId'])


@bot.command(
    name='reso',
    description="Command to trigger ReSO Bot interpretation",
    options=[
        interactions.Option(
            name="bot_parameters",
            description="Parameters",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, bot_parameters: str):
    invalid_reasons = Bot_Func.check_invalid_user(ctx, config, bot_parameters)
    if invalid_reasons != "":
        await ctx.send('Cannot execute command:\n' + invalid_reasons)
        return

    try:
        server_name = bot_parameters.split(" ")[0]
        server_command = bot_parameters.split(" ")[1]
        command_parameters = bot_parameters.replace(server_name, '').replace(server_command, '').strip()
    except IndexError:
        await ctx.send(
            'There seems to be an error with your command format. If you need help please refer to the documentation')
        return

    server = Bot_Func.get_server_by_name(server_name, servers)
    if server is None:
        await ctx.send(f"Server '{server_name}' Not Found")
        return

    for script in scripts['scripts']:
        if script["name"] == server_command:
            if script['type'] == 'command':
                await ctx.send(f"Running {script['type']}: {script['name']}")
                Server_Func.run_command(server, script, command_parameters)
                await ctx.send('Complete')
                return
            if script['type'] == 'fetch':
                await ctx.send(f"Running {script['type']}: {script['name']}")
                end_file = Server_Func.run_fetch(server, script, config)
                await command_send(ctx, script["name"], files=end_file)
                return

    await ctx.send(f"Command '{server_command}' Not Found")


print('Start Client')
bot.start()
