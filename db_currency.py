import sqlite3 # Импорт библиотеки для работы с БД
import matplotlib.pyplot as plt # Импорт библиотеки для построения графиков


# Маркеры валют:
# 1 - Доллар США
# 2 - Евро
# 3 - Юань
# 4 - Турецкая лира


def db_add(cur_now,date_now,db_marker): # Объявление функции для добавления данных в таблицы валют
    base = sqlite3.connect('CUR_1.db') # Установка соединения с БД
    cursor = base.cursor() # Объявление курсора
    if (db_marker == 1):
        base.execute('CREATE TABLE IF NOT EXISTS USD_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        base.execute("""INSERT INTO USD_VAL (value, date) VALUES ( ?, ?)""", (cur_now[0:5],date_now)) # Добавление ячейки в таблицу с входными данными
        base.commit() # Сохранение внесенных изменений в БД
    if (db_marker == 2):
        base.execute('CREATE TABLE IF NOT EXISTS EUR_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        base.execute("""INSERT INTO EUR_VAL (value, date) VALUES ( ?, ?)""", (cur_now[0:5],date_now))# Добавление ячейки в таблицу с входными данными
        base.commit() # Сохранение внесенных изменений в БД
    if (db_marker == 3):
        base.execute('CREATE TABLE IF NOT EXISTS CNY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        base.execute("""INSERT INTO CNY_VAL (value, date) VALUES ( ?, ?)""", (cur_now[0:4],date_now))# Добавление ячейки в таблицу с входными данными
        base.commit() # Сохранение внесенных изменений в БД
    if (db_marker == 4):
        base.execute('CREATE TABLE IF NOT EXISTS TRY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        base.execute("""INSERT INTO TRY_VAL (value, date) VALUES ( ?, ?)""", (cur_now[0:4],date_now))# Добавление ячейки в таблицу с входными данными
        base.commit() # Сохранение внесенных изменений в БД

def db_last(db_marker): # Объявление функции для запроса даты из последней ячейки таблицы с определенной валютой
    base = sqlite3.connect('CUR_1.db') # Установка соединения с БД
    cursor = base.cursor() # Объявление курсора
    if (db_marker == 1):
        base.execute('CREATE TABLE IF NOT EXISTS USD_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        search_db = cursor.execute('SELECT date FROM USD_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
    if (db_marker == 2):
        base.execute('CREATE TABLE IF NOT EXISTS EUR_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        search_db = cursor.execute('SELECT date FROM EUR_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
    if (db_marker == 3):
        base.execute('CREATE TABLE IF NOT EXISTS CNY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        search_db = cursor.execute('SELECT date FROM CNY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
    if (db_marker == 4):
        base.execute('CREATE TABLE IF NOT EXISTS TRY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        search_db = cursor.execute('SELECT date FROM TRY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
    # Преобразование строки для определенного вида
    search_db[-1] = (str(search_db[-1]))
    count_cell = -3
    search_db = search_db[-1][2:count_cell]
    mark_str = 0
    len_cell = len(search_db)
    for count_str in range(len_cell):
        if (search_db[count_str] == ' '):
            mark_str = count_str
            day_db = search_db[0:mark_str]
            break
    month_db = search_db[mark_str+1:len_cell-5]
    year_db = search_db[len_cell-4:len_cell]
    return(day_db,month_db,year_db) # Возвращение даты, записанной в таблице последней

def convert_str(value_con, date_con): # Объявление функции для преобразование строки курса валюты и даты к определенному виду
    date_con = date_con[2:-3]
    value_con = value_con[1:-2]
    return(value_con, date_con) # Возвращение форматированного вида курса и даты

def db_date_last(db_marker): # Объявление функции, возвращающей значения курса и даты, записанные последними в таблице
    base = sqlite3.connect('CUR_1.db') # Установка соединения с БД
    cursor = base.cursor() # Объявление курсора

    if (db_marker == 1):
        base.execute('CREATE TABLE IF NOT EXISTS USD_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        date_db = cursor.execute('SELECT date FROM USD_VAL').fetchall()  # Запрос всех ячеек из столбца с именем 'date'
        course_db = cursor.execute('SELECT value FROM USD_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
    if (db_marker == 2):
        base.execute('CREATE TABLE IF NOT EXISTS EUR_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        date_db = cursor.execute('SELECT date FROM EUR_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        course_db = cursor.execute('SELECT value FROM EUR_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
    if (db_marker == 3):
        base.execute('CREATE TABLE IF NOT EXISTS CNY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        date_db = cursor.execute('SELECT date FROM CNY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        course_db = cursor.execute('SELECT value FROM CNY_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
    if (db_marker == 4):
        base.execute('CREATE TABLE IF NOT EXISTS TRY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        date_db = cursor.execute('SELECT date FROM TRY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        course_db = cursor.execute('SELECT value FROM TRY_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
    course_db, date_db = convert_str(str(course_db[-1]), str(date_db[-1]))
    return(course_db, date_db) # Возвращение курса и даты

def db_graph(db_marker): # Объявление функции для построения графика исходя из значений, взятых из таблицы БД
    base = sqlite3.connect('CUR_1.db') # Установка соединения с БД
    cursor = base.cursor() # Объявление курсора
    if (db_marker == 1):
        base.execute('CREATE TABLE IF NOT EXISTS USD_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        course_db = cursor.execute('SELECT value FROM USD_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
        date_db = cursor.execute('SELECT date FROM USD_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        plt.title('График курса Доллара США к рублю Российской Федерации за последние 7 дней') # Заголовок графика

    if (db_marker == 2):
        base.execute('CREATE TABLE IF NOT EXISTS EUR_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        course_db = cursor.execute('SELECT value FROM EUR_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
        date_db = cursor.execute('SELECT date FROM EUR_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        plt.title('График курса Евро к рублю Российской Федерации за последние 7 дней') # Заголовок графика

    if (db_marker == 3):
        base.execute('CREATE TABLE IF NOT EXISTS CNY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        course_db = cursor.execute('SELECT value FROM CNY_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
        date_db = cursor.execute('SELECT date FROM CNY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        plt.title('График курса Юаня к рублю Российской Федерации за последние 7 дней') # Заголовок графика

    if (db_marker == 4):
        base.execute('CREATE TABLE IF NOT EXISTS TRY_VAL(date text, value real)') # Создание таблицы в БД с конкретным именем, если такой еще не существует
        course_db = cursor.execute('SELECT value FROM TRY_VAL').fetchall() # Получение всех ячеек из столбца с именем 'value'
        date_db = cursor.execute('SELECT date FROM TRY_VAL').fetchall() # Запрос всех ячеек из столбца с именем 'date'
        plt.title('График курса Турецкой лиры к рублю Российской Федерации за последние 7 дней') # Заголовок графика
    # Объявление списков для курса валюты и даты
    list_value = []
    list_date = []
    for count_gr in range (-7,0, 1): # Цикл для заполнения списков дат и курса валют
        course_db_elem, date_db_elem = convert_str(str(course_db[count_gr]), str(date_db[count_gr]))
        list_value.append(float(course_db_elem))
        list_date.append(date_db_elem)

    plt.ylabel('Рубли, ₽') # Подпись оси y
    plt.grid() # Включение сетки на графике
    plt.plot(list_date,list_value,  color = 'C7', marker = '.') # Построение графика
    plt.xticks(rotation=25) # Поворот подписей оси X
    plt.savefig('graph.png', bbox_inches='tight') # Сохранение графика
    plt.clf() # Удаление графика

if __name__ == '__main__':
    db_graph()
    # курс, дата, маркер