from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from services.db import get_token, Session_local, get_local_mode


async def set_commands(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Команды кнопки меню """

    commands = [
        ("start", "Запустить бота"),
        ("login", "Войти в систему"),
    ]
    await context.bot.set_my_commands(commands)


def get_main_keyboard(is_authorized: bool, local_mode: bool) -> ReplyKeyboardMarkup:
    """ Основная клавиатура которая меняется в зависимости от авторизации пользователя """

    if is_authorized:
        keyboard = [
            ["Добавить новую задачу"],
            ["Подтвердить задачу"],
            ["Получить невыполненные задачи"],
            ["Получить выполненные задачи"],
            ["Получить все задачи"],
            ["Детали задачи"],
            ["Удалить задачу"],
            ["Посмотреть мой профиль"],
            ['Синхронизировать задачи'],
            ["Выйти"]
        ]
    elif local_mode:
        keyboard = [
            ["Добавить новую задачу"],
            ["Подтвердить задачу"],
            ["Получить невыполненные задачи"],
            ["Получить выполненные задачи"],
            ["Получить все задачи"],
            ["Удалить задачу"],
            ["Авторизоваться"]
        ]
    else:
        keyboard = [
            ["Авторизоваться"],
            ["Без авторизации"]
        ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обработка команды /start """

    user_id = update.message.from_user.id
    session = Session_local()
    await set_commands(context)
    token = get_token(user_id, session)  # Получаем токен из базы данных
    is_authorized = token is not None
    local_mode = get_local_mode(user_id, session)
    reply_markup = get_main_keyboard(is_authorized, local_mode)
    await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)


async def send_main_keyboard(update: Update, is_authorized: bool, local_mode) -> None:
    """ Обновление клавиатуры """

    reply_markup = get_main_keyboard(is_authorized, local_mode)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
