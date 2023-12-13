FROM nginx:stable-alpine

RUN apk --no-cache add certbot

COPY default.conf /etc/nginx
COPY default.conf /etc/nginx/conf.d
