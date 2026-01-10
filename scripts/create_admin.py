"""
Скрипт для создания первого администратора
"""
import asyncio
from loguru import logger

from config import setup_logging, settings
from database import get_session
from modules.users import UserService


async def main():
    """Создание администратора"""
    setup_logging()
    
    logger.info("Создание администратора...")
    
    if not settings.admin_list:
        logger.error("❌ Не указаны ADMIN_IDS в .env файле!")
        return
    
    admin_id = settings.admin_list[0]
    
    async for session in get_session():
        user_service = UserService(session)
        
        # Создаем или получаем пользователя
        user = await user_service.get_or_create_user(
            telegram_id=admin_id,
            first_name="Admin"
        )
        
        # Назначаем администратором
        await user_service.set_admin(admin_id, True)
        
        logger.success(f"✅ Пользователь {admin_id} назначен администратором!")
        break


if __name__ == "__main__":
    asyncio.run(main())
