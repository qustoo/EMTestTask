###########
# BUILDER #
###########
FROM python:3.10-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apk add --no-cache gcc build-base libffi-dev musl-dev postgresql-dev

#########
# FINAL #
#########
FROM builder AS production

# Указываем рабочий каталог
WORKDIR /app

# Копируем установленные зависимости из этапа сборки
COPY --from=builder /usr/src/app /app

# Создаем нового пользователя
RUN adduser -D user

EXPOSE 8080

# Переключаемся на пользователя
USER user

# Копирование кода в контейнер
COPY --chown=user:user . .

# Команда для запуска сервера с помощью Uvicorn
ENTRYPOINT ["/bin/sh", "-c", "alembic upgrade heads && python server.py"]