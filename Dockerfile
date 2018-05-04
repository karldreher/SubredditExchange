# Use official Python3 parent image
FROM python:3-alpine

WORKDIR /subreddit_exchange/

ADD templates/* templates/
ADD SubredditExchange.py .
ADD web.py .
ADD requirements.txt .

# Build will fail if config.yaml is missing.  This is intentional.
ADD config.yaml .


# Install any needed packages
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app when the container launches
CMD ["python", "/subreddit_exchange/web.py"]
