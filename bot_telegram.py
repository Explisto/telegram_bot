from aiogram import Bot, types # Импорт класса бота и специальный тип для аннотаций в функциях
from aiogram.dispatcher import Dispatcher # Импорт класса для регистрации событий в чате
from aiogram.utils import executor # Импорт модуля для обработки событий
from pas import pars_currency # Импорт функции для парсинга сайтов
import os # Импорт модуля для работы с операционной системой
from db_currency import* # Импорт модуля для работы с базами данных
import datetime # Импорт модуля для работы с системным временем

bot = Bot(token=os.getenv('TOKEN'))  # Инициализация бота прием токена из виртуальной среды
dp = Dispatcher(bot) # Инициализация диспетчера

async def on_startup(_): # Объявление асинхронной функции для записи о статусе бота
    print('Бот онлайн')

# Маркеры валют:
# 1 - Доллар США
# 2 - Евро
# 3 - Юань
# 4 - Турецкая лира

###
def check_date_today(marker_course): # Объявление функции для преобразования системной даты к названию месяца от его номера
    now_date = datetime.datetime.now() # Получение текущей даты
    month_now = now_date.month # Получение текущего месяца
    day_now = now_date.day # Получение текущего для
    year_now = now_date.year # Получение текущего года

    # Преобразование названия месяца в зависимости от его номера
    if (month_now == 1):
        month_now = 'января'
    if (month_now == 2):
        month_now = 'февраля'
    if (month_now == 3):
        month_now = 'марта'
    if (month_now == 4):
        month_now = 'апреля'
    if (month_now == 5):
        month_now = 'мая'
    if (month_now == 6):
        month_now = 'июня'
    if (month_now == 7):
        month_now = 'июля'
    if (month_now == 8):
        month_now = 'августа'
    if (month_now == 9):
        month_now = 'сентября'
    if (month_now == 10):
        month_now = 'октября'
    if (month_now == 11):
        month_now = 'ноября'
    if (month_now == 12):
        month_now = 'декабря'

    # Вызов функции для получения данных о последнем записанном значении в таблицу
    # Номер - это маркер для каждой валюты
    # 1 - Доллар США
    # 2 - Евро
    # 3 - Юань
    # 4 - Турецкая лира

    if (marker_course == 1):
        day_db, month_db, year_db = db_last(1)
    if (marker_course == 2):
        day_db, month_db, year_db = db_last(2)
    if (marker_course == 3):
        day_db, month_db, year_db = db_last(3)
    if (marker_course == 4):
        day_db, month_db, year_db = db_last(4)

    # Если данные в таблице уже внесены
    if (str(day_db) == str(day_now)) and (month_db == month_now) and (str(year_db) == str(year_now)):
        return(1)
    # Если данных нет
    else:
        return(0)


@dp.message_handler(commands = 'start') # Декоратор для реакции бота на определенную команду
async def cmd_start(message: types.Message): # Объявление асинхронной функции для начала работы с ботом
    # Создание интерактивной клавитуры для взаимодействия с пользователем
    kb_1 = types.KeyboardButton(text='Доллар США')
    kb_2 = types.KeyboardButton(text='Евро')
    kb_3 = types.KeyboardButton(text='Юань')
    kb_4 = types.KeyboardButton(text='Турецкая лира')
    kb_5 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name_file = "salute.txt" # Наименование файла с приветственными словами
    sal_str = ""
    file_input = open(name_file, 'r', encoding='utf-8') # Открытие файла с приветствием
    for count_key in range(11): # Цикл чтения файла
        inf_ser = file_input.read()
        sal_str =  sal_str + inf_ser
    file_input.close() # Закрытие файла
    keyboard.add(kb_1).insert(kb_2).add(kb_3).insert(kb_4).add(kb_5) # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer(sal_str, reply_markup=keyboard) # Ответ пользователю в чате

### Доллар США

