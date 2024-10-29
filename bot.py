from config import API_TOKEN
from handlers.start_handler import start
from utils.logging_config import setup_logging, error_handler
from handlers.create_new_task_handle import handle_task_title, handle_task_description
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, filters,
                          ConversationHandler)
from handlers.messages_handle import (handle_message, handle_state,
                                      WAITING_FOR_TASK_ID, CONFIRMING_TASK,
                                      WAITING_FOR_TASK_TITLE, WAITING_FOR_TASK_DESCRIPTION,
                                      DELETE_TASK, WAITING_FOR_LOGIN)


def main() -> None:
    """ Главная функция, регистрирует handlers и запускает бота """

    setup_logging()  # Настройка логирования
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Настройка ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            WAITING_FOR_TASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_state)],
            CONFIRMING_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_state)],
            WAITING_FOR_TASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_title)],
            WAITING_FOR_TASK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_description)],
            DELETE_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_state)],
            WAITING_FOR_LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_state)],
        },
        fallbacks=[],
    )

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)  # Регистрация ConversationHandler

    application.add_error_handler(error_handler)

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
