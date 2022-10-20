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

    invalid_reasons = Bot_Func.check_invalid_user(ctx, config)
    invalid_characters = ["&", ";"]
    if any(character in bot_parameters for character in invalid_characters):
        invalid_reasons += "Invalid Characters\n"
    if invalid_reasons != "":
        message = f"Cannot execute command:\n{invalid_reasons}"
        Bot_Func.log_action(message, logger, ctx)
        await ctx.send(message)
        return

    try:
        server_name = bot_parameters.split(" ")[0]
        server_command = bot_parameters.split(" ")[1]
        command_parameters = bot_parameters.replace(server_name, '').replace(server_command, '').strip()
    except IndexError:
        message = 'There seems to be an error with your command format. Please use /reso_help for assistance'
        Bot_Func.log_action(message, logger, ctx)
        await ctx.send(message)
        return

    server = Bot_Func.get_object_by_name(server_name, config['servers'])
    if server is None:
        message = f"Server '{server_name}' Not Found"
        Bot_Func.log_action(message, logger, ctx)
        await ctx.send(message)
        return

    script = Bot_Func.get_object_by_name(server_command, config['scripts'])
    if script is None:
        message = f"Script '{server_command}' Not Found"
        Bot_Func.log_action(message, logger, ctx)
        await ctx.send(message)
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
    invalid_reasons = Bot_Func.check_invalid_user(ctx, config)
    if invalid_reasons != "":
        await ctx.send('Cannot execute command:\n' + invalid_reasons)
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
    invalid_reasons = Bot_Func.check_invalid_user(ctx, config)
    if invalid_reasons != "":
        await ctx.send('Cannot execute command:\n' + invalid_reasons)
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
