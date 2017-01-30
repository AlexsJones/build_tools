FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y  nodejs-legacy
RUN apt-get install -y npm
RUN apt-get install -y git
RUN npm install -g bower
