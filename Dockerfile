# Specify base image
FROM python:3.9-slim-buster

# Copy requirements first to leverage Docker caching
COPY ./requirements.txt /app/requirements.txt

# Set working directory for RUN, CMD, ENTRYPOINT, COPY, and ADD commands
WORKDIR /app

# Copy all the code inside the container workdir
COPY . /app

# Install pip packages
RUN pip install -r requirements.txt

# Copy the entrypoint script
COPY run.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run.sh

# Set the entrypoint
ENTRYPOINT ["run.sh"]
