"""
Middleware для авторизации и работы с пользователями
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loguru import logger

from database import get_session
from modules.users import UserService


class AuthMiddleware(BaseMiddleware):
    """Middleware для автоматического создания/обновления пользователей"""
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка события
        
        Args:
            handler: Следующий обработчик
            event: Событие (Message или CallbackQuery)
            data: Данные для передачи в обработчик
        """
        # Получаем пользователя из события
        user = event.from_user
        
        if not user:
            return await handler(event, data)
        
        # Создаем сессию БД
        async for session in get_session():
            user_service = UserService(session)
            
            # Получаем или создаем пользователя
            db_user = await user_service.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language_code=user.language_code or "ru"
            )
            
            # Добавляем пользователя и сервисы в data
            data["db_user"] = db_user
            data["user_service"] = user_service
            data["db_session"] = session
            
            logger.debug(f"Пользователь {user.id} обработан middleware")
            
            # Вызываем следующий обработчик
            return await handler(event, data)
