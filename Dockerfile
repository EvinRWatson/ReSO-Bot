FROM python:3

ADD . /

ARG interactions_link=https://github.com/interactions-py/library.git#egg=discord-py-interactions

RUN python3 -m pip install -U discord.py
RUN python3 -m pip install -e git+$interactions_link
RUN apt-get install openssh-client

CMD [ "python", "./Bot.py" ]