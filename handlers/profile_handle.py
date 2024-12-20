import httpx
from telegram import Update
from telegram.ext import ContextTypes
from services.db import get_token
from config import DJANGO_API_URL
from sqlalchemy.orm import Session
from services.db import Session_local
from .start_handler import send_main_keyboard, set_commands


async def profile_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Получение информации о пользователе, зарегистрированном на сайте """

    user_id = update.message.from_user.id
    session: Session = Session_local()
    token = get_token(user_id, session)

    if not token:
        await update.message.reply_text("Вы не авторизованы. Пожалуйста, авторизуйтесь.")
        return

    headers = {
        'Authorization': f'Token {token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}profile/", headers=headers)

    if response.status_code == 200:
        profile = response.json()
        if profile:
            profile_details = (f' Имя: {profile["user"].get('first_name')}\n'
                               f'Фамилия: {profile["user"].get('last_name')}\n'
                               f'E-mail: {profile["user"].get('email')}\n'
                               f'О себе: {profile["profile"].get('bio')}\n')
            await update.message.reply_text(profile_details)
        else:
            await update.message.reply_text("Ошибка при получении информации.")
    else:
        await update.message.reply_text("Ошибка при получении профиля. Попробуйте позже.")

    is_authorized = token is not None
    await send_main_keyboard(update, is_authorized, local_mode=False)
    await set_commands(context)
