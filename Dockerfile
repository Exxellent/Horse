FROM python:3.9.14-alpine3.16
USER root
COPY ./web/* /web/
RUN apk update && pip install --upgrade pip && apk add postgresql-dev gcc g++ python3-dev musl-dev && pip install -r web/req.txt
WORKDIR /web/
EXPOSE 1234
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
