"""
Скрипт инициализации базы данных
"""
import asyncio
from loguru import logger

from config import setup_logging
from database import init_db


async def main():
    """Инициализация БД"""
    setup_logging()
    
    logger.info("Начало инициализации базы данных...")
    
    try:
        await init_db()
        logger.success("✅ База данных успешно инициализирована!")
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации БД: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
