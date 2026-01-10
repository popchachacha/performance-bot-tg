# Варианты Структуры Проекта

## Обзор

Документ описывает три варианта организации файловой структуры проекта с учетом модульной архитектуры.

---

## Вариант 1: Монолитная Структура (Рекомендуется для MVP)

### Описание
Все модули находятся в одном проекте, но логически разделены по папкам.

### Структура Директорий

```
perfomance-bot-tg/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── config/
│   ├── settings.py          # Конфигурация (env переменные)
│   ├── database.py          # Настройки БД
│   └── logging.py           # Настройки логирования
│
├── bot/
│   ├── __init__.py
│   ├── main.py              # Точка входа бота
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── user.py          # Обработчики для пользователей
│   │   ├── admin.py         # Обработчики для админов
│   │   ├── events.py        # Обработчики событий/спектаклей
│   │   └── payments.py      # Обработчики платежей
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── inline.py        # Inline клавиатуры
│   │   └── reply.py         # Reply клавиатуры
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── auth.py          # Проверка авторизации
│   │   └── throttling.py    # Защита от спама
│   └── filters/
│       ├── __init__.py
│       └── admin.py         # Фильтр для админов
│
├── modules/
│   ├── __init__.py
│   │
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy модели
│   │   ├── service.py       # Бизнес-логика
│   │   └── schemas.py       # Pydantic схемы
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── service.py
│   │   └── schemas.py
│   │
│   ├── tickets/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── generator.py     # Генерация QR-кодов
│   │
│   ├── streaming/
│   │   ├── __init__.py
│   │   ├── service.py       # Управление доступом к трансляциям
│   │   ├── tokens.py        # Генерация токенов доступа
│   │   └── validators.py    # Проверка прав доступа
│   │
│   ├── payments/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   ├── yukassa.py       # Интеграция ЮKassa
│   │   └── webhooks.py      # Обработка вебхуков
│   │
│   ├── ai_content/
│   │   ├── __init__.py
│   │   ├── generator.py     # Генерация контента
│   │   ├── scheduler.py     # Планировщик постов
│   │   ├── openai_client.py # Клиент OpenAI
│   │   └── models.py
│   │
│   └── analytics/
│       ├── __init__.py
│       ├── service.py
│       └── metrics.py       # Сбор метрик
│
├── api/                     # FastAPI для Web App
│   ├── __init__.py
│   ├── main.py              # Точка входа API
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Авторизация
│   │   ├── events.py        # API событий
│   │   ├── streaming.py     # API трансляций
│   │   └── tickets.py       # API билетов
│   └── dependencies.py      # Зависимости FastAPI
│
├── webapp/                  # Frontend (Telegram Mini App)
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── player.js        # Видео плеер
│   │   └── api.js           # API клиент
│   └── assets/
│       └── images/
│
├── database/
│   ├── __init__.py
│   ├── base.py              # Base класс для моделей
│   ├── session.py           # Создание сессий
│   └── migrations/          # Alembic миграции
│       └── versions/
│
├── utils/
│   ├── __init__.py
│   ├── redis_client.py      # Redis клиент
│   ├── validators.py        # Общие валидаторы
│   └── helpers.py           # Вспомогательные функции
│
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_tickets.py
│   └── test_streaming.py
│
├── scripts/
│   ├── init_db.py           # Инициализация БД
│   ├── create_admin.py      # Создание админа
│   └── seed_data.py         # Тестовые данные
│
└── logs/
    └── .gitkeep
```

### Плюсы
- ✅ Простота разработки и деплоя
- ✅ Легко начать (один репозиторий)
- ✅ Общие зависимости и конфигурация
- ✅ Быстрая разработка MVP

### Минусы
- ❌ Сложнее масштабировать отдельные модули
- ❌ Все в одном процессе (падение одного модуля = падение всего)
- ❌ Усложняется при росте кодовой базы

### Когда использовать
- MVP и начальные этапы
- Команда до 3-5 разработчиков
- Нагрузка до 10,000 пользователей

---

## Вариант 2: Микросервисная Структура

### Описание
Каждый модуль - отдельный сервис со своей БД и API.

### Структура Директорий

