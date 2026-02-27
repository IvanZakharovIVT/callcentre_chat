# Используем официальный образ Python 3.14 (когда он выйдет, пока используем 3.12)
FROM python:3.12-slim

# Устанавливаем системные зависимости для Ansible и Python пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Ansible
RUN pip install --no-cache-dir ansible

# Создаем директорию для проекта
WORKDIR /app

# Копируем только requirements.txt для кэширования зависимостей
COPY apps/requirements.txt ./apps/

# Переходим в apps и устанавливаем зависимости
WORKDIR /app/apps
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
WORKDIR /app
COPY apps/ ./apps/

# Команда по умолчанию
CMD ["/bin/bash"]