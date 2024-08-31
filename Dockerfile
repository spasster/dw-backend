FROM python:3.12.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update \
    && apk add --no-cache \
        build-base \
        mariadb-connector-c-dev \
        mariadb-dev \
        libffi-dev \
        openssl-dev \
        pkgconfig \
        bash

# Обновление pip python
RUN pip install --upgrade pip
WORKDIR /app

# Установка пакетов для проекта
COPY requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 8000

# CMD ["python", "sk3d_pages/manage.py", "runserver", "0.0.0.0:8000"]
