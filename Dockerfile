FROM frolvlad/alpine-python3:latest
COPY . /app

ENV MYSQL_HOST localhost
ENV MYSQL_PASSWORD auskunftsbegehren_at
ENV MYSQL_USER auskunftsbegehren_at
ENV MYSQL_DATABASE auskunftsbegehren_at

RUN pip3 -r install /app/requirements.txt

ENTRYPOINT ["python3", "/app/convert-to-sql.py $MYSQL_HOST $MYSQL_USER $MYSQL_PASSWORD $MYSQL_DATABASE"]
