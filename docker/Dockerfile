FROM python:3.8-alpine

# build time dependencies
RUN apk update && \
        apk add --no-cache \
        gcc \
        g++ \
        musl-dev \
        libffi-dev \
        zeromq-dev \
        make \
        cmake \
        openssl \
        libzmq\
        libressl-dev \
        git \
        bash \
        && pip install locust pyzmq numpy paho-mqtt  \
        && apk del gcc g++ musl-dev libffi-dev make cmake zeromq-dev

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