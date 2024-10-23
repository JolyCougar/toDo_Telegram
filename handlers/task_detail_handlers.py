import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local

WAITING_FOR_TASK_ID = range(1)


async def detail_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> None:
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
            task_details = (f'Задача: {task.get('name')}\n'
                            f'Описание: {task.get('description')}\n'
                            f'Добавлена: {task.get("create_at")[:10]}\n'
                            f'Состояние: {task_status}\n')
            await update.message.reply_text(task_details)
        else:
            await update.message.reply_text("Нет такой задачи.")
    else:
        await update.message.reply_text("Ошибка при получении задачи. Попробуйте позже.")

