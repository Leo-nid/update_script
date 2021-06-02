FROM ubuntu:latest

COPY server.py /server/server.py

RUN apt-get update

RUN apt-get -y install python3 python3-pip

RUN pip3 install requests

EXPOSE 8001

CMD python3 /server/server.py 8001 1
