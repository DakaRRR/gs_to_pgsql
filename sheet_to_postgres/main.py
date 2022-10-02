import time
from decouple import config
from datetime import datetime
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import gspread

import psycopg2

# Считывание данных с env файла
DB_NAME = config('POSTGRES_DB_NAME')
DB_HOST = config('POSTGRES_HOST')
DB_USER = config('POSTGRES_USER')
DB_PASSWORD = config('POSTGRES_PASSWORD')
DB_PORT = config('POSTGRES_PORT')
JSON_FILE_NAME = config('JSON_FILE_NAME')
GOOGLE_SHEET_NAME = config('GOOGLE_SHEET_NAME')
GOOGLE_SHEET_LIST_NAME = config('GOOGLE_SHEET_LIST_NAME')


def load_google_sheets_list():
    '''Подключение к аккаунту с json файла'''
    sa = gspread.service_account(filename=JSON_FILE_NAME)

    sh = sa.open(GOOGLE_SHEET_NAME)

    '''Чтение данных из документа Google Sheets'''
    worksheet = sh.worksheet(GOOGLE_SHEET_LIST_NAME)
    return worksheet.get_all_values() # Все значения таблицы


def get_usd_quote(url):
    '''Возвращает стоимость одного доллара США в рублях по курсу ЦБ РФ'''
    html = urllib.request.urlopen(url).read().decode(encoding="windows-1251")
    data = ET.fromstring(html)
    usd_quote = float(
        (data.find("Valute[@ID='R01235']/Value").text).replace(',', '.'))
    return usd_quote


'''Подключение к БД через данные env файла'''
def connect_to_database():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                host=DB_HOST,
                                user=DB_USER,
                                password=DB_PASSWORD,
                                port=DB_PORT)

    except psycopg2.DatabaseError as e:
        print('Database error')
        print(str(e.value[1]))
    except psycopg2.Error as e:
        print('Connection error')
        print(str(e.value[1]))

    else:
        cursor = conn.cursor()
    '''Создание таблицы если её нет в БД'''
    cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", ('orders_app_order',))
    if not cursor.fetchone()[0]:
        create_query = '''CREATE TABLE orders_app_order (id int,"заказ №" int UNIQUE,"стоимость,$" int,"срок поставки" date,"стоимость в руб." int);'''
        cursor.execute(create_query)
    return conn, cursor


def get_order_numbers(CURSOR):
    '''Получает список номеров заказов, которые на данный момент находятся в базе данных PostgreSQL'''
    check_query = '''select "заказ №" from orders_app_order;'''
    CURSOR.execute(check_query)
    order_numbers = CURSOR.fetchall()
    numbers = [number[0] for number in order_numbers]
    return numbers


def delete_orders(CONNECTION, CURSOR, orders):
    '''Удаляет записи о заказах, которых более нет в исходном файле Google Sheets'''
    if len(orders) == 1:
        orders = f'({orders[0]})'
    delete_query = f'''delete from orders where "заказ №" in {orders}'''
    CURSOR.execute(delete_query)
    CONNECTION.commit()


def load_database_list(CURSOR):
    '''Получает список всех заказов(кроме колонки "стоимость в руб."), которые на данный момент находятся в базе данных PostgreSQL'''
    get_data_query = '''select "id","заказ №","стоимость,$","срок поставки" from orders_app_order order by orders_app_order.id;'''
    CURSOR.execute(get_data_query)
    orders = CURSOR.fetchall()
    orders = [list(order) for order in orders]
    for order in orders:
        for i in range(3):
            order[i] = str(order[i])
        order[3] = datetime.strptime(str(order[3]), '%Y-%m-%d').strftime('%d.%m.%Y')
    return orders


def main():
    while True:
        # Подключение к БД PostgreSQL
        CONNECTION, CURSOR = connect_to_database()
        # Сбор данных c БД PostgreSQL
        database_data = load_database_list(CURSOR)
        # Сбор данных c Google Sheets
        google_sheets_data = load_google_sheets_list()
        if google_sheets_data[1:] == database_data:
            pass
        else:
            database_orders = get_order_numbers(CURSOR)
            current_orders = [int(order[1]) for order in google_sheets_data[1:]]
            obsolete_orders = tuple()
            for order in database_orders:
                if order not in current_orders:
                    obsolete_orders += (order,)

            # Удаление неактуальных заказов, которых уже нет в документе Google Sheets
            if obsolete_orders:
                delete_orders(CONNECTION, CURSOR, obsolete_orders)

            # Получение текущего курса доллара США
            link = 'https://www.cbr.ru/scripts/XML_daily.asp'
            exchange_rate = get_usd_quote(link)

            # Форматирование полученных данных перед добавлением в таблицу
            for order in google_sheets_data[1:]:
                for i in range(3):
                    order[i] = int(order[i])
                order[3] = datetime.strptime(order[3], "%d.%m.%Y").date()
                ruble_price = order[2] * exchange_rate
                order += [int(ruble_price)]

            # Обработка информации, которую необходимо записать в базу данных PostgreSQL
            orders = [tuple(order) for order in google_sheets_data[1:]]

            args = ','.join(CURSOR.mogrify("(%s,%s,%s,%s,%s)", i).decode('utf-8')
                            for i in orders)

            insert_query = "INSERT INTO orders_app_order VALUES " + \
                           (args) + ' on conflict ("заказ №") ' \
                                    'do update set "стоимость,$"=excluded."стоимость,$", "срок поставки"=excluded."срок поставки", "стоимость в руб."=excluded."стоимость в руб."'
            CURSOR.execute(insert_query)
            CONNECTION.commit()
            CONNECTION.close()
            print("Скрипт успешно завершил работу!")
        time.sleep(1)


if __name__ == "__main__":
    main()
