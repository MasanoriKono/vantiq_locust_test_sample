FROM python:3.8-alpine as builder

# build time dependencies
RUN apk update && \
        apk add --no-cache \
        gcc \
        g++ \
        musl-dev \
        libffi-dev \
        zeromq-dev \
        make \
        libzmq\
        git \
        && pip install locust pyzmq \
        && apk del gcc g++ musl-dev libffi-dev make zeromq-dev

RUN locust -V

RUN adduser -D locust
EXPOSE 8089 5557
USER locust
WORKDIR /home/locust

COPY ./run.sh .
SHELL ["/bin/ash", "-c"]
ENTRYPOINT ./run.sh

# turn off python output buffering
ENV PYTHONUNBUFFERED=1