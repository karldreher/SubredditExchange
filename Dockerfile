# Use official Python3 parent image
FROM python:3-alpine

WORKDIR /subreddit_exchange/

ADD config.yaml config.yaml
ADD SubredditExchange.py SubredditExchange.py
ADD web.py web.py
ADD requirements.txt requirements.txt
ADD /templates/index.html templates/index.html

# Install any needed packages
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "/subreddit_exchange/web.py"]
