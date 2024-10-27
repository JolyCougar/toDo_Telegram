from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, filters,
                          ConversationHandler)
from config import API_TOKEN
from handlers.start_handler import start
from utils.logging_config import setup_logging
from handlers.login_handles import login_command
from handlers.create_new_task_handle import handle_task_title, handle_task_description
from handlers.messages_handle import (handle_message, handle_task_id,
                                      WAITING_FOR_TASK_ID, CONFIRMING_TASK,
                                      WAITING_FOR_TASK_TITLE, WAITING_FOR_TASK_DESCRIPTION,
                                      DELETE_TASK)


async def error_handler(update, context):
    """Обработчик ошибок."""
    print(f'Произошла ошибка: {context.error}')

def main() -> None:
    setup_logging()  # Настройка логирования
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Настройка ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            WAITING_FOR_TASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_id)],
            CONFIRMING_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_id)],
            WAITING_FOR_TASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_title)],
            WAITING_FOR_TASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_description)],
            DELETE_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_id)],
        },
        fallbacks=[],
    )

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", login_command))  # Обработчик для команды логина
    application.add_handler(conv_handler)  # Регистрация ConversationHandler

    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
