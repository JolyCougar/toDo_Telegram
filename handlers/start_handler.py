import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        command = context.args[0]
        if command.startswith('bind_'):
            user_id = command.split('_')[1]
            context.user_data['bind_user_id'] = user_id  # Сохраняем user_id в контексте
            print(user_id, '--user-id')

    keyboard = [[KeyboardButton("Привязать аккаунт")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я ваш Telegram-бот. Нажмите кнопку ниже, чтобы привязать ваш аккаунт:",
                                    reply_markup=reply_markup)
