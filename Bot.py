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
            name="server_name",
            description="Server Name",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="command_name",
            description="Server Command",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="command_parameters",
            description="Optional Parameters",
            type=interactions.OptionType.STRING,
            required=False
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, server_name: str, command_name: str, command_parameters: str = ""):
    await ctx.send('Command Received')

    exception_message: str = None

    try:
        Bot_Func.check_invalid_user(ctx, config)
        Bot_Func.prevent_command_chaining(command_parameters)
        server = Bot_Func.get_object_by_name(server_name, config['servers'])
        script = Bot_Func.get_object_by_name(command_name, config['scripts'])
    except PermissionError as pe:
        exception_message = f"Cannot execute command:\n{str(pe)}"
    except KeyError as ke:
        exception_message = str(ke)

    if exception_message is not None:
        Bot_Func.log_action(exception_message, logger, ctx)
        await ctx.send(exception_message)
        return

    log_message = f"Running {script['name']} on {server_name} with the following parameters: {command_parameters}"
    Bot_Func.log_action(log_message, logger, ctx)
    await Server_Func.run(ctx, config, server, script, command_parameters)


@bot.command(
    name='reso_help',
    description="Display help information",
    dm_permission=False
)
async def reso_help(ctx: interactions.CommandContext):
    try:
        Bot_Func.check_invalid_user(ctx, config)
    except PermissionError as pe:
        exception_message = f"Cannot execute command:\n{pe}"
        Bot_Func.log_action(exception_message, logger, ctx)
        await ctx.send(exception_message)
        return

    log_message = 'Used reso_help'
    Bot_Func.log_action(log_message, logger, ctx)

    help_message = Bot_Func.get_help_message(config)

    await ctx.send(help_message)


@bot.command(
    name='reso_ping',
    description="Ping server",
    options=[
        interactions.Option(
            name="server_name",
            description="Name of server to ping",
            type=interactions.OptionType.STRING,
            required=True
        )
    ],
    dm_permission=False
)
async def reso_help(ctx: interactions.CommandContext, server_name: str):
    try:
        Bot_Func.check_invalid_user(ctx, config)
    except PermissionError as pe:
        exception_message = f"Cannot execute command:\n{pe}"
        Bot_Func.log_action(exception_message, logger, ctx)
        await ctx.send(exception_message)
        return

    message = f'Pinging server: {server_name}'
    Bot_Func.log_action(message, logger, ctx)
    await ctx.send(message)

    if Server_Func.is_server_up(server_name, config):
        await ctx.send(f'{server_name} server is up!')
    else:
        await ctx.send(f'{server_name} server is down!')


Bot_Func.log_action('Start RESO Client', logger)
bot.start()
