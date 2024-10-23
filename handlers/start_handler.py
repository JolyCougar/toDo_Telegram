from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Авторизоваться"],
        ["Получить невыполненные задачи"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("Добро пожаловать! Нажмите кнопку ниже, чтобы авторизоваться:",
                                    reply_markup=reply_markup)
