"""
Фильтр для проверки прав администратора
"""
from aiogram.filters import Filter
from aiogram.types import Message

from config import settings


class IsAdminFilter(Filter):
    """Фильтр для проверки, является ли пользователь администратором"""
    
    async def __call__(self, message: Message) -> bool:
        """
        Проверка прав администратора
        
        Args:
            message: Сообщение от пользователя
            
        Returns:
            bool: True если пользователь админ
        """
        return message.from_user.id in settings.admin_list
