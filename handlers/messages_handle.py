from telegram import Update
from .get_task_handles import get_tasks
from .task_detail_handlers import detail_tasks
from .confirm_task_handle import confirm_tasks
from .profile_handle import profile_detail
from .delete_handle import delete_task
from .sync_task_handler import sync_task
from .handle_local import handle_local_mode
from telegram.ext import ContextTypes, ConversationHandler
from .login_handles import logout, handle_login_input
from .create_new_task_handle import handle_task_title, handle_task_description

""" Состояния бота """
WAITING_FOR_TASK_TITLE = range(1)  # Состояние ожидания названия задачи
WAITING_FOR_TASK_DESCRIPTION = range(2)  # Состояние ожидания описания задачи
WAITING_FOR_TASK_ID = range(3)  # Состояние ожидания ID задачи
CONFIRMING_TASK = range(4)  # Состояние подтверждения задачи
DELETE_TASK = range(5)  # Состояние ожидания ID задачи для удаления
WAITING_FOR_LOGIN = range(6)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Обработка команд бота вызванные с клавиатуры """

    message = update.message.text
    user_id = update.message.from_user.id

    if message == "Авторизоваться":
        await update.message.reply_text("Пожалуйста, введите имя пользователя и пароль в формате: username:password")
        context.user_data['state'] = WAITING_FOR_LOGIN
        return WAITING_FOR_LOGIN
    if message == "Без авторизации":
        await handle_local_mode(update, context)
    elif message == "Выйти":
        await logout(update, user_id)
    elif message == "Получить невыполненные задачи":
        await get_tasks(update, context, complete='False')  # Передаем аргумент для невыполненных задач
    elif message == "Получить выполненные задачи":
        await get_tasks(update, context, complete='True')  # Передаем аргумент для выполненных задач
    elif message == "Получить все задачи":
        await get_tasks(update, context, complete='')  # Передаем пустую строку для всех задач
    elif message == "Детали задачи":
        await update.message.reply_text("Пожалуйста, введите ID задачи:")
        context.user_data['state'] = WAITING_FOR_TASK_ID
        return WAITING_FOR_TASK_ID  # Переход к состоянию ожидания ID задачи
    elif message == "Подтвердить задачу":
        await update.message.reply_text("Пожалуйста, введите ID задачи для подтверждения:")
        context.user_data['state'] = CONFIRMING_TASK
        return CONFIRMING_TASK  # Переход к состоянию подтверждения задачи
    elif message == "Удалить задачу":
        await update.message.reply_text("Пожалуйста, введите ID задачи для удаления:")
        context.user_data['state'] = DELETE_TASK
        return DELETE_TASK  # Переход к состоянию удаления задачи
    elif message == "Посмотреть мой профиль":
        await profile_detail(update, context)
    elif message == "Добавить новую задачу":
        await update.message.reply_text("Пожалуйста, введите название задачи:")
        context.user_data['state'] = WAITING_FOR_TASK_TITLE
        return WAITING_FOR_TASK_TITLE
    elif message == "Синхронизировать задачи":
        await update.message.reply_text("Начинается синхронизация. Пожалуйста подождите. "
                                        "После выполнения синхронизации, ваши локальные задачи удалятся и "
                                        "будут доступны только на вашем аккаунте")
        await sync_task(update, context)


async def handle_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Внедрение состояния в context """

    state = context.user_data.get('state')
    task_id = update.message.text

    if state == WAITING_FOR_TASK_TITLE:
        await handle_task_title(update, context)
    elif state == WAITING_FOR_TASK_DESCRIPTION:
        await handle_task_description(update, context)
    elif state == WAITING_FOR_TASK_ID:
        await detail_tasks(update, context, task_id)
    elif state == CONFIRMING_TASK:
        await confirm_tasks(update, context, task_id)
    elif state == DELETE_TASK:
        await delete_task(update, context, task_id)
    elif state == WAITING_FOR_LOGIN:
        await handle_login_input(update, context)

    else:
        await update.message.reply_text("Неизвестное состояние. Пожалуйста, начните заново.")

    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Если у вас возникли проблемы то отправьте команду /start "
                                    "её также можно отправить с помощью меню. \n"
                                    "Если у вас возникли какие то сложности, пожалуйста свяжитесь с Администрацией\n"
                                    "Этот бот создан для улучшения пользовательского опыта при взаимодействии с"
                                    "приложением toDo app.\n\n Спасибо что используете наш сервис!❤️  ")
