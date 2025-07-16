FROM ubuntu:22.04

# Обновление и установка зависимостей
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv nginx systemctl curl dbus && \
    pip install poetry && \
    apt-get clean

# Установка Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Копирование зависимостей
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копирование кода
COPY app ./app

# Копирование systemd unit-файла (имитация в контейнере, по необходимости)
RUN systemctl enable nginx

# Открываем порт
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
