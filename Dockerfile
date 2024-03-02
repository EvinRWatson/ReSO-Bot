FROM python:3

ADD . /

RUN apt-get update -y
RUN python3 -m pip install -U pyyaml discord.py discord-py-interactions interactions-files
RUN apt-get install openssh-client vim nano iputils-ping curl -y
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

CMD [ "python", "./Bot.py" ]