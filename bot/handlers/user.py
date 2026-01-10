"""
Обработчики для обычных пользователей
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from loguru import logger

from database.models import User
from bot.keyboards.inline import main_menu_keyboard, back_to_main_keyboard

router = Router(name="user")


@router.message(CommandStart())
async def cmd_start(message: Message, db_user: User):
    """
    Обработчик команды /start
    
    Args:
        message: Сообщение от пользователя
        db_user: Пользователь из БД (из middleware)
    """
    welcome_text = (
        f"🎭 <b>Добро пожаловать, {db_user.first_name}!</b>\n\n"
        "Это бот для просмотра онлайн-спектаклей.\n\n"
        "Здесь вы можете:\n"
        "• Смотреть афишу предстоящих спектаклей\n"
        "• Покупать билеты на трансляции\n"
        "• Смотреть спектакли онлайн\n\n"
        "Выберите действие:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard()
    )
    
    logger.info(f"Пользователь {db_user.telegram_id} запустил бота")


@router.message(Command("menu"))
@router.callback_query(F.data == "main_menu")
async def show_main_menu(event: Message | CallbackQuery, db_user: User):
    """Показать главное меню"""
    menu_text = (
        "🎭 <b>Главное меню</b>\n\n"
        "Выберите действие:"
    )
    
    if isinstance(event, Message):
        await event.answer(menu_text, reply_markup=main_menu_keyboard())
    else:
        await event.message.edit_text(menu_text, reply_markup=main_menu_keyboard())
        await event.answer()


@router.callback_query(F.data == "my_tickets")
async def show_my_tickets(callback: CallbackQuery, db_user: User):
    """Показать билеты пользователя"""
    # TODO: Реализовать получение билетов из БД
    
    text = (
        "🎫 <b>Мои билеты</b>\n\n"
        "У вас пока нет купленных билетов.\n"
        "Посмотрите афишу и выберите интересующий спектакль!"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    """Информация о проекте"""
    about_text = (
        "ℹ️ <b>О проекте</b>\n\n"
        "🎭 Платформа для онлайн-спектаклей\n\n"
        "Мы предоставляем возможность смотреть качественные театральные "
        "постановки не выходя из дома.\n\n"
        "Все трансляции проходят в высоком качестве с возможностью "
        "интерактивного взаимодействия.\n\n"
        "По вопросам сотрудничества: @support"
    )
    
    await callback.message.edit_text(
        about_text,
        reply_markup=back_to_main_keyboard()
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Помощь"""
    help_text = (
        "📖 <b>Помощь</b>\n\n"
        "<b>Доступные команды:</b>\n"
        "/start - Запустить бота\n"
        "/menu - Главное меню\n"
        "/events - Афиша спектаклей\n"
        "/tickets - Мои билеты\n"
        "/help - Эта справка\n\n"
        "Если у вас возникли вопросы, обратитесь в поддержку: @support"
    )
    
    await message.answer(help_text)
