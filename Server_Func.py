import os
import subprocess

import interactions
from interactions.ext.files import command_send

import Bot_Func


async def run(ctx: interactions.CommandContext, config: dict, server: dict, script: dict, run_script: str):
    if script['type'] == 'command':
        run_command(server, script, run_script)
        await ctx.send("Complete")
        return
    if script['type'] == 'fetch':
        end_file: interactions.File = run_fetch(server, script, config)
        await command_send(ctx, script['name'], files=end_file)
        return


def run_command(server: dict, script: dict, run_script: str):
    subprocess.run(["ssh", f"{server['username']}@{server['host']}", run_script],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def run_fetch(server: dict, script: dict, config: dict):
    file_location: str = script['location']
    file_destination: str = config['general']['fileDropClientFilePath']

    subprocess.run(["scp", f"{server['username']}@{server['host']}:{file_location}", file_destination])

    file_name: str = os.path.basename(file_location)
    file_path: str = f'{file_destination}/{file_name}'

    return interactions.File(file_path)


def is_server_up(server_name: str, config: dict):
    server: dict = Bot_Func.get_object_by_name(server_name, config['servers'])

    response: int = os.system("ping -c 1 " + server['host'])

    return response == 0