```
perfomance-bot-tg/
├── README.md
├── docker-compose.yml       # Оркестрация всех сервисов
│
├── services/
│   │
│   ├── bot-service/         # Telegram Bot
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   ├── handlers/
│   │   └── config/
│   │
│   ├── user-service/        # Сервис пользователей
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py          # FastAPI приложение
│   │   ├── models/
│   │   ├── routes/
│   │   └── database/
│   │
│   ├── event-service/       # Сервис событий
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── ticket-service/      # Сервис билетов
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── streaming-service/   # Сервис трансляций
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── payment-service/     # Сервис платежей
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── ai-content-service/  # Сервис ИИ-контента
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py
│   │   └── ...
│   │
│   └── analytics-service/   # Сервис аналитики
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── main.py
│       └── ...
│
├── api-gateway/             # API Gateway (опционально)
│   ├── Dockerfile
│   ├── nginx.conf
│   └── ...
│
├── webapp/                  # Frontend
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│
├── shared/                  # Общие библиотеки
│   ├── auth/
│   ├── database/
│   └── utils/
│
└── infrastructure/
    ├── kubernetes/          # K8s манифесты
    ├── terraform/           # Infrastructure as Code
    └── monitoring/          # Prometheus, Grafana
```

### Плюсы
- ✅ Независимое масштабирование сервисов
- ✅ Изоляция отказов
- ✅ Разные технологии для разных сервисов
- ✅ Параллельная разработка командами

### Минусы
- ❌ Сложность инфраструктуры
- ❌ Overhead на коммуникацию между сервисами
- ❌ Сложнее отлаживать
- ❌ Требует DevOps экспертизу

### Когда использовать
- Большие нагрузки (>100,000 пользователей)
- Команда >5 разработчиков
- Требуется независимое масштабирование

---

## Вариант 3: Гибридная Структура (Модульный Монолит)

### Описание
Монолит с четким разделением модулей, готовый к выделению в микросервисы.

### Структура Директорий

```
perfomance-bot-tg/
├── README.md
├── requirements.txt
├── docker-compose.yml
│
├── apps/
│   │
│   ├── bot/                 # Telegram Bot приложение
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── handlers/
│   │   └── config.py
│   │
│   ├── api/                 # FastAPI приложение
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │
│   └── worker/              # Celery worker для фоновых задач
│       ├── __init__.py
│       ├── main.py
│       └── tasks/
│
├── core/                    # Ядро системы (общее для всех apps)
│   ├── __init__.py
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   └── exceptions/
│       └── handlers.py
│
├── domain/                  # Бизнес-логика (Domain-Driven Design)
│   │
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py        # Domain модели
│   │   ├── repository.py    # Интерфейс репозитория
│   │   ├── service.py       # Бизнес-логика
│   │   └── schemas.py       # DTO
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── schemas.py
│   │
│   ├── tickets/
│   │   └── ...
│   │
│   ├── streaming/
│   │   └── ...
│   │
│   ├── payments/
│   │   └── ...
│   │
│   ├── ai_content/
│   │   └── ...
│   │
│   └── analytics/
│       └── ...
│
├── infrastructure/          # Реализация репозиториев и внешних сервисов
│   ├── database/
│   │   ├── repositories/    # SQLAlchemy реализации
│   │   └── models.py        # ORM модели
│   ├── external/
│   │   ├── openai.py
│   │   ├── yukassa.py
│   │   └── telegram.py
│   └── cache/
│       └── redis.py
│
├── webapp/
│   └── ...
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── scripts/
    └── ...
```

### Плюсы
- ✅ Чистая архитектура (Clean Architecture)
- ✅ Легко тестировать
- ✅ Готовность к выделению в микросервисы
- ✅ Четкое разделение ответственности
- ✅ Простота деплоя (как монолит)

### Минусы
- ❌ Больше boilerplate кода
- ❌ Требует понимания DDD
- ❌ Медленнее разработка на старте

### Когда использовать
- Долгосрочный проект
- Команда знакома с Clean Architecture
- Планируется рост до микросервисов

---

## Сравнительная Таблица

| Критерий | Монолит | Микросервисы | Гибрид |
|----------|---------|--------------|--------|
| Сложность старта | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Скорость разработки MVP | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Масштабируемость | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Поддерживаемость | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Тестируемость | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| DevOps сложность | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## Рекомендация

### Для текущего проекта:

**Начать с Варианта 1 (Монолит)**, затем:
1. **Фаза 1 (0-3 месяца)**: Монолитная структура для быстрого MVP
2. **Фаза 2 (3-6 месяцев)**: Рефакторинг в Вариант 3 (Гибрид) при росте кодовой базы
3. **Фаза 3 (6+ месяцев)**: Выделение критичных модулей (streaming, payments) в микросервисы

### Критерии перехода:
- **К Гибриду**: Когда кодовая база >10,000 строк или команда >3 человек
- **К Микросервисам**: Когда нагрузка >50,000 активных пользователей или нужно независимое масштабирование

---

## Следующие Шаги

1. Создать базовую структуру Варианта 1
2. Настроить окружение (Docker, PostgreSQL, Redis)
3. Реализовать первый модуль (Users) как шаблон
4. Настроить CI/CD пайплайн