@dp.message_handler(text = ['Доллар США']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для работы с конкретной валютой
    # Создание интерактивной клавитуры для взаимодействия с пользователем
    kb_1_1 = types.KeyboardButton(text='Вывести курс Доллара США на сегодня')
    kb_2_1 = types.KeyboardButton(text='Вывести график курса Доллара США за последние 7 дней')
    kb_3_1 = types.KeyboardButton(text='Вывести информацию о Долларе США')
    kb_4_1 = types.KeyboardButton(text='Вернуться к выбору валюты')
    kb_5_1 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(kb_1_1).insert(kb_2_1).add(kb_3_1).insert(kb_4_1).add(kb_5_1)  # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer('Выберите один из предложенных пунктов:', reply_markup=keyboard) # Сообщение пользователю

@dp.message_handler(text = ['Вывести курс Доллара США на сегодня']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода сегодняшнего курса валюты
    if (check_date_today(1) == 0): # Если сегодняшнее значение не записано в таблицу БД
        result_pars, date_pars = pars_currency(1) # Вызов функции для парсинга сайта
        db_add(result_pars, date_pars,1) # Вызов функции для добавления ячейки в таблицу
        answer_user_tg = "Курс Доллара США на сегодня:\n" + date_pars + "\n" + result_pars # Формирование сообщения
    else: # Если значение есть в таблице БД
        result_pars, date_pars = db_date_last(1) # Забираем данные из таблицы БД
        answer_user_tg = "Курс Доллара США на сегодня:\n" + date_pars + "\n" + result_pars + " ₽" # Формирование сообщения
    await message.answer(answer_user_tg) # Вывод сообщения пользователю

@dp.message_handler(text = ['Вывести график курса Доллара США за последние 7 дней']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода графика
    db_graph(1) # Вызов функции для построения графика курса валюты
    photo = open('graph.png', 'rb') # Объявление объекта - фото
    await bot.send_photo(chat_id = message.chat.id, photo = photo) # Отправка фотографии в виде сообщения

@dp.message_handler(text = ['Вывести информацию о Долларе США']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода информации о валюте
    name_file = "information_USD.txt" # Название файла с информацией о валюте
    file_input = open(name_file, 'r', encoding='utf-8') # Открытие файла с информацией о валюте
    inf_s_1 = file_input.readline() # Чтение файла
    inf_s_2 = file_input.readline()
    await message.answer('=Краткая информация о Долларе США=\n'+inf_s_1+inf_s_2) # Вывод сообщения пользователю
    file_input.close() # Закрытие файла


### Евро

@dp.message_handler(text = ['Евро']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для работы с конкретной валютой
    # Создание интерактивной клавитуры для взаимодействия с пользователем
    kb_1_1 = types.KeyboardButton(text='Вывести курс Евро на сегодня')
    kb_2_1 = types.KeyboardButton(text='Вывести график курса Евро за последние 7 дней')
    kb_3_1 = types.KeyboardButton(text='Вывести информацию о Евро')
    kb_4_1 = types.KeyboardButton(text='Вернуться к выбору валюты')
    kb_5_1 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # Вывод кнопок клавиатуры в определенном порядке пользователю

    keyboard.add(kb_1_1).insert(kb_2_1).add(kb_3_1).insert(kb_4_1).add(kb_5_1)  # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer('Выберите один из предложенных пунктов:', reply_markup=keyboard)  # Сообщение пользователю

@dp.message_handler(text = ['Вывести курс Евро на сегодня']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода сегодняшнего курса валюты
    if (check_date_today(2) == 0): # Если сегодняшнее значение не записано в таблицу БД
        result_pars, date_pars = pars_currency(2) # Вызов функции для парсинга сайта
        db_add(result_pars, date_pars,2) # Вызов функции для добавления ячейки в таблицу
        answer_user_tg = "Курс Евро на сегодня:\n" + date_pars + "\n" + result_pars # Формирование сообщения
    else:
        result_pars, date_pars = db_date_last(2) # Забираем данные из таблицы БД
        answer_user_tg = "Курс Евро на сегодня:\n" + date_pars + "\n" + result_pars + " ₽" # Формирование сообщения
    await message.answer(answer_user_tg) # Вывод сообщения пользователю

@dp.message_handler(text = ['Вывести график курса Евро за последние 7 дней']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода графика
    db_graph(2) # Вызов функции для построения графика курса валюты
    photo = open('graph.png', 'rb') # Объявление объекта - фото
    await bot.send_photo(chat_id = message.chat.id, photo = photo) # Отправка фотографии в виде сообщения

@dp.message_handler(text = ['Вывести информацию о Евро']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода информации о валюте
    name_file = "information_EUR.txt" # Название файла с информацией о валюте
    file_input = open(name_file, 'r', encoding='utf-8') # Открытие файла с информацией о валюте
    inf_s_1 = file_input.readline() # Чтение файла
    inf_s_2 = file_input.readline()
    await message.answer('=Краткая информация о Евро=\n'+inf_s_1+inf_s_2) # Вывод сообщения пользователю в чате
    file_input.close() # Закрытие файла


### Юань

@dp.message_handler(text = ['Юань']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для работы с конкретной валютой
    # Создание интерактивной клавитуры для взаимодействия с пользователем
    kb_1_1 = types.KeyboardButton(text='Вывести курс Юаня на сегодня')
    kb_2_1 = types.KeyboardButton(text='Вывести график курса Юаня за последние 7 дней')
    kb_3_1 = types.KeyboardButton(text='Вывести информацию о Юане')
    kb_4_1 = types.KeyboardButton(text='Вернуться к выбору валюты')
    kb_5_1 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # Вывод кнопок клавиатуры в определенном порядке пользователю

    keyboard.add(kb_1_1).insert(kb_2_1).add(kb_3_1).insert(kb_4_1).add(kb_5_1) # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer('Выберите один из предложенных пунктов:', reply_markup=keyboard) # Сообщение пользователю

@dp.message_handler(text = ['Вывести курс Юаня на сегодня']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода сегодняшнего курса валюты
    if (check_date_today(3) == 0): # Если сегодняшнее значение не записано в таблицу БД
        result_pars, date_pars = pars_currency(3) # Вызов функции для парсинга сайта
        db_add(result_pars, date_pars,3) # Вызов функции для добавления ячейки в таблицу
        answer_user_tg = "Курс Юаня на сегодня:\n" + date_pars + "\n" + result_pars # Формирование сообщения
    else: # Если значение есть в таблице БД
        result_pars, date_pars = db_date_last(3) # Забираем данные из таблицы БД
        answer_user_tg = "Курс Юаня на сегодня:\n" + date_pars + "\n" + result_pars + " ₽" # Формирование сообщения
    await message.answer(answer_user_tg) # Вывод сообщения пользователю

@dp.message_handler(text = ['Вывести график курса Юаня за последние 7 дней']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода графика
    db_graph(3) # Вызов функции для построения графика курса валюты
    photo = open('graph.png', 'rb') # Объявление объекта - фото
    await bot.send_photo(chat_id = message.chat.id, photo = photo) # Отправка фотографии в виде сообщения

@dp.message_handler(text = ['Вывести информацию о Юане']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода информации о валюте
    name_file = "information_CNY.txt" # Название файла с информацией о валюте
    file_input = open(name_file, 'r', encoding='utf-8')  # Открытие файла с информацией о валюте
    inf_s_1 = file_input.readline() # Чтение файла
    inf_s_2 = file_input.readline()
    await message.answer('=Краткая информация о Юане=\n'+inf_s_1+inf_s_2) # Вывод сообщения пользователю в чате
    file_input.close() # Закрытие файла


### Турецкая лира

@dp.message_handler(text = ['Турецкая лира']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для работы с конкретной валютой
    # Создание интерактивной клавитуры для взаимодействия с пользователем
    kb_1_1 = types.KeyboardButton(text='Вывести курс Турецкой лиры на сегодня')
    kb_2_1 = types.KeyboardButton(text='Вывести график курса Турецкой лиры за последние 7 дней')
    kb_3_1 = types.KeyboardButton(text='Вывести информацию о Турецкой лире')
    kb_4_1 = types.KeyboardButton(text='Вернуться к выбору валюты')
    kb_5_1 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) # Вывод кнопок клавиатуры в определенном порядке пользователю

    keyboard.add(kb_1_1).insert(kb_2_1).add(kb_3_1).insert(kb_4_1).add(kb_5_1)  # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer('Выберите один из предложенных пунктов:', reply_markup=keyboard) # Сообщение пользователю

@dp.message_handler(text = ['Вывести курс Турецкой лиры на сегодня']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода сегодняшнего курса валюты
    if (check_date_today(4) == 0): # Если сегодняшнее значение не записано в таблицу БД
        result_pars, date_pars = pars_currency(4) # Вызов функции для парсинга сайта
        db_add(result_pars, date_pars,4) # Вызов функции для добавления ячейки в таблицу
        answer_user_tg = "Курс Турецкой лиры на сегодня:\n" + date_pars + "\n" + result_pars # Формирование сообщения
    else: # Если значение есть в таблице БД
        result_pars, date_pars = db_date_last(4) # Забираем данные из таблицы БД
        answer_user_tg = "Курс Турецкой лиры на сегодня:\n" + date_pars + "\n" + result_pars + " ₽" # Формирование сообщения
    await message.answer(answer_user_tg) # Вывод сообщения пользователю

@dp.message_handler(text = ['Вывести график курса Турецкой лиры за последние 7 дней']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода графика
    db_graph(4) # Вызов функции для построения графика курса валюты
    photo = open('graph.png', 'rb') # Объявление объекта - фото
    await bot.send_photo(chat_id = message.chat.id, photo = photo) # Отправка фотографии в виде сообщения

@dp.message_handler(text = ['Вывести информацию о Турецкой лире']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для вывода информации о валюте
    name_file = "information_TRY.txt" # Название файла с информацией о валюте
    file_input = open(name_file, 'r', encoding='utf-8') # Открытие файла с информацией о валюте
    inf_s_1 = file_input.readline() # Чтение файла
    await message.answer('=Краткая информация о Турецкой лире=\n'+inf_s_1) # Вывод сообщения пользователю в чате
    file_input.close() # Закрытие файла

### Кнопка 'Назад'

@dp.message_handler(text = ['Вернуться к выбору валюты']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление асинхронной функции для возвращения исходной клавиатуры
    kb_1 = types.KeyboardButton(text='Доллар США')
    kb_2 = types.KeyboardButton(text='Евро')
    kb_3 = types.KeyboardButton(text='Юань')
    kb_4 = types.KeyboardButton(text='Турецкая лира')
    kb_5 = types.KeyboardButton(text='Помощь')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(kb_1).insert(kb_2).add(kb_3).insert(kb_4).add(kb_5) # Вывод кнопок клавиатуры в определенном порядке пользователю
    await message.answer('Выберите одну из предложенных валют:', reply_markup=keyboard) # Вывод сообщения пользователю в чате

### Кнопка 'Помощь'

@dp.message_handler(text = ['Помощь']) # Декоратор функции для реакции бота на определенную команду пользователя
async def with_puree(message: types.Message): # Объявление функции для вывода инструкции пользователю
    name_file = "helping.txt" # Имя файла с инструкцией
    help_str = ""
    file_input = open(name_file, 'r', encoding='utf-8') # Открытие файла
    for count_key in range(11): # Чтение файла
        inf_ser = file_input.read()
        help_str = help_str + inf_ser
    file_input.close() # Закрытие файла
    await message.answer(help_str) # Вывод сообщения пользователю в чате


### Общий хендлер

@dp.message_handler() # Декоратор, объявляющий событие в чате
async def echo_send(message : types.Message): # Объявление асинхронной функции для ответа на сообщение
    if message.text == 'Привет':
        await message.answer('И тебе привет!') # Ожидание, пока в потоке не появится свободное окно. Отправка сообщения пользователю
    else:
        await message.answer('Неизвестная команда. Пожалуйста, действуйте в соответствии с интсрукцией. Ее можно прочитать с помощью кнопки "Помощь".') # Отправка сообщения пользователю

executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # Запуск бота в режиме Long polling и пропуск сообщений, когда бот не онлайн