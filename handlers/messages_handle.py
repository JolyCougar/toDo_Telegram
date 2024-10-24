from telegram.ext import ContextTypes, ConversationHandler
from services.db import save_token, get_token, Session_local
from config import DJANGO_API_URL
from .login_handles import request_login_format, logout
from .get_task_handles import get_tasks
from .task_detail_handlers import detail_tasks
from .confirm_task_handle import confirm_tasks
from .create_new_task_handle import handle_task_title, handle_task_description
from telegram import Update
from handlers.start_handler import start
import requests

WAITING_FOR_TASK_TITLE = range(1)  # Состояние ожидания названия задачи
WAITING_FOR_TASK_DESCRIPTION = range(2)  # Состояние ожидания описания задачи
WAITING_FOR_TASK_ID = range(3)  # Состояние ожидания ID задачи
CONFIRMING_TASK = range(4)  # Состояние подтверждения задачи


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user_id = update.message.from_user.id
    session = Session_local()
    token = get_token(user_id, session)  # Получаем токен из базы данных

    if message == "Авторизоваться":
        await request_login_format(update, context)
    elif message == "Выйти":
        await logout(update, user_id)  # Вызываем функцию выхода
    elif message == "Получить невыполненные задачи":
        await get_tasks(update, context, complete='?complete=false')  # Передаем аргумент для невыполненных задач
    elif message == "Получить выполненные задачи":
        await get_tasks(update, context, complete='?complete=true')  # Передаем аргумент для выполненных задач
    elif message == "Получить все задачи":
        await get_tasks(update, context, complete='')  # Передаем пустую строку для всех задач
    elif message == "Детали задачи":
        await update.message.reply_text("Пожалуйста, введите ID задачи:")
        context.user_data['state'] = WAITING_FOR_TASK_ID
        return WAITING_FOR_TASK_ID  # Переход к состоянию ожидания ID задачи
    elif message == "Подтвердить задачу":
        await update.message.reply_text("Пожалуйста, введите ID задачи для подтверждения:")
        context.user_data['state'] = CONFIRMING_TASK
        return CONFIRMING_TASK  # Переход к состоянию подтверждения задачи
    elif message == "Добавить новую задачу":
        await update.message.reply_text("Пожалуйста, введите название задачи:")
        context.user_data['state'] = WAITING_FOR_TASK_TITLE  # Устанавливаем состояние
        return WAITING_FOR_TASK_TITLE
    elif ':' in message:
        username, password = message.split(':', 1)
        response = requests.post(f"{DJANGO_API_URL}login/", data={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            # Сохраняем токен в базе данных
            save_token(user_id, token)
            await update.message.reply_text("Вы успешно авторизованы!")

            # Обновляем клавиатуру
            await start(update, context)  # Перезапускаем стартовое меню
        else:
            await update.message.reply_text("Ошибка авторизации. Проверьте имя пользователя и пароль.")
    else:
        await update.message.reply_text("Неверный формат. Используйте: username:password.")


async def handle_task_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get('state')
    task_id = update.message.text

    if state == WAITING_FOR_TASK_TITLE:
        await handle_task_title(update, context)
    elif state == WAITING_FOR_TASK_DESCRIPTION:
        await handle_task_description(update, context)
    elif state == WAITING_FOR_TASK_ID:
        await detail_tasks(update, context, task_id)
    elif state == CONFIRMING_TASK:
        await confirm_tasks(update, context, task_id)
    else:
        await update.message.reply_text("Неизвестное состояние. Пожалуйста, начните заново.")

    return ConversationHandler.END
