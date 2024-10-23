import requests
from config import DJANGO_API_URL
from telegram import Update
from telegram.ext import ContextTypes
from services.db import save_token, get_token, Session_local
from handlers.start_handler import start


async def request_login_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите ваше имя пользователя и пароль в формате: username:password")


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await request_login_format(update, context)


async def logout(update: Update, user_id: int) -> None:
    # Получаем токен из базы данных
    session = Session_local()
    token = get_token(user_id, session)

    # Удаляем токен из базы данных
    save_token(user_id, None)

    # Отправляем запрос на сервер о выходе
    headers = {
        'Authorization': f'Token {token}'  # Указываем токен в заголовках
    }
    response = requests.post(f"{DJANGO_API_URL}logout/", headers=headers, json={'user_id': user_id})

    if response.status_code == 200:
        await update.message.reply_text("Вы вышли из системы.")
    else:
        await update.message.reply_text("Ошибка при выходе из системы. Попробуйте позже.")

    await start(update, None)  # Обновляем клавиатуру
