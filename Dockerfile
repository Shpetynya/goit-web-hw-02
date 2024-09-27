# Використовуємо базовий образ з Python 3.12
FROM python:3.12-slim

# Встановлюємо необхідні системні залежності
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо віртуальне середовище Python
RUN python -m venv /opt/venv

# Встановлюємо віртуальне середовище як дефолтне середовище Python
ENV PATH="/opt/venv/bin:$PATH"

# Створюємо робочу директорію для застосунку
WORKDIR /app

# Копіюємо всі файли проекту у контейнер
COPY . /app

# Оновлюємо pip і встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Вказуємо команду для запуску "Персонального помічника" через файл main.py
CMD ["python", "main.py"]
