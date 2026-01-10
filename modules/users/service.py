"""
Сервис для работы с пользователями
"""
from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from database.models import User, UserRole


class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_or_create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        language_code: str = "ru"
    ) -> User:
        """
        Получить или создать пользователя
        
        Args:
            telegram_id: ID пользователя в Telegram
            username: Username пользователя
            first_name: Имя
            last_name: Фамилия
            language_code: Код языка
            
        Returns:
            User: Объект пользователя
        """
        # Пытаемся найти пользователя
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Обновляем last_active
            user.last_active = datetime.utcnow()
            # Обновляем данные если изменились
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            
            logger.info(f"Пользователь {telegram_id} обновлен")
        else:
            # Создаем нового пользователя
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                language_code=language_code,
                last_active=datetime.utcnow()
            )
            self.session.add(user)
            logger.info(f"Создан новый пользователь {telegram_id}")
        
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def is_admin(self, telegram_id: int) -> bool:
        """Проверить, является ли пользователь администратором"""
        user = await self.get_user(telegram_id)
        if not user:
            return False
        return user.role in [UserRole.ADMIN, UserRole.MODERATOR]
    
    async def set_admin(self, telegram_id: int, is_admin: bool = True) -> bool:
        """Назначить/снять права администратора"""
        user = await self.get_user(telegram_id)
        if not user:
            return False
        
        user.role = UserRole.ADMIN if is_admin else UserRole.USER
        await self.session.commit()
        
        logger.info(f"Пользователь {telegram_id} {'назначен' if is_admin else 'снят'} администратором")
        return True
