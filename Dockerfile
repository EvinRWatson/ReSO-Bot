FROM python:3

ADD . /

RUN python3 -m pip install -U discord.py

CMD [ "python", "./Bot.py" ]