from telegram.ext import ContextTypes
from services.db import save_token
from config import DJANGO_API_URL
from .login_handles import request_login_format
from .get_task_handles import get_tasks
from telegram import Update, ReplyKeyboardMarkup
import requests


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    if message == "Авторизоваться":
        await request_login_format(update, context)
    elif message == "Получить невыполненные задачи":  # Обработка нажатия кнопки "Получить задачи"
        await get_tasks(update, context)
    elif ':' in message:
        username, password = message.split(':', 1)
        response = requests.post(DJANGO_API_URL + 'login/',
                                 data={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            user_id = update.message.from_user.id

            # Сохраняем токен в базе данных
            save_token(user_id, token)
            await update.message.reply_text("Вы успешно авторизованы!")

            # Обновляем клавиатуру, убирая кнопку "Авторизоваться"
            await update.message.reply_text("Добро пожаловать!",
                                            reply_markup=ReplyKeyboardMarkup([],
                                                                             one_time_keyboard=True))
        else:
            await update.message.reply_text("Ошибка авторизации. Проверьте имя пользователя и пароль.")
    else:
        await update.message.reply_text("Неверный формат. Используйте: username:password.")
