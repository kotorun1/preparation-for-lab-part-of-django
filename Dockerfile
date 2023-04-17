# Указываем базовый образ
FROM python:3.9

# Создаем директорию для нашего кода
WORKDIR /app

# Копируем зависимости проекта
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все содержимое текущей директории внутрь контейнера
COPY . .

RUN python manage.py makemigrations
# Применяем миграции
RUN python manage.py migrate

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем команду, которая запускает сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

