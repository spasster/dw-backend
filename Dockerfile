FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновление и установка необходимых пакетов
RUN apk update \
    && apk add --no-cache \
        build-base \
        mariadb-connector-c-dev \
        mariadb-dev \
        libffi-dev \
        openssl-dev \
        bash \
        netcat-openbsd

# Обновление pip
RUN pip install --upgrade pip

WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
ADD . /app/

EXPOSE 8000

# CMD ["python", "sk3d_pages/manage.py", "runserver", "0.0.0.0:8000"]
