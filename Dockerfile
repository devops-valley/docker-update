FROM alpine:3.7
RUN apk add --update --no-cache py3-yaml bash && pip3 install docker-compose