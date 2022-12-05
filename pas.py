import requests # Импорт библиотеки для составления HTTP-запросов
from bs4 import BeautifulSoup # Импорт библиотеки для парсинга сайтов

# Запись URL страниц для парсинга

URL_USD = 'https://www.tinkoff.ru/invest/currencies/USDRUB/'

URL_EUR = 'https://www.tinkoff.ru/invest/currencies/EURRUB/'

URL_CNY = 'https://www.tinkoff.ru/invest/currencies/CNYRUB/'

URL_TRY = 'https://www.tinkoff.ru/invest/currencies/TRYRUB/'

# URL_HAG = 'https://cbr.ru/curreNcy_base/daily/'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Маркеры валют:
# 1 - Доллар США
# 2 - Евро
# 3 - Юань
# 4 - Турецкая лира

def pars_currency(MARK_CURRENCY): # Объявление функции для парсинга сайта

    # Выбор URL адреса в зависимости от выбранной валюты

    if (MARK_CURRENCY == 1):
        URL_CURRENCY = URL_USD

    if (MARK_CURRENCY == 2):
        URL_CURRENCY = URL_EUR

    if (MARK_CURRENCY == 3):
        URL_CURRENCY = URL_CNY

    if (MARK_CURRENCY == 4):
        URL_CURRENCY = URL_TRY

    response = requests.get(URL_CURRENCY, timeout=30, headers=headers) # Get-запрос и получения кода состояния

    soup = BeautifulSoup(response.content, features="html.parser") # Получение кода HTML-страницы

    CURRENCY_ALL = soup.find_all("span", {"class": "Money-module__money_UZBbh"})[7].text # Поиск тэга и класса с интересующей нас информацией

    CURRENCY_ALL = CURRENCY_ALL.replace(',', '.') # Замена в строке запятой на точку

    DATE_ALL = soup.find_all("div", {"data-qa-file": "SecurityInvitingScreen"})[1].text # Поиск тэга и класса с интересующей нас информацией

    # Форматирование строки даты
    len_date = len(DATE_ALL)

    DATE_ALL = DATE_ALL[12:len_date]

    return(CURRENCY_ALL, DATE_ALL) # Возвращение полученных значений курса валюты и даты


if __name__ == '__main__':
    pars_currency(4)
