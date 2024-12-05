import httpx
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import get_token, Session_local, get_local_mode, complete_task
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from .start_handler import send_main_keyboard, set_commands

CONFIRMING_TASK = range(2)


async def confirm_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, task_id: str) -> None:
    """ Меняет статус задачи на выполнено,
        в зависимости от авторизации либо
        локально, либо на сервере """

    user_id = update.message.from_user.id
    session: Session = Session_local()
    token = get_token(user_id, session)
    local_mode = get_local_mode(user_id, session)

    if not token and local_mode:
        await update.message.reply_text("Вы не авторизованы. Бот работает в локальном режиме.")
        complete_task(int(task_id), session)
        await update.message.reply_text("Состояние задачи успешно обновлено.")
    elif token:
        headers = {
            'Authorization': f'Token {token}'
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{DJANGO_API_URL}tasks/{task_id}/confirm/", headers=headers)

        if response.status_code == 200:
            await update.message.reply_text(f"Задача с ID {task_id} успешно подтверждена!")
        else:
            await update.message.reply_text("Ошибка при подтверждении задачи. Проверьте ID задачи или статус задачи.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode)
    await set_commands(context)

    return ConversationHandler.END
