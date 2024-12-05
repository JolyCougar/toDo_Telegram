# ToDo app Telegram bot


## Описание
Todo App Telegram bot — это бот для управления задачами. Взаимодействует с API приложения toDo либо может работать автономно 
Оно позволяет пользователям добавлять, удалять и отмечать задачи как выполненные, что помогает организовать повседневные дела.


## Функции
- Добавление новых задач
- Удаление задач
- Отметка задач как выполненных

## Установка
ВНИМАНИЕ! ПОДРАЗУМЕВАЕТСЯ ЧТО У ВАС УЖЕ ЕСТЬ API БОТА , КАК СОЗДАТЬ БОТА ИНФОРМАЦИЮ МОЖНО НАЙТИ ТУТ: [ДОКУМЕНТАЦИЯ TELEGRAM](https://core.telegram.org/bots/features#creating-a-new-bot)<br><br>
Для установки приложения выполните следующие шаги:

1.Для развертывания на своем компьютере:<br>
  1.1 Клонируйте репозиторий:<br>
     ```
       git clone https://github.com/JolyCougar/toDo_Telegram.git
       ```<br>
  1.2 Создайте файл .env с вашими переменными:<br>
   ```
      API_TOKEN='Укажите API ключ вашего бота'
      DJANGO_API_URL='Укажите здесь адрес на котором стоит приложение toDo_app + /api/v1'  
      DB_HOST='local_db'
      DB_NAME='Укажите здесь то что будет в db.env POSTGRES_DB'
      DB_USER='Укажите пользователя который будет в db.env'
      DB_PASSWORD='Укажите пароль который будет в db.env'

   ```
  1.3 Создайте файл db.env с вашими переменными:<br>
```
  POSTGRES_USER='Укажите здесь пользователя который будет создан в БД'
  POSTGRES_PASSWORD='Укажите здесь пароль который будет создан в БД'
  POSTGRES_DB='Укажите название БД'
```
  1.4 Скачайте и установите docker и docker-compose [Установка Docker](https://docs.docker.com/engine/install/)<br>
  1.5 Перейдите в папку с проектом в комадной строке<br>
  1.6 Напишите команду:<br>
    ```
      docker-compose up --build
    ```<br>
  1.7 Приложение доступно в телеграме в боте которого вы создали)<br>
2. Развертывание на сервере происходит аналогичным образом