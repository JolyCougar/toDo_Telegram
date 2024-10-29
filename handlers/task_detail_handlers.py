import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local
from .start_handler import send_main_keyboard, set_commands

WAITING_FOR_TASK_ID = range(1)


async def detail_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> None:
    """ Получения детализированной информации о задаче с сервера """

    user_id = update.message.from_user.id
    session: Session = Session_local()
    token = get_token(user_id, session)  # Получаем токен из базы данных

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return

    headers = {
        'Authorization': f'Token {token}'  # Указываем токен в заголовках
    }

    response = requests.get(f"{DJANGO_API_URL}tasks/{task_id}/", headers=headers)

    if response.status_code == 200:
        task = response.json()
        if task:
            task_status = "Не выполнена"
            if task.get("complete"):
                task_status = "Выполнена"
            task_details = (f'Задача ID {task.get('id')}: {task.get('name')}\n'
                            f'Описание: {task.get('description')}\n'
                            f'Добавлена: {task.get("create_at")[:10]}\n'
                            f'Состояние: {task_status}\n')
            await update.message.reply_text(task_details)
        else:
            await update.message.reply_text("Нет такой задачи.")
    else:
        await update.message.reply_text("Ошибка при получении задачи. Попробуйте позже.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode=False)
    await set_commands(context)
    return ConversationHandler.END
