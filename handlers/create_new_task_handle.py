import httpx
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token, Session_local, get_local_mode, add_task
from config import DJANGO_API_URL
from .start_handler import send_main_keyboard, set_commands

WAITING_FOR_TASK_DESCRIPTION = range(2)


async def handle_task_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Получение от пользователя название задачи """

    task_title = update.message.text  # Получаем название задачи от пользователя
    context.user_data['task_title'] = task_title  # Сохраняем название задачи в контексте

    await update.message.reply_text("Пожалуйста, введите описание задачи:")  # Запрашиваем описание задачи
    context.user_data['state'] = WAITING_FOR_TASK_DESCRIPTION  # Устанавливаем следующее состояние
    return WAITING_FOR_TASK_DESCRIPTION


async def handle_task_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Получение описания задачи пользователя
    и добавление ее в локальную бд или на сервер """

    task_description = update.message.text
    task_title = context.user_data.get('task_title')  # Получаем название задачи
    user_id = update.message.from_user.id
    session = Session_local()
    local_mode = get_local_mode(user_id, session)
    token = get_token(user_id, session)

    if not token and local_mode:
        add_task(user_id, task_title, task_description, session)
        await update.message.reply_text("Задача успешно добавлена в локальную базу данных!")
        await update.message.reply_text("Вы не авторизованы. Бот работает в локальном режиме.")

    elif token:
        headers = {
            'Authorization': f'Token {token}'
        }

        # Создаем задачу
        task_data = {
            'name': task_title,
            'description': task_description
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{DJANGO_API_URL}tasks/create/", json=task_data, headers=headers)

        if response.status_code == 201:
            await update.message.reply_text("Задача успешно добавлена!")
        else:
            await update.message.reply_text("Ошибка при добавлении задачи. Проверьте данные и попробуйте снова.")

        context.user_data.clear()
    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode)
    await set_commands(context)
    return ConversationHandler.END
