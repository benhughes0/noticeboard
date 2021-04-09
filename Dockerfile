FROM ubuntu:20.04
RUN dpkg-reconfigure debconf -f noninteractive -p critical && \
    DEBIAN_FRONTEND=noninteractive apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3.9
RUN mkdir -p /project
ADD . /project
WORKDIR /project
CMD ["python3.9", "bin/noticeboard_server.py", "--host", "0.0.0.0"]
