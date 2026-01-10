"""
Обработчики для работы с событиями (спектаклями)
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from database.models import User
from modules.events import EventService
from bot.keyboards.inline import events_list_keyboard, event_detail_keyboard, back_to_main_keyboard

router = Router(name="events")


@router.message(Command("events"))
@router.callback_query(F.data == "events_list")
async def show_events_list(event: Message | CallbackQuery, db_session: AsyncSession):
    """
    Показать список предстоящих событий
    
    Args:
        event: Сообщение или callback
        db_session: Сессия БД (из middleware)
    """
    event_service = EventService(db_session)
    events = await event_service.get_upcoming_events()
    
    if not events:
        text = (
            "🎭 <b>Афиша</b>\n\n"
            "К сожалению, пока нет запланированных спектаклей.\n"
            "Следите за обновлениями!"
        )
        keyboard = back_to_main_keyboard()
    else:
        text = (
            "🎭 <b>Афиша предстоящих спектаклей</b>\n\n"
            f"Найдено событий: {len(events)}\n"
            "Выберите спектакль для подробной информации:"
        )
        keyboard = events_list_keyboard(events)
    
    if isinstance(event, Message):
        await event.answer(text, reply_markup=keyboard)
    else:
        await event.message.edit_text(text, reply_markup=keyboard)
        await event.answer()


@router.callback_query(F.data.startswith("event_"))
async def show_event_detail(callback: CallbackQuery, db_session: AsyncSession, db_user: User):
    """
    Показать детальную информацию о событии
    
    Args:
        callback: Callback query
        db_session: Сессия БД
        db_user: Пользователь
    """
    event_id = int(callback.data.split("_")[1])
    
    event_service = EventService(db_session)
    event = await event_service.get_event(event_id)
    
    if not event:
        await callback.answer("❌ Событие не найдено", show_alert=True)
        return
    
    # TODO: Проверить, есть ли у пользователя билет
    has_ticket = False
    
    # Форматирование даты
    start_time = event.start_time.strftime("%d.%m.%Y %H:%M")
    
    text = (
        f"🎭 <b>{event.title}</b>\n\n"
        f"📅 Дата: {start_time}\n"
        f"⏱ Длительность: {event.duration_minutes} мин\n"
        f"💰 Цена: {event.price} ₽\n\n"
    )
    
    if event.description:
        text += f"{event.description}\n\n"
    
    if event.max_viewers:
        # TODO: Подсчитать количество проданных билетов
        sold_tickets = 0
        text += f"🎫 Доступно мест: {event.max_viewers - sold_tickets} из {event.max_viewers}\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=event_detail_keyboard(event_id, has_ticket)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def buy_ticket(callback: CallbackQuery, db_session: AsyncSession, db_user: User):
    """
    Купить билет на событие
    
    Args:
        callback: Callback query
        db_session: Сессия БД
        db_user: Пользователь
    """
    event_id = int(callback.data.split("_")[1])
    
    event_service = EventService(db_session)
    event = await event_service.get_event(event_id)
    
    if not event:
        await callback.answer("❌ Событие не найдено", show_alert=True)
        return
    
    # TODO: Реализовать создание заказа и платежа
    
    text = (
        f"🎫 <b>Покупка билета</b>\n\n"
        f"Спектакль: {event.title}\n"
        f"Цена: {event.price} ₽\n\n"
        f"⚠️ Функция оплаты находится в разработке.\n"
        f"Для покупки билета обратитесь к администратору."
    )
    
    await callback.answer(text, show_alert=True)
    logger.info(f"Пользователь {db_user.telegram_id} пытается купить билет на событие {event_id}")


@router.callback_query(F.data.startswith("watch_"))
async def watch_stream(callback: CallbackQuery, db_session: AsyncSession, db_user: User):
    """
    Смотреть трансляцию
    
    Args:
        callback: Callback query
        db_session: Сессия БД
        db_user: Пользователь
    """
    event_id = int(callback.data.split("_")[1])
    
    event_service = EventService(db_session)
    event = await event_service.get_event(event_id)
    
    if not event:
        await callback.answer("❌ Событие не найдено", show_alert=True)
        return
    
    # TODO: Проверить наличие билета
    # TODO: Проверить, что трансляция идет
    
    if not event.invite_link:
        await callback.answer(
            "⚠️ Ссылка на трансляцию еще не готова. Попробуйте позже.",
            show_alert=True
        )
        return
    
    text = (
        f"▶️ <b>Трансляция: {event.title}</b>\n\n"
        f"Перейдите по ссылке для просмотра:\n"
        f"{event.invite_link}\n\n"
        f"Приятного просмотра! 🎭"
    )
    
    await callback.message.answer(text)
    await callback.answer()
    
    logger.info(f"Пользователь {db_user.telegram_id} смотрит событие {event_id}")
