import interactions

import Bot_Func
import Server_Func

print("Loading Config")
config: dict = Bot_Func.get_config()

print("Checking for token")
Bot_Func.prevent_start_without_token(config)

print("Initialize Client")
bot: interactions.Client = interactions.Client(token=config['general']['botToken'],
                                               default_scope=str(config['general']['guildId']))


@bot.command(
    name="reso",
    description="Remote Server Operation Bot",
    options=[
        interactions.Option(
            name="run",
            description="Run Command",
            type=interactions.OptionType.SUB_COMMAND,
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
        ),
        interactions.Option(
            name="help",
            description="Displays help information",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="ping",
            description="Determines whether a server is reachable or not",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="server_name",
                    description="Name of server to ping",
                    type=interactions.OptionType.STRING,
                    required=True
                )
            ],
        ),
        interactions.Option(
            name="reload",
            description="Reloads configuration file",
            type=interactions.OptionType.SUB_COMMAND,
        )
    ],
    dm_permission=False
)
async def reso(ctx: interactions.CommandContext, sub_command: str, server_name: str = "", command_name: str = "",
               command_parameters: str = ""):
    await ctx.send("Command Received")

    exception_message: str = None

    try:
        if sub_command == 'run':
            await reso_run(ctx, server_name, command_name, command_parameters)
        if sub_command == 'help':
            await reso_help(ctx)
        if sub_command == 'ping':
            await reso_ping(ctx, server_name)
        if sub_command == 'reload':
            await reso_reload(ctx)
    except PermissionError as pe:
        exception_message = str(pe)
    except KeyError as ke:
        exception_message = str(ke)
    except Exception as e:
        exception_message = "Unexpected Error"

    if exception_message is not None:
        await Bot_Func.respond_and_log(ctx, exception_message)
        return


async def reso_run(ctx: interactions.CommandContext, server_name: str, command_name: str, command_parameters: str = ""):
    Bot_Func.prevent_invalid_user(ctx, config)
    server: dict = Bot_Func.get_object_by_name(server_name, config['servers'])
    script: dict = Bot_Func.get_object_by_name(command_name, config['scripts'])
    script['command'] = Bot_Func.inject_params(script['command'], command_parameters)

    log_message: str = f"Running {script['name']} on {server_name} with the parameters: {command_parameters}"
    await Bot_Func.respond_and_log(ctx, log_message)
    await Server_Func.run(ctx, config, server, script)


async def reso_help(ctx: interactions.CommandContext):
    Bot_Func.prevent_invalid_user(ctx, config)

    log_message: str = 'Used reso_help'
    Bot_Func.log_action(log_message, ctx)

    await ctx.send(Bot_Func.get_help_message(config))


async def reso_ping(ctx: interactions.CommandContext, server_name: str):
    Bot_Func.prevent_invalid_user(ctx, config)

    message: str = f'Pinging server: {server_name}'
    await Bot_Func.respond_and_log(ctx, message)

    if Server_Func.is_server_up(server_name, config):
        await ctx.send(f'{server_name} server is up!')
    else:
        await ctx.send(f'{server_name} server is down!')


async def reso_reload(ctx: interactions.CommandContext):
    global config
    config = Bot_Func.get_config()
    await Bot_Func.respond_and_log(ctx, "Reloading Configuration")

Bot_Func.log_action('Start RESO Client')
bot.start()
