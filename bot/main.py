"""
Главный файл Telegram бота
"""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from config import settings, setup_logging
from database import init_db, close_db

from bot.handlers import user, admin, events
from bot.middlewares.auth import AuthMiddleware


async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    logger.info("🚀 Запуск бота...")
    
    # Инициализация БД
    await init_db()
    logger.success("✅ База данных инициализирована")
    
    # Уведомление админов о запуске
    for admin_id in settings.admin_list:
        try:
            await bot.send_message(
                admin_id,
                "🎭 <b>Бот запущен!</b>\n\n"
                "Система онлайн-спектаклей готова к работе.",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить сообщение админу {admin_id}: {e}")


async def on_shutdown(bot: Bot):
    """Действия при остановке бота"""
    logger.info("🛑 Остановка бота...")
    
    # Уведомление админов об остановке
    for admin_id in settings.admin_list:
        try:
            await bot.send_message(
                admin_id,
                "⚠️ <b>Бот остановлен</b>",
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass
    
    # Закрытие соединения с БД
    await close_db()
    logger.success("✅ Соединение с БД закрыто")


async def main():
    """Главная функция"""
    # Настройка логирования
    setup_logging()
    
    # Создание бота и диспетчера
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    # Регистрация middleware
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    
    # Регистрация роутеров
    dp.include_router(user.router)
    dp.include_router(events.router)
    dp.include_router(admin.router)
    
    # Регистрация startup/shutdown хуков
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Запуск polling
    logger.success("✅ Бот успешно запущен!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
