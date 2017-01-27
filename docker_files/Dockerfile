FROM ubuntu:16.04
COPY ce-devops-stats/ tmp/ce-devops-stats/
COPY goldmaster_keys/ tmp/goldmaster_keys/
RUN cp -r tmp/ce-devops-stats ~
RUN cp -r tmp/goldmaster_keys ~
RUN apt-get update
RUN apt-get install -y  nodejs-legacy
RUN apt-get install -y npm
RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y python3.5
RUN curl -L https://npmjs.org/install.sh | sh
RUN npm install -g bower
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN apt-get install -y python3-pip
RUN pip3 install flask
RUN cd ~/ce-devops-stats && pip3 install -r requirements.txt
RUN cd ~/ce-devops-stats/
RUN cp ~/ce-devops-stats/bower.json ~/ce-devops-stats/package.json
RUN cd ~/ce-devops-stats && npm install
RUN cd ~/ce-devops-stats && bower install --allow-root
