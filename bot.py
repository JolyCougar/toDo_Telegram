from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import API_TOKEN
from handlers.start_handler import start
from utils.logging_config import setup_logging
from handlers.login_handles import handle_message, login_command


def main() -> None:
    setup_logging()  # Настройка логирования
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("login", login_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
