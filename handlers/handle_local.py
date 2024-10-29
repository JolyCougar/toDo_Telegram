from telegram.ext import ContextTypes
from telegram import Update
from services.db import Session_local, set_local_mode
from .start_handler import send_main_keyboard, set_commands


async def handle_local_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Установка режима работы с локальной БД """

    user_id = update.message.from_user.id
    session = Session_local()

    set_local_mode(user_id, True, session)  # Устанавливаем local_mode в True
    await update.message.reply_text("Вы перешли в локальный режим. Теперь все действия будут выполняться локально.")
    await send_main_keyboard(update, False, True)
    await set_commands(context)
