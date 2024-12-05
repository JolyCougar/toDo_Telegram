import httpx
from config import DJANGO_API_URL
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from services.db import save_token, get_token, Session_local
from handlers.start_handler import send_main_keyboard, set_commands
from services.db import set_local_mode
from .start_handler import start

WAITING_FOR_LOGIN = range(6)


async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str, password: str) -> None:
    """ Обработка логики авторизации """
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DJANGO_API_URL}login/", data={'username': username, 'password': password})

    if response.status_code == 200:
        token = response.json().get('token')
        # Сохраняем токен в базе данных
        user_id = update.message.from_user.id
        session = Session_local()
        save_token(user_id, token)
        set_local_mode(user_id, False, session)
        await update.message.reply_text("Вы успешно авторизованы!")

        await start(update, context)  # Перезапускаем стартовое меню

    else:
        await update.message.reply_text("Ошибка авторизации. Проверьте имя пользователя и пароль.")
    return ConversationHandler.END


async def handle_login_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обработка ввода логина и пароля """

    message = update.message.text

    if ':' in message:
        username, password = message.split(':', 1)
        await handle_login(update, context, username, password)
    else:
        await update.message.reply_text("Неверный формат. Пожалуйста, "
                                        "введите имя пользователя и пароль в формате: username:password")


async def logout(update: Update, user_id: int) -> None:
    """ Логика logout """

    # Получаем токен из базы данных
    session = Session_local()
    token = get_token(user_id, session)

    # Удаляем токен из базы данных
    save_token(user_id, None)

    # Отправляем запрос на сервер о выходе
    headers = {
        'Authorization': f'Token {token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DJANGO_API_URL}logout/", headers=headers, json={'user_id': user_id})

    if response.status_code == 200:
        await update.message.reply_text("Вы вышли из системы.")
    else:
        await update.message.reply_text("Ошибка при выходе из системы. Попробуйте позже.")

    await send_main_keyboard(update, is_authorized=False, local_mode=False)  # Обновляем клавиатуру
