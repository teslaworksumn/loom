# ExCEED Labs Site
# 
# VERSION 1.0

FROM ubuntu:quantal
MAINTAINER Taylor Trimble @tylrtrmbl

# Install packages
RUN echo "deb http://nginx.org/packages/mainline/ubuntu/ quantal nginx" >> /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/mainline/ubuntu/ quantal nginx" >> /etc/apt/sources.list
RUN apt-get -q -y update
RUN apt-get -q -y install nginx-full git python2.7 python-pip python-dev daemontools curl

# Install uWSGI
RUN pip install uWSGI

# Transfer this repo's contents to the image
ADD . /root/loom

# Install app deps
RUN pip install -r /root/loom/requirements.txt

# Set up nginx
ADD config/nginx_config /etc/nginx/sites-available/default

# Set up uWSGI and its service handler
ADD scripts/uwsgi_service.sh /root/uwsgi_service/run
RUN chmod a+x /root/uwsgi_service/run

# Transfer management scripts
ADD scripts/run.sh /root/run.sh
RUN chmod a+x /root/run.sh

# Retrieve Flask server from repo; start nginx; supervise uWSGI.
CMD /root/run.sh
