import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token, Session_local
from config import DJANGO_API_URL

WAITING_FOR_TASK_DESCRIPTION = range(2)


async def handle_task_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_title = update.message.text  # Получаем название задачи от пользователя
    context.user_data['task_title'] = task_title  # Сохраняем название задачи в контексте

    await update.message.reply_text("Пожалуйста, введите описание задачи:")  # Запрашиваем описание задачи
    context.user_data['state'] = WAITING_FOR_TASK_DESCRIPTION  # Устанавливаем следующее состояние
    return WAITING_FOR_TASK_DESCRIPTION


async def handle_task_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_description = update.message.text
    task_title = context.user_data.get('task_title')  # Получаем название задачи

    # Отправляем данные на ваш Django API
    user_id = update.message.from_user.id
    session = Session_local()
    token = get_token(user_id, session)

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return

    headers = {
        'Authorization': f'Token {token}'
    }

    # Создаем задачу
    task_data = {
        'name': task_title,
        'description': task_description
    }

    response = requests.post(f"{DJANGO_API_URL}tasks/create/", json=task_data, headers=headers)

    if response.status_code == 201:  # Успешное создание задачи
        await update.message.reply_text("Задача успешно добавлена!")
    else:
        await update.message.reply_text("Ошибка при добавлении задачи. Проверьте данные и попробуйте снова.")

    # Сброс состояния
    context.user_data.clear()
    return ConversationHandler.END
