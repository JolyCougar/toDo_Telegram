import requests
from telegram import Update
from telegram.ext import ContextTypes
from services.db import get_token, get_tasks_from_local
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local, get_local_mode
from .start_handler import send_main_keyboard


async def get_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, complete: str) -> None:
    user_id = update.message.from_user.id
    session: Session = Session_local()
    local_mode = get_local_mode(user_id, session)
    status_task = {True: "Выполнено", False: "Не выполнено"}
    token = get_token(user_id, session)  # Получаем токен из базы данных

    if not token and local_mode:
        await update.message.reply_text("Вы не авторизованы. Бот работает в локальном режиме.")
        task_list = get_tasks_from_local(user_id, session, complete)
        text = "".join(
                    [f"Задача ID {task.id} :  {task.title} : {task.description}\n"
                     f"Состояние: {status_task[task.is_completed]}"
                     for task in task_list
                     ])
        await update.message.reply_text(f"Ваши задачи:\n{text}")

    elif token:
        headers = {
            'Authorization': f'Token {token}'  # Указываем токен в заголовках
        }

        response = requests.get(f"{DJANGO_API_URL}tasks/?complete={complete}", headers=headers)

        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                tasks_list = "\n".join(
                    [f"Задача ID {task['id']} :  {task['name']} : {task['description']}\n"
                     f"Состояние: {status_task[task['complete']]}"
                     for task in tasks
                     ])

                await update.message.reply_text(f"Ваши задачи:\n{tasks_list}")
            else:
                await update.message.reply_text("У вас нет задач.")
        else:
            await update.message.reply_text("Ошибка при получении задач. Попробуйте позже.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode)
