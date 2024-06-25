FROM python:3.12-alpine

RUN apk update && apk add nginx
RUN mkdir /botsockets

RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

WORKDIR /wkpnbot

COPY ./wkpnbot ./wkpnbot
COPY pyproject.toml wkpnbot.toml ./
RUN pip3 install . && pip3 install supervisor

COPY configs/nginx.conf /etc/nginx/
COPY configs/supervisor.conf /supervisord/

WORKDIR /

ENTRYPOINT supervisord -c /supervisord/supervisor.conf && tail -f /dev/null