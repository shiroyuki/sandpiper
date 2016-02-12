FROM python:alpine

RUN apk update
RUN apk add openjdk7
RUN apk add curl
RUN apk add make
RUN mkdir -p /db

WORKDIR /db

RUN curl -v --location -O http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
RUN tar xzf dynamodb_local_latest.tar.gz

WORKDIR /opt

CMD make test-dynamodb-docker-runner
