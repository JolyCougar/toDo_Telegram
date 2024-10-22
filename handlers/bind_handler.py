import logging
import requests
from telegram import Update
from telegram.ext import ContextTypes
from config import DJANGO_API_URL


async def bind_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.user_data.get('bind_user_id')

    if user_id is not None:
        telegram_user_id = update.message.from_user.id
        telegram_username = update.message.from_user.username

        # Получаем CSRF-токен
        try:
            csrf_response = requests.get('http://127.0.0.1:8000/csrf-token/')  # Замените на ваш URL
            csrf_response.raise_for_status()
            csrf_token = csrf_response.json().get('csrfToken')
        except requests.exceptions.RequestException as e:
            error_message = f"Ошибка при получении CSRF-токена: {str(e)}"
            await update.message.reply_text(error_message)
            return

        # Отправка POST-запроса на Django API с CSRF-токеном
        try:
            response = requests.post(DJANGO_API_URL, data={
                'user_id': user_id,
                'telegram_id': telegram_user_id,
                'telegram_username': telegram_username,
            }, headers={
                'X-CSRFToken': csrf_token  # Добавляем CSRF-токен в заголовок
            }, cookies={'csrftoken': csrf_token})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            error_message = f"Ошибка при обращении к серверу: {str(e)}"
            await update.message.reply_text(error_message)
            return

        # Логирование ответа
        logging.info(f"Response from Django API: {response.text}")

        # Попытка разобрать ответ как JSON
        try:
            data = response.json()
        except ValueError:
            error_message = f"Ошибка при разборе ответа: {response.text}"
            await update.message.reply_text(error_message)
            return

        # Обработка ответа
        if 'status' in data and data['status'] == 'success':
            await update.message.reply_text("Ваш аккаунт успешно привязан!")
        else:
            await update.message.reply_text("Не удалось привязать аккаунт. Попробуйте еще раз.")
    else:
        await update.message.reply_text("Не удалось найти ID пользователя для привязки.")
