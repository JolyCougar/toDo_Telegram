from telegram import Update
from telegram.ext import ContextTypes


async def request_login_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите ваше имя пользователя и пароль в формате: username:password")


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await request_login_format(update, context)
