import requests
from telegram import Update
from config import DJANGO_API_URL
from telegram.ext import ContextTypes
from services.db import Session_local, get_token, get_tasks_from_local, delete_task_local
from .start_handler import send_main_keyboard, set_commands


async def sync_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Функция синхроназации задач, отправляет локальные
    задачи на сервер и удаляет из локальной БД """

    user_id = update.message.from_user.id
    session = Session_local()
    token = get_token(user_id, session)
    user_tasks = get_tasks_from_local(user_id, session)

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return
    else:
        headers = {
            'Authorization': f'Token {token}'
        }

        # Подготовка данных для отправки
        for task in user_tasks:
            task_data = {
                'name': task.title,
                'description': task.description,
                'complete': task.is_completed
            }
            # Отправка задач на сервер
            response = requests.post(f"{DJANGO_API_URL}tasks/create/",
                                     json=task_data,
                                     headers=headers
                                     )

        if response.status_code == 201:  # Успешное создание задач
            await update.message.reply_text("Начинается удаление локальных задач!")
            for task in user_tasks:
                delete_task_local(task.id, session)
        else:
            await update.message.reply_text(f"Ошибка при добавлении задач: {response.status_code}")

        # Сброс состояния
        context.user_data.clear()

    is_authorized = token is not None
    await update.message.reply_text("Ваши задачи успешно синхронизированны")
    await send_main_keyboard(update, is_authorized, local_mode=False)
    await set_commands(context)
