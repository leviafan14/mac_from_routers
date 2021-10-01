#!/usr/bin/env python
# -*- coding: utf_8 -*-

import pymysql

# Функция создаёт подключение к БД
def connect_to_db(username:str, password:str, db_name:str, host:str) -> object:
    try:
        con = pymysql.connect(
        host = host,
        user = username
        password = password,
        db = db_name,
        charset = "utf8mb4",
        use_unicode = True
        )
        return con
    except Exception as e:
        print(f"Не удалось создать подключение к БД\n{e}")
        return 1


# Функция записывает vlan и mac в таблицу
def insert_to_users_mac(vlan:str, mac:str, con:object) -> int:
    table_name = "users_mac"
    cursor = mysql_db.db.cursor()
    
    # Проверка, есть ли мак адрес с таким вланом в таблице
    try:
        select_data = f"SELECT mac FROM {table_name} WHERE vlan={vlan}"
        result_mac = cursor.execute(select_data)
    except Exception as e:
        print("Не удалось получить MAC адрес из таблицы {users_mac}\n{e}"
        return 1
    
    # Если такой мак с таким вланом есть
    if result_mac != '':
        # Если мак с маршрутизатора не совпадает с маком из таблицы то его обновляем в таблице
        if mac != result_mac:
            try:
                update_mac = f"UPDATE {table_name} SET mac = {mac} WHERE  vlan = {vlan}"
                cursor.execute(update_mac)
            except Exception as e:
                print(f"Не удалось обновить MAC адрес в таблице {table_name}\n{e}")
                return 1
        else:
            pass
        
    # Если такого мак адреса нет, то вставляется запись в таблицу
    else:
        try:
            insert_row = f"INSERT INTO {table_name} (vlan, mac) VALUES ({vlan}, {mac})"
            cursor.execute(insert_row)
        except Exception as e:
            print(f"Не удалось вставить запись в {table_name}, возможно такой vlan: {vlan} и mac-address: {mac}\n уже есть\n{e}"
            return 1
    
    return 0
    
    

# Функция записывает или обновляет mac у пользователя
def set_or_update_mac(vlan:str, mac:str, con:object) -> int:
    cursor = mysql_db.db.cursor()
    try:
        update_mac = f"UPDATE users SET icq_number = {mac} WHERE email = {vlan} LIMIT 1)
        cursor.execute(update_mac)
    except Exception as e:
        print (f"Не удалось обновить MAC-address пользователя в таблице users\n{e}")
        return 1
    
    return 0
        
    
