import json
import time

import interactions
from interactions.ext.files import command_send

import Bot_Func
import Server_Func

print('Loading:')
print('\tLogger')
logger = Bot_Func.initialize_logger()

print('\tLoading Config')
config = json.load(open('config.json'))

print('\tLoading Servers')
servers = json.load(open('servers.json'))

print('\tLoading Scripts')
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
            name="input",
            description="Parameters",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, input: str):
    await ctx.send(f'Received Command Parameters: {input}')

    invalid_reasons = Bot_Func.check_invalid_user(ctx, input)
    if invalid_reasons != "":
        await ctx.send('Cannot execute command:\n' + invalid_reasons)
        return

    server_name = input.split(" ")[0]
    server_command = input.split(" ")[1]
    command_parameters = input.replace(server_name, '').replace(server_command, '').strip()

    server = Bot_Func.get_server_by_name(server_name, servers)
    if server is None:
        await ctx.send(f"Server '{server_name}' Not Found")
        return

    for script in scripts['scripts']:
        if script["name"] == server_command:
            if script['type'] == 'command':
                await ctx.send(f"Running {script['type']}: {script['name']}")
                Server_Func.call_script(server, script, command_parameters)
                await ctx.send('Complete')
                return
            if script['type'] == 'fetch':
                await ctx.send(f"Running {script['type']}: {script['name']}")
                end_file = Server_Func.fetch_file(server, script, config)
                await command_send(ctx, script["name"], files=end_file)
                return

    await ctx.send(f"Command '{server_command}' Not Found")


bot.start()
