FROM python:3.9.14-alpine3.16
USER root
COPY ./web/* /web/
RUN apk update && pip install --upgrade pip && pip install pytest
ENTRYPOINT ["python", "pytest"]

