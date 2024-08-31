FROM python:3.12.2-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновление и установка необходимых пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libmariadb-dev-compat \
        libmariadb-dev \
        libffi-dev \
        libssl-dev \
        pkg-config \
        bash \
    && rm -rf /var/lib/apt/lists/*

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
