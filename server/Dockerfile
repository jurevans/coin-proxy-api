FROM python:3.8.5-slim-buster

LABEL maintainer="Justin R. Evans<jurevans@gmail.com>"

COPY . /

RUN pip install -r requirements.txt && pip install gunicorn

ENTRYPOINT ["/run.sh"]
