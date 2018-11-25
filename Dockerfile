

# sudo docker build -t react_niginx_webhost .
# docker run --name some-nginx -d -p 8080:80 some-content-nginx
# docker run -p 5001:5001 react_niginx_webhost
# docker run -p 5001:5001 -it react_niginx_webhost

# got to http://localhost:8080/

#FROM ubuntu:18.04
FROM ubuntu:16.04

RUN apt-get update

RUN apt-get -y upgrade

RUN apt-get install -y python3 

RUN apt-get install -y python3-pip
RUN apt-get install -y git

RUN git clone https://github.com/Shimwell/database_GUI.git

RUN cd database_GUI && pip3 install -r requirements.txt --user

RUN apt-get install -y curl software-properties-common
#RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt-get install -y nodejs
RUN apt-get install -y build-essential
RUN cd database_GUI && npm install
#RUN cd database_GUI && npm audit fix
RUN cd database_GUI && npm install bootstrap --save
RUN cd database_GUI && npm install --save reactstrap react react-dom
RUN cd database_GUI && npm install react-table
RUN cd database_GUI && npm install react-select
RUN cd database_GUI && npm install reactstrap
RUN cd database_GUI && npm install react-plotly.js plotly.js
RUN cd database_GUI && npm install --save rc-slider
# RUN cd database_GUI && npm install -g serve

# add some unit tests
# RUN cd database_GUI && npm run start test  

RUN cd database_GUI && npm run build

# to serve the new site
# RUN cd database_GUI && serve -s build

RUN mkdir -p /usr/share/nginx/html

RUN cp -r database_GUI/build/* /usr/share/nginx/html

# COPY static-html-directory /usr/share/nginx/html

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

#RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list

RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list

RUN apt-get update
RUN apt-get install -y libcurl3

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

#RUN apt-get install -y tzdata
#RUN dpkg-reconfigure -f noninteractive tzdata
#RUN timedatectl set-timezone Europe/Bratislava

#RUN apt-get install -y mongodb-org-server
#RUN apt-get install -y mongodb-org=4.0.4 mongodb-org-server=4.0.4 mongodb-org-shell=4.0.4 mongodb-org-mongos=4.0.4 mongodb-org-tools=4.0.4
RUN apt-get install -y mongodb-org


RUN curl -sL https://packagecloud.io/AtomEditor/atom/gpgkey | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'

RUN apt-get update
RUN apt-get install -y atom

RUN pip3 install --upgrade --force-reinstall sphinx
RUN pip3 install --upgrade --force-reinstall pymongo

RUN mkdir -p /data/db
#RUN mongod --bind_ip_all & 
#RUN mongod &  

#RUN service mongod start

#RUN cd database_GUI/database_creation_tools && git pull


#RUN mongod &  
RUN mongod --fork --logpath /var/log/mongodb.log

RUN echo 'go to localhost:8080'



#EXPOSE 80
#EXPOSE 5001
#EXPOSE 5000



COPY . database_GUI/

RUN cd database_GUI/database_creation_tools && python3 create_database_nuclear.py

WORKDIR "database_GUI/database_creation_tools"


#ENTRYPOINT ["python3"]
#CMD ["rest_api_database_functions.py"]
