FROM ubuntu:latest
MAINTAINER Adam Konieczny "adam.konieczny@cervirobotics.com"
# ENV http_proxy "http://165.225.104.34:80"
# ENV https_proxy "http://165.225.104.34:80"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential python-numpy python-opencv
RUN mkdir /drone_stabilization
COPY . /drone_stabilization
WORKDIR /drone_stabilization
# ENV http_proxy ""
# ENV https_proxy ""
ENTRYPOINT ["/usr/bin/python"]
CMD ["run.py"]
EXPOSE "10000"
