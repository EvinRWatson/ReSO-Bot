FROM python:3

ADD . /

RUN apt-get update -y
RUN python3 -m pip install -U discord.py
RUN python3 -m pip install -U discord-py-interactions
RUN python3 -m pip install -U interactions-files
RUN apt-get install openssh-client vim nano

CMD [ "python", "./Bot.py" ]