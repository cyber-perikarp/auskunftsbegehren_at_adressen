FROM python:3.6.4-slim-stretch
LABEL maintainer="Sebastian Elisa Pfeifer <sebastian.pfeifer@unicorncloud.org>"

WORKDIR /opt

RUN apt-get update && \
  apt-get install -y python3-pip python3-dev libmariadbclient-dev && \
  apt-get install -y build-essential python-dev openssl libssl-dev && \
  pip3 install --upgrade pip && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get clean

COPY . /opt

RUN pip3 install -r /opt/requirements.txt

ENTRYPOINT ["python3", "/opt/convert-to-sql.py", "database", "auskunftsbegehren_at", "auskunftsbegehren_at", "auskunftsbegehren_at"]
