"""
Обработчики для администраторов
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from loguru import logger

from database.models import User
from modules.events import EventService
from bot.filters.admin import IsAdminFilter
from bot.keyboards.inline import admin_menu_keyboard, back_to_main_keyboard

router = Router(name="admin")
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


class CreateEventStates(StatesGroup):
    """Состояния для создания события"""
    title = State()
    description = State()
    start_time = State()
    duration = State()
    price = State()
    max_viewers = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Админ-панель"""
    text = (
        "👨‍💼 <b>Панель администратора</b>\n\n"
        "Выберите действие:"
    )
    
    await message.answer(text, reply_markup=admin_menu_keyboard())


@router.callback_query(F.data == "admin_events_list")
async def admin_events_list(callback: CallbackQuery, db_session: AsyncSession):
    """Список всех событий для админа"""
    event_service = EventService(db_session)
    events = await event_service.get_all_events()
    
    if not events:
        text = "📋 <b>Список событий</b>\n\nСобытий пока нет."
    else:
        text = f"📋 <b>Список событий</b>\n\nВсего: {len(events)}\n\n"
        
        for event in events[:10]:  # Показываем первые 10
            status_emoji = {
                "upcoming": "🔜",
                "live": "🔴",
                "finished": "✅",
                "cancelled": "❌"
            }.get(event.status.value, "❓")
            
            text += (
                f"{status_emoji} <b>{event.title}</b>\n"
                f"   ID: {event.id} | {event.start_time.strftime('%d.%m.%Y %H:%M')}\n"
                f"   Цена: {event.price} ₽\n\n"
            )
    
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "admin_create_event")
async def start_create_event(callback: CallbackQuery, state: FSMContext):
    """Начать создание события"""
    await state.set_state(CreateEventStates.title)
    
    text = (
        "➕ <b>Создание нового события</b>\n\n"
        "Шаг 1/6: Введите название спектакля:"
    )
    
    await callback.message.edit_text(text)
    await callback.answer()


@router.message(CreateEventStates.title)
async def process_event_title(message: Message, state: FSMContext):
    """Обработка названия события"""
    await state.update_data(title=message.text)
    await state.set_state(CreateEventStates.description)
    
    await message.answer(
        "Шаг 2/6: Введите описание спектакля\n"
        "(или отправьте '-' чтобы пропустить):"
    )


@router.message(CreateEventStates.description)
async def process_event_description(message: Message, state: FSMContext):
    """Обработка описания события"""
    description = None if message.text == "-" else message.text
    await state.update_data(description=description)
    await state.set_state(CreateEventStates.start_time)
    
    await message.answer(
        "Шаг 3/6: Введите дату и время начала\n"
        "Формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
        "Например: 25.12.2024 19:00"
    )


@router.message(CreateEventStates.start_time)
async def process_event_start_time(message: Message, state: FSMContext):
    """Обработка времени начала"""
    try:
        start_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(start_time=start_time)
        await state.set_state(CreateEventStates.duration)
        
        await message.answer(
            "Шаг 4/6: Введите длительность в минутах\n"
            "(по умолчанию 120):"
        )
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты!\n"
            "Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ\n"
            "Например: 25.12.2024 19:00"
        )


@router.message(CreateEventStates.duration)
async def process_event_duration(message: Message, state: FSMContext):
    """Обработка длительности"""
    try:
        duration = int(message.text) if message.text != "-" else 120
        await state.update_data(duration_minutes=duration)
        await state.set_state(CreateEventStates.price)
        
        await message.answer(
            "Шаг 5/6: Введите цену билета в рублях\n"
            "(0 для бесплатного):"
        )
    except ValueError:
        await message.answer("❌ Введите число!")


@router.message(CreateEventStates.price)
async def process_event_price(message: Message, state: FSMContext):
    """Обработка цены"""
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await state.set_state(CreateEventStates.max_viewers)
        
        await message.answer(
            "Шаг 6/6: Введите максимальное количество зрителей\n"
            "(или '-' для неограниченного):"
        )
    except ValueError:
        await message.answer("❌ Введите число!")


@router.message(CreateEventStates.max_viewers)
async def process_event_max_viewers(message: Message, state: FSMContext, db_session: AsyncSession):
    """Обработка максимального количества зрителей и создание события"""
    try:
        max_viewers = None if message.text == "-" else int(message.text)
        data = await state.get_data()
        
        # Создаем событие
        event_service = EventService(db_session)
        event = await event_service.create_event(
            title=data["title"],
            description=data.get("description"),
            start_time=data["start_time"],
            duration_minutes=data["duration_minutes"],
            price=data["price"],
            max_viewers=max_viewers
        )
        
        await state.clear()
        
        text = (
            "✅ <b>Событие успешно создано!</b>\n\n"
            f"🎭 {event.title}\n"
            f"📅 {event.start_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"⏱ {event.duration_minutes} мин\n"
            f"💰 {event.price} ₽\n"
            f"ID: {event.id}"
        )
        
        await message.answer(text, reply_markup=admin_menu_keyboard())
        logger.info(f"Создано событие {event.id}: {event.title}")
        
    except ValueError:
        await message.answer("❌ Введите число или '-'!")


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery, db_session: AsyncSession):
    """Статистика"""
    # TODO: Реализовать подсчет статистики
    
    text = (
        "📊 <b>Статистика</b>\n\n"
        "Пользователей: -\n"
        "Событий: -\n"
        "Продано билетов: -\n"
        "Выручка: - ₽\n\n"
        "⚠️ Функция в разработке"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "admin_ai_content")
async def admin_ai_content(callback: CallbackQuery):
    """ИИ-контент"""
    text = (
        "🤖 <b>ИИ-генерация контента</b>\n\n"
        "⚠️ Функция в разработке\n\n"
        "Планируется:\n"
        "• Генерация анонсов спектаклей\n"
        "• Создание афиш\n"
        "• Автопостинг в канал"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()
