import os
import subprocess

import interactions


def run_command(server, command, params):
    server_command = f'{command["command"]} "{params.strip()}"'
    subprocess.run(["ssh", f"{server['username']}@{server['host']}", server_command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   check=False)


def run_fetch(server, file, config):
    file_location = file['location']
    file_destination = config['general']['fileDropClientFilePath']

    subprocess.run(["scp", f"{server['username']}@{server['host']}:{file_location}", file_destination])

    file_name = os.path.basename(file_location)
    file_path = f'{file_destination}/{file_name}'

    end_file = interactions.File(file_path)
    return end_file
