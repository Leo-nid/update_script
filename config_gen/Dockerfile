FROM ubuntu:latest


RUN apt-get update -y
RUN apt-get install -y nginx

EXPOSE 80 443

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /etc/nginx

CMD ["nginx"]
