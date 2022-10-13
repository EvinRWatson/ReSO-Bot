import os
import subprocess

import interactions
from interactions.ext.files import command_send


def call_script(server, script, params):
    server_command = f'{script["command"]} "{params.strip()}"'
    subprocess.run(["ssh", f"{server['username']}@{server['host']}", server_command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def fetch_file(server, file, config):
    file_location = file['location']
    file_destination = config['file_fetch']['fileDropClientFilePath']

    subprocess.run(["scp", f"{server['username']}@{server['host']}:{file_location}", file_destination])

    file_name = os.path.basename(file_location)
    file_path = f'{file_destination}/{file_name}'

    end_file = interactions.File(file_path)
    return end_file
