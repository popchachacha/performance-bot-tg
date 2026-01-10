# Быстрый Старт

## Шаг 1: Подготовка окружения

### Установка зависимостей (локально)

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

## Шаг 2: Настройка переменных окружения

```bash
# Скопировать пример
cp .env.example .env

# Отредактировать .env и заполнить:
# - BOT_TOKEN (получить у @BotFather)
# - ADMIN_IDS (ваш Telegram ID)
# - DB_PASSWORD (пароль для PostgreSQL)
# - OPENAI_API_KEY (для ИИ-функций)
```

## Шаг 3: Запуск через Docker (рекомендуется)

```bash
# Запустить все сервисы
docker-compose up -d

# Инициализировать БД
docker-compose exec bot python scripts/init_db.py

# Создать администратора
docker-compose exec bot python scripts/create_admin.py

# Просмотр логов
docker-compose logs -f bot
```

## Шаг 4: Запуск локально (без Docker)

```bash
# Запустить PostgreSQL и Redis (должны быть установлены)
# Или использовать только их из docker-compose:
docker-compose up -d postgres redis

# Инициализировать БД
python scripts/init_db.py

# Создать администратора
python scripts/create_admin.py

# Запустить бота
python bot/main.py
```

## Первые Шаги

1. **Откройте бота в Telegram** и отправьте `/start`
2. **Войдите в админ-панель**: `/admin`
3. **Создайте первое событие** через админ-панель
4. **Проверьте афишу**: `/events`

## Создание Трансляции (Вариант А - Telegram Native)

### Через Telegram Desktop/Web:

1. Создайте **приватный канал** для трансляций
2. Добавьте бота в администраторы канала
3. Начните **Live Stream** в канале
4. Скопируйте **invite link** на трансляцию
5. В админ-панели бота установите эту ссылку для события

### Через OBS Studio:

1. Установите [OBS Studio](https://obsproject.com/)
2. Настройте сцену для спектакля
3. В Telegram создайте Live Stream
4. Получите **RTMP URL и ключ** (если доступно)
5. Настройте в OBS: Settings → Stream
6. Начните трансляцию

## Полезные Команды

### Пользовательские:
- `/start` - Запустить бота
- `/menu` - Главное меню
- `/events` - Афиша спектаклей
- `/help` - Помощь

### Администраторские:
- `/admin` - Админ-панель
- Создание событий через интерактивный диалог
- Просмотр статистики

## Остановка

```bash
# Docker
docker-compose down

# Локально
# Ctrl+C в терминале с ботом
```

## Troubleshooting

### Бот не запускается
- Проверьте `.env` файл
- Убедитесь что PostgreSQL и Redis запущены
- Проверьте логи: `docker-compose logs bot`

### Ошибка подключения к БД
- Проверьте что PostgreSQL запущен
- Проверьте `DB_*` переменные в `.env`
- Попробуйте: `docker-compose restart postgres`

### Бот не отвечает
- Проверьте `BOT_TOKEN`
- Убедитесь что бот не запущен в другом месте
- Проверьте интернет-соединение

## Следующие Шаги

1. **Настроить платежи** - интеграция ЮKassa
2. **Добавить ИИ-контент** - настроить OpenAI API
3. **Кастомизировать** - изменить тексты и дизайн
4. **Масштабировать** - перейти на продакшн сервер

## Поддержка

Документация: `docs/`
- `prologue.md` - Видение проекта
- `modules_architecture.md` - Архитектура
- `project_structure.md` - Структура кода
