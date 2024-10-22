import requests
from telegram import Update
from telegram.ext import ContextTypes


async def request_login_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите ваше имя пользователя и пароль в формате: username:password")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    if message == "Авторизоваться":
        await request_login_format(update, context)
    elif ':' in message:
        username, password = message.split(':', 1)
        response = requests.post('http://127.0.0.1:8000/api/v1/login/',
                                 data={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            print(response.json())
            await update.message.reply_text(f"Вы успешно авторизованы! Ваш токен: {token}")
        else:
            await update.message.reply_text("Ошибка авторизации. Проверьте имя пользователя и пароль.")
    else:
        await update.message.reply_text("Неверный формат. Используйте: username:password.")


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await request_login_format(update, context)
