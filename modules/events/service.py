"""
Сервис для работы с событиями (спектаклями)
"""
from typing import Optional, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from database.models import Event, EventStatus


class EventService:
    """Сервис для работы с событиями"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_event(
        self,
        title: str,
        description: Optional[str] = None,
        start_time: datetime = None,
        duration_minutes: int = 120,
        price: float = 0,
        max_viewers: Optional[int] = None,
        poster_url: Optional[str] = None
    ) -> Event:
        """
        Создать новое событие
        
        Args:
            title: Название спектакля
            description: Описание
            start_time: Время начала
            duration_minutes: Длительность в минутах
            price: Цена билета
            max_viewers: Максимальное количество зрителей
            poster_url: URL афиши
            
        Returns:
            Event: Созданное событие
        """
        event = Event(
            title=title,
            description=description,
            start_time=start_time,
            duration_minutes=duration_minutes,
            price=price,
            max_viewers=max_viewers,
            poster_url=poster_url,
            status=EventStatus.UPCOMING
        )
        
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        
        logger.info(f"Создано событие: {event.title} (ID: {event.id})")
        return event
    
    async def get_event(self, event_id: int) -> Optional[Event]:
        """Получить событие по ID"""
        result = await self.session.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()
    
    async def get_upcoming_events(self) -> List[Event]:
        """Получить список предстоящих событий"""
        result = await self.session.execute(
            select(Event)
            .where(Event.status == EventStatus.UPCOMING)
            .where(Event.start_time > datetime.utcnow())
            .order_by(Event.start_time)
        )
        return list(result.scalars().all())
    
    async def get_all_events(self) -> List[Event]:
        """Получить все события"""
        result = await self.session.execute(
            select(Event).order_by(Event.start_time.desc())
        )
        return list(result.scalars().all())
    
    async def update_event_status(self, event_id: int, status: EventStatus) -> bool:
        """Обновить статус события"""
        event = await self.get_event(event_id)
        if not event:
            return False
        
        event.status = status
        await self.session.commit()
        
        logger.info(f"Статус события {event_id} изменен на {status}")
        return True
    
    async def set_stream_link(self, event_id: int, invite_link: str) -> bool:
        """Установить ссылку на трансляцию"""
        event = await self.get_event(event_id)
        if not event:
            return False
        
        event.invite_link = invite_link
        await self.session.commit()
        
        logger.info(f"Установлена ссылка на трансляцию для события {event_id}")
        return True
    
    async def delete_event(self, event_id: int) -> bool:
        """Удалить событие"""
        event = await self.get_event(event_id)
        if not event:
            return False
        
        await self.session.delete(event)
        await self.session.commit()
        
        logger.info(f"Событие {event_id} удалено")
        return True
