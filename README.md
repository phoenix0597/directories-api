## Запуск приложения

### 1. Склонировать репозиторий с исходным кодом и перейти в папку `directories-api`:

```bash
git clone https://github.com/phoenix0597/directories-api.git && cd directories-api
```

### 2. Запустить приложение:

```bash
docker compose up -d --build
```

### 3. Выполнить миграцию базы данных:

```bash
docker compose exec web sh -c "alembic upgrade head"
```

### 4. Заполнить базу данных демо данными:

SQL-запрос с тестовыми данными находится в файле `app/db/demo_data/fill_demo_db.sql`.

### 5. Проверить работу API: открыть в браузере `http://localhost:8000/docs`
