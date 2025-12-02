# Dockerfile

# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt сначала для кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser /app
USER flaskuser

# Открываем порт
EXPOSE 5000

# Переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Команда запуска
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]