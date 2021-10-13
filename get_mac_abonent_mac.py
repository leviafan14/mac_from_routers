#!/usr/bin/env python
# -*- coding: utf_8 -*-

import re
from routers_auth_data import username, password, db_username, db_password, db_name, db_host
from sql_functions import connect_to_db, set_or_update_mac
from paramiko import SSHClient
from paramiko import AutoAddPolicy

# Список роутеров из которых будет извлекаться информация
routers=['192.168.100.1']
connection = connect_to_db(db_username, db_password, db_name, db_host)


# Функция получает MAC-адрес и интерфейс пользователя и количество записей в ARP таблице
def get_arp_data(host:str, username:str, password:str) -> int:
    mac_addresses = []
    users_vlan = []
    # Создаем объект подключения к роутеру
    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
    except Exception as e:
        print(f"Не удалось подключиться к роутеру {host}\n{e}")
        return 1

    # Получаем количество записей в таблице
    ssh.connect(host, port=22, username=username, password=password, look_for_keys=False)
    get_count = "put [ip arp print count-only]"
    ex_get_count = ssh.exec_command(get_count)[1].read()
    ssh.close()
    count=str(ex_get_count.decode("unicode-escape")[0:4]).strip()
    print(f"Количество записей: {count}")
    
    count_list = [c for c in count]
    print(count_list)
    
    # Получаем информацию в цикле по каждому подключенному устройству
    for x in range(0, int(count)):
        try:
            # Получаем MAC-адрес
            ssh.connect(host, port=22, username=username, password=password, look_for_keys=False)
            get_mac = "put [/ip arp get number=%s mac-address]"%(x)
            ex_get_mac = ssh.exec_command(get_mac)[1].read()
            ssh.close()
            
            # Получаем vlan
            ssh.connect(host, port=22, username=username, password=password)
            get_vlan = "put [/ip arp get number=%s interface]"%(x)
            ex_get_vlan = ssh.exec_command(get_vlan)[1].read()
            ssh.close()

            # Декодируем и обрезаем пробелы у полученных результатов команд
            mac = ex_get_mac.decode().strip()
            vlan = ex_get_vlan.decode().strip()
            
            # Проверяем результат на пустоту
            if mac !='' and and mac != "00:00:00:00:00:00" and vlan != '':
                if "no such elements" not in mac or vlan:
                    # Обрезаем 'vlan' перед номером влан'а, убираем пробелы
                    vlan.replace("vlan","").strip()
                    # Убираем из МАК адреса все символы крое цифр и латинских букв
                    mac = re.sub("[^A-Za-z0-9]","",mac)
                    # Вызываем функцию которая присваивает мак адрес по номеру влана
                    set_or_update_mac(vlan, mac, connection)
                    mac_addresses.append(mac)
                    users_vlan.append(vlan)
                else:
                    continue
            else:
                continue

            print(f"vlan:{vlan} mac:{mac} number:{x}")
        except Exception as e:
            print(f"Ошибка получения данных\n{e}")
            return 1
    return 0


if __name__ == "__main__":
    for host in routers:
        get_arp_data(host, username, password)

            
