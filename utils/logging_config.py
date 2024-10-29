import logging


def setup_logging():
    """ Обработка логов бота """

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def error_handler(update, context):
    """Обработчик ошибок."""

    print(f'Произошла ошибка: {context.error}')
