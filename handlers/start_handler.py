from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from services.db import get_token, Session_local


def get_main_keyboard(is_authorized: bool) -> ReplyKeyboardMarkup:
    if is_authorized:
        keyboard = [
            ["Добавить новую задачу"],
            ["Подтвердить задачу"],
            ["Получить невыполненные задачи"],
            ["Получить выполненные задачи"],
            ["Получить все задачи"],
            ["Детали задачи"],
            ["Удалить задачу"],
            ["Выйти"]
        ]
    else:
        keyboard = [
            ["Авторизоваться"]
        ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    session = Session_local()
    token = get_token(user_id, session)  # Получаем токен из базы данных
    is_authorized = token is not None

    reply_markup = get_main_keyboard(is_authorized)
    await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)


async def send_main_keyboard(update: Update, is_authorized: bool) -> None:
    reply_markup = get_main_keyboard(is_authorized)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)