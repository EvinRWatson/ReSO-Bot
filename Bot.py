import yaml

import interactions

import Bot_Func
import Server_Func

print('Loading:')
print('\tLogger')
logger = Bot_Func.initialize_logger()

print('\tConfig')
config = yaml.safe_load(open('config.yml'))

print('Checking for token')
Bot_Func.prevent_start_without_token(config)

print('Initialize Client')
bot = interactions.Client(token=config['general']['botToken'],
                          default_scope=str(config['general']['guildId']))


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
    await ctx.send('Command Received')

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

    server = Bot_Func.get_object_by_name(server_name, config['servers'])
    if server is None:
        await ctx.send(f"Server '{server_name}' Not Found")
        return

    script = Bot_Func.get_object_by_name(server_command, config['scripts'])
    if script is None:
        await ctx.send(f"Script '{server_command}' Not Found")
        return

    await Server_Func.run(ctx, config, server, script, command_parameters)


@bot.command(
    name='reso_help',
    description="Display help information",
    dm_permission=False
)
async def reso_help(ctx: interactions.CommandContext):
    output = "Command Format: /reso <server-name> <command-name> <parameters>"
    await ctx.send("Help Info")


print('Start Client')
bot.start()
