FROM python:latest

RUN apt-get update
RUN apt-get install -y openjdk-7-jdk curl make
RUN mkdir -p /db

WORKDIR /db

RUN curl --location -O http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
RUN tar xzf dynamodb_local_latest.tar.gz

WORKDIR /opt

CMD make test-dynamodb-docker-runner
