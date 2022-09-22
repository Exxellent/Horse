FROM python:3.11.0rc2-alpine3.16
USER root
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip install psycopg2
COPY ./* /app/
ENTRYPOINT ["python3", "/app/hello.py"]
