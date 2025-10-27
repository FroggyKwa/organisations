## Запуск

1. Создать файл окружения `.docker/.env` с содержимым:

```env
POSTGRES_USER=postgress
POSTGRES_PASSWORD=postgress
POSTGRES_HOST=database
POSTGRES_DB=db
DATABASE_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@database:5432/${POSTGRES_DB}"
DEBUG=true

API_KEY=ultrasuperdupersecretkey
```

2. Запустить контейнеры:

```bash
docker-compose -f .docker/docker-compose.yml up -d
```

3. Заполнить базу тестовыми данными:

```docker-compose -f .docker/docker-compose.yml run api python init_test_data.py```


Swagger доступен по `http://host:8000/docs`, Redoc по `http://host:8000/redoc`

## Тесты

- Тесты автоматически запускаются при старте контейнера.
- Для запуска извне:

docker-compose -f `.docker/docker-compose.yml run api pytest`