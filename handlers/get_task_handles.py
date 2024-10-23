import requests
from telegram import Update
from telegram.ext import ContextTypes
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session as SessionLocal


async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    session: Session = SessionLocal()
    token = get_token(user_id, session)  # Получаем токен из базы данных

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return

    headers = {
        'Authorization': f'Token {token}'  # Указываем токен в заголовках
    }

    response = requests.get(f"{DJANGO_API_URL}tasks/", headers=headers)

    if response.status_code == 200:
        tasks = response.json()
        if tasks:
            tasks_list = "\n".join(
                [f"Задача {task['id']} :  {task['name']}: Описание {task['description']}"
                 for task in tasks
                 if not task['complete']
                 ])

            await update.message.reply_text(f"Ваши задачи:\n{tasks_list}")
        else:
            await update.message.reply_text("У вас нет задач.")
    else:
        await update.message.reply_text("Ошибка при получении задач. Попробуйте позже.")
