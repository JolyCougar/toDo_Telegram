from telegram.ext import ContextTypes
from telegram import Update
from services.db import Session_local, set_local_mode
from .start_handler import send_main_keyboard

local_mode = False


async def handle_local_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    session = Session_local()

    # Устанавливаем local_mode в True
    set_local_mode(user_id, True, session)
    await update.message.reply_text("Вы перешли в локальный режим. Теперь все действия будут выполняться локально.")
