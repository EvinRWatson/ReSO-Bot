import os
import subprocess

import interactions
from interactions.ext.files import command_send

import Bot_Func


async def run(ctx, config, server, script, command_parameters):
    if script['type'] == 'command':
        await ctx.send(f"Running {script['type']}: {script['name']}")
        run_command(server, script, command_parameters)
        await ctx.send("Complete")
        return
    if script['type'] == 'fetch':
        await ctx.send(f"Running {script['type']}: {script['name']}")
        end_file = run_fetch(server, script, config)
        await command_send(ctx, script['name'], files=end_file)
        return


def run_command(server, command, params):
    server_command = f'{command["command"]} "{params.strip()}"'
    subprocess.run(["ssh", f"{server['username']}@{server['host']}", server_command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def run_fetch(server, script, config):
    file_location = script['location']
    file_destination = config['general']['fileDropClientFilePath']

    subprocess.run(["scp", f"{server['username']}@{server['host']}:{file_location}", file_destination])

    file_name = os.path.basename(file_location)
    file_path = f'{file_destination}/{file_name}'

    end_file = interactions.File(file_path)
    return end_file


def is_server_up(server_name: str, config):
    server = Bot_Func.get_object_by_name(server_name, config['servers'])

    response = os.system("ping -c 1 " + server['host'])

    return response == 0

