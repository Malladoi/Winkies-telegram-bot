author = 'KSugonyakin'

import psycopg2
from psycopg2 import extensions as ext
import os

vendors = [
    'Apple',
    'Acer',
    'Asus',
    'Google',
    'HTC',
    'Huawei',
    'Lenovo',
    'LG',
    'Meizu',
    'Microsoft',
    'Motorola',
    'Nokia',
    'OnePlus',
    'Samsung',
    'Sony',
    'Xiaomi',
    'ZTE',
    'Alcatel',
    'Explay',
    'Fly',
    'Texet',
    'Prestigio',
    'Другой бренд']

issues = [
    'Ремонт модуля дисплея / LCD (ЖК) экрана',
    'Ремонт стекла дисплея',
    'Ремонт тачскрина / сенсорного экрана',
    'Ремонт аккумулятора',
    'Ремонт разъема питания',
    'Ремонт разъема наушников',
    'Ремонт слухового динамика',
    'Ремонт динамика звонка',
    'Ремонт кнопки включения',
    'Ремонт микрофона',
    'Замена / ремонт корпуса',
    'Ремонт камеры фронтальной/основной',
    'Прошивка',
    'Восстановление после попадания воды',
    'Подбор графического ключа',
    'Сохранение данных / контактов',
    'Ремонт датчика приближения',
    'Замена задней крышки',
    'Ремонт кнопок громкости',
    'Разблокировка'

]


def getserverversion(conn: psycopg2._ext.connection):
    return conn.server_version


def recreatedb(conn: psycopg2._ext.connection):
    recreatecommands = (
        """
        DROP TABLE IF EXISTS vendors, issues CASCADE 
        """,
        """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE issues (
                issue_id SERIAL PRIMARY KEY,
                issue_name VARCHAR(255) NOT NULL
                )
        """)
    insertvendorcommand = """insert into vendors(vendor_id, vendor_name) values({0}, '{1}')"""
    insertissuecommand = """insert into issues(issue_id, issue_name) values({0}, '{1}')"""
    try:
        if conn.status == 1:
            cur = conn.cursor()
            # create table one by one
            for command in recreatecommands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        if conn.status == 1:
            cur = conn.cursor()
            # create table one by one
            for i, vendor in enumerate(vendors):
                cur.execute(insertvendorcommand.format(i, vendor))
            cur.close()
            # commit the changes
            conn.commit()
        if conn.status == 1:
            cur = conn.cursor()
            # create table one by one
            for i, issue in enumerate(issues):
                cur.execute(insertissuecommand.format(i, issue))
            cur.close()
            # commit the changes
            conn.commit()
        return -1
    except (Exception, psycopg2.DatabaseError) as error:
        return error
