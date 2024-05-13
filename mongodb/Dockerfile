# Use a base image with MongoDB pre-installed
FROM mongo:latest

# Install curl and the AWS CLI
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y python3-pip && \
    pip3 install awscli

COPY backup.sh backup.sh
RUN chmod +x backup.sh
RUN mkdir usr/files/

# Set the default command to run MongoDB

CMD ["mongod", "--storageEngine", "wiredTiger", "--auth"]