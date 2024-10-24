import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local
from .start_handler import send_main_keyboard

CONFIRMING_TASK = range(2)


async def confirm_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> None:
    user_id = update.message.from_user.id
    session: Session = Session_local()
    token = get_token(user_id, session)  # Получаем токен из базы данных

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return

    headers = {
        'Authorization': f'Token {token}'  # Указываем токен в заголовках
    }

    # Отправляем запрос на подтверждение задачи
    response = requests.patch(f"{DJANGO_API_URL}tasks/{task_id}/confirm/", headers=headers)
    if response.status_code == 200:
        await update.message.reply_text(f"Задача с ID {task_id} успешно подтверждена!")
    else:
        await update.message.reply_text("Ошибка при подтверждении задачи. Проверьте ID задачи или статус задачи.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized)

    return ConversationHandler.END  # Завершаем разговор
