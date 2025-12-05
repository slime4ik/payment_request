# Система аутентификации и авторизации с JWT

### Содержание
- [Локальная разработка](#локальная-разработка)
- [Эндпоинты](#api-endpoints)
- [Запуск тестов](#запуск-тестов)
- [Продакшен](#продакшен)
---

### Локальная разработка
> (должна быть поднята база(postgreSQL с именем request, можно использовать sqlite или просто запустить проект через докер)
```bash
# 1. Клонируй репозиторий
git clone https://github.com/slime4ik/account.git
cd account

# 2. Создай и активируй env
uv venv env
source env/bin/activate  # Для Windows: env\Scripts\activate

# 3. Установить зависимости
uv pip install -r requirements.txt

# 4. Примени миграции
python manage.py migrate

# 5. Запуск Celery(для проверки заявки)
celery -A supermaster worker -l info

# 6. Запуск сервера
python manage.py runserver
```
## API Endpoints
### DEBUG URLS(основные)
- `GET /api/schema/swagger-ui/` — Свагер(все готово просто подставь свои данные)

### Заявки
- `GET /api/requests/` — Список заявок
- `POST /api/requests/` — Создать заявку
- `GET /api/requests/{id}/` — Получить заявку по id
- `PATCH /api/requests/{id}/` — Обновить статаус заявки(частично)
- `DELETE /api/requests/{id}/` — Удалить заявку
- `POST /api/token/refresh/` — Обновление access токена


### Запуск тестов
```bash
# Запуск тестов
python manage.py test
```

# Продакшен
### 1.Написать nginx(раздача статики, медиа, прокси), свои домены(ALLOWED_HOSTS, etc.), cors и прочие настройки безопасности(в prod.py) и поменять импорт в __init__.py в папке settings
### 2.Вынести переменые в .env(DB, cache, rmq settings)
### 3. Настроить сервисы в докере под систему на которой деплоим, воркеры, память редис, CONN_MAX_AGE в настрйоках django и прочие настройки оптимизации
