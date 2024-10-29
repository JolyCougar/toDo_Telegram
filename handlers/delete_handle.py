import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local, delete_task_local, get_local_mode
from .start_handler import send_main_keyboard, set_commands

DELETE_TASK = range(5)


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> None:
    """ Удаление задачи в зависимости от флага local_mode
        либо с сервера либо из локальной БД """

    user_id = update.message.from_user.id
    session: Session = Session_local()
    token = get_token(user_id, session)
    local_mode = get_local_mode(user_id, session)

    if not token and local_mode:
        if delete_task_local(int(task_id), user_id, session):
            await update.message.reply_text(f"Задача номер {task_id} успешно удалена.")
            await update.message.reply_text("Вы не авторизованы. Бот работает в локальном режиме.")
        else:
            await update.message.reply_text("Неверно указан ID задачи")
    elif token:
        headers = {
            'Authorization': f'Token {token}'
        }

        response = requests.delete(f"{DJANGO_API_URL}tasks/{task_id}/delete/", headers=headers)

        if response.status_code == 204:
            await update.message.reply_text(f"Задача ID {task_id} успешно удалена")

        else:
            await update.message.reply_text("Ошибка при удалении задачи. Попробуйте позже.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode)
    await set_commands(context)
    return ConversationHandler.END
