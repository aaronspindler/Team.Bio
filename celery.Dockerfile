FROM library/python:3.10-alpine

RUN apk update && apk upgrade && apk add --no-cache make g++ bash git openssh postgresql-dev curl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /usr/src/app

EXPOSE 80

CMD ["celery", "--app", "config.celery", "worker", "-B", "--loglevel", "info", "--concurrency", "5", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]