import requests
from telegram import Update
from telegram.ext import ContextTypes
from services.db import save_token
from config import DJANGO_API_URL


async def request_login_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите ваше имя пользователя и пароль в формате: username:password")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    if message == "Авторизоваться":
        await request_login_format(update, context)
    elif ':' in message:
        username, password = message.split(':', 1)
        response = requests.post(DJANGO_API_URL+'login/',
                                 data={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            user_id = update.message.from_user.id

            # Сохраняем токен в базе данных
            save_token(user_id, token)
            await update.message.reply_text("Вы успешно авторизованы!")
        else:
            await update.message.reply_text("Ошибка авторизации. Проверьте имя пользователя и пароль.")
    else:
        await update.message.reply_text("Неверный формат. Используйте: username:password.")


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await request_login_format(update, context)