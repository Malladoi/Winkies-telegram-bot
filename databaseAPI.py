author = 'KSugonyakin'

import psycopg2
from telebot import types
import datetime
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
    'Разблокировка']

request_statuses = [
    'Не отвечено',
    'В процессе',
    'Закрыто',
    ]



def getserverversion(conn: psycopg2._ext.connection):
    return conn.server_version


def recreatedb(conn: psycopg2._ext.connection):
    recreatecommands = (
        """
        DROP TABLE IF EXISTS vendors, issues, registered_requests, request_statuses CASCADE 
        """,
        """
        CREATE TABLE IF NOT EXISTS vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS issues (
                issue_id SERIAL PRIMARY KEY,
                issue_name VARCHAR(255) NOT NULL
                )
        """,
        """ CREATE TABLE IF NOT EXISTS request_statuses (
                        status_id SERIAL PRIMARY KEY,
                        status_name VARCHAR(255) NOT NULL
                        )
        """,
        """ CREATE TABLE IF NOT EXISTS registered_requests (
                request_id SERIAL PRIMARY KEY,
                status_id SERIAL NOT NULL,
                user_id SERIAL NOT NULL,
                request_text text NOT NULL,
                FOREIGN KEY (status_id)
                    REFERENCES request_statuses (status_id)
                    ON UPDATE CASCADE ON DELETE CASCADE                
                )
        """,
        """ CREATE SEQUENCE seq_request_id START 1;
        """
    )
    insertvendorcommand = """insert into vendors(vendor_id, vendor_name) values({0}, '{1}')"""
    insertissuecommand = """insert into issues(issue_id, issue_name) values({0}, '{1}')"""
    insertrequeststatusescommand = """insert into request_statuses(status_id, status_name) values({0}, '{1}')"""
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
        if conn.status == 1:
            cur = conn.cursor()
            # create table one by one
            for i, request_status in enumerate(request_statuses):
                cur.execute(insertrequeststatusescommand.format(i, request_status))
            cur.close()
            # commit the changes
            conn.commit()
        return -1
    except (Exception, psycopg2.DatabaseError) as error:
        return error


def registratenewrequest(conn: psycopg2._ext.connection, message: types.Message):
    insertrequestcommand = """insert into registered_requests(request_id, status_id, user_id, request_text) 
    values(nextval('seq_request_id'), 0, {0}, '{1}'"""
    # print(datetime.datetime(message.date))
    if conn.status == 1:
        cur = conn.cursor()
        cur.execute(insertrequestcommand.format(message.from_user.id, message.text))
        cur.close()
        conn.commit()
    return -1
