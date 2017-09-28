FROM ubuntu:latest
 
# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade
 
# Install Python
RUN apt-get install -y python-dev python-pip
 
# Add requirements.txt
ADD requirements.txt /redditapp
 
# Install uwsgi Python web server
RUN pip install uwsgi
# Install app requirements
RUN pip install -r requirements.txt
 
# Create app directory
ADD . /redditapp
 
# Set the default directory for our environment
ENV HOME /reddit
WORKDIR /redditapp
 
# Expose port 8000 for uwsgi
EXPOSE 8000
 
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
