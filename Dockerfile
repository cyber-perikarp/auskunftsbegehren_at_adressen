FROM ubuntu:latest
LABEL maintainer="Sebastian Elisa Pfeifer <sebastian.pfeifer@unicorncloud.org>"

WORKDIR /opt

RUN apt-get update && \
  apt-get install -y python3-pip python3-dev libmysqlclient-dev && \
  pip3 install --upgrade pip && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get clean

ENV MYSQL_HOST localhost
ENV MYSQL_PASSWORD auskunftsbegehren_at
ENV MYSQL_USER auskunftsbegehren_at
ENV MYSQL_DATABASE auskunftsbegehren_at

COPY . /opt

RUN pip3 install -r /opt/requirements.txt

ENTRYPOINT ["python3", "/opt/convert-to-sql.py", "$MYSQL_HOST", "$MYSQL_USER", "$MYSQL_PASSWORD", "$MYSQL_DATABASE"]
