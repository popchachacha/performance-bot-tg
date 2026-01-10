"""
Inline клавиатуры
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List

from database.models import Event


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🎭 Афиша", callback_data="events_list")
    )
    builder.row(
        InlineKeyboardButton(text="🎫 Мои билеты", callback_data="my_tickets")
    )
    builder.row(
        InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")
    )
    
    return builder.as_markup()


def events_list_keyboard(events: List[Event]) -> InlineKeyboardMarkup:
    """Клавиатура со списком событий"""
    builder = InlineKeyboardBuilder()
    
    for event in events:
        builder.row(
            InlineKeyboardButton(
                text=f"🎭 {event.title}",
                callback_data=f"event_{event.id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")
    )
    
    return builder.as_markup()


def event_detail_keyboard(event_id: int, has_ticket: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура для детальной информации о событии"""
    builder = InlineKeyboardBuilder()
    
    if has_ticket:
        builder.row(
            InlineKeyboardButton(
                text="▶️ Смотреть трансляцию",
                callback_data=f"watch_{event_id}"
            )
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="🎫 Купить билет",
                callback_data=f"buy_{event_id}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(text="◀️ Назад к афише", callback_data="events_list")
    )
    
    return builder.as_markup()


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню администратора"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="➕ Создать событие", callback_data="admin_create_event")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Список событий", callback_data="admin_events_list")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")
    )
    builder.row(
        InlineKeyboardButton(text="🤖 ИИ-контент", callback_data="admin_ai_content")
    )
    
    return builder.as_markup()


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")
    )
    return builder.as_markup()
