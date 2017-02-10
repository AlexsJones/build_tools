FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y  nodejs-legacy
RUN apt-get install -y npm
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN python3.5 --version
RUN git clone --recursive https://413e5065bdee6ee33391bbea98d19c00f5a6de57:x-oauth-basic@github.com/sky-uk/ce-devops-stats.git
WORKDIR ce-devops-stats
RUN npm i
RUN ./node_modules/bower/bin/bower install --allow-root
RUN pip3 install -r requirements.txt
