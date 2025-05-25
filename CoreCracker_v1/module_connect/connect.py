"""
Модуль сетевого взаимодействия с устройствами
"""

from netmiko import ConnectHandler, NetmikoBaseException, redispatch
import time, re
from module_connect.regular_connect import devc_type_list
from sshtunnel import open_tunnel, BaseSSHTunnelForwarderError

def connect_tunnel(ip_address_device: str, ip_address_local: str, jumpParm: dict)-> object:
    '''
    Функция организациии ssh туннеля, через jump host к устройству

    Args:
        ip_address_device (str): ip адрес устройства к которому подключаемся
        ip_address_local (str): локальный ip адрес, через который осуществляется подключение
        jumpParm (dict): словарь с настройками подключения к jumphost
    Return:
        ip_address_local (str): локальный ip адрес через который поднят тунель к устройству
        port_local (str): локальный порт через который поднят тунель к устройству
    '''
    port_local = 22
    tunnel = open_tunnel (
        (jumpParm['ip'], 22),
        ssh_username = jumpParm['username'],
        ssh_password = jumpParm['password'],
        remote_bind_addresses = [
            (ip_address_device, 22), 
            (ip_address_device, 23)
            ],
        local_bind_address = (ip_address_local, port_local)
    )
    try:
        tunnel.start()
        print(f'Создание туннеля к устройству с ip адресом {ip_address_device} прошло успешно')
    except BaseSSHTunnelForwarderError as error:
        tunnel = None
        print(f'Создание туннеля к устройству с ip адресом {ip_address_device} прошло с ошибкой: {error}')
    return tunnel, ip_address_local, port_local

def connect_jump(jumpParm):
    """
    Функция подключения к jumphost получает словарь с параметрами подключения к jumphost
    :param jumpParm: параметры подключения к jumphost
    :return jump_ssh: объект подключения через jumphost, в случае ошибки подключения возвращается None
    """
    try:
        jump_ssh = ConnectHandler(**jumpParm)  # устанавливаем подключение к jumphost
        return jump_ssh
    except NetmikoBaseException as error:  # если подключение с ошибкой возвращаем None
        print(f'Подключение к JumpHost {jumpParm['ip']} прошло с ошибкой {error}')  # LOG
        return None
    except Exception as error:
        print(f'Подключение к JumpHost {jumpParm['ip']} прошло с ошибкой {error}')  # LOG
        return None

def connect_server(ip_address: str, port: str, server_parm: dict)-> object:
    """
    Функция подключения к Zabbix серверу

    Args:
        ip_address (str): строковое представление локального ip адреса туннеля 
        port (str): строковое представление локального порта туннеля
        zabbix_server_parm (dict): словарь подключения к zabbix серверу
    """
    zabbix_parm = {
        'device_type': 'linux',
        'host': ip_address,
        'port': port,
        'username': server_parm['username'],
        'use_keys': True,
        'key_file': server_parm['key_file'],
        'timeout': 60
    }
    try:
        server = ConnectHandler(**zabbix_parm)
        return server
    except NetmikoBaseException as error:  # если подключение с ошибкой возвращаем None
        print(f'Подключение к JumpHost {zabbix_parm['host']} прошло с ошибкой {error}')  # LOG
        return None
    except Exception as error:
        print(f'Подключение к JumpHost {zabbix_parm['host']} прошло с ошибкой {error}')  # LOG
        return None
    
def connect_device(ip, devc_type, conn_parm_devc, cont_parm_jump):
    """
    :param ip: ip адрес устройства тип которого определяем
    :param devc_type: тип устройства netmiko
    :param conn_parm_devc: словарь содержащий данные для авторизации на устройстве
    :param cont_parm_jump: словарь содержащий данные для авторизации на jumphost
    :return devs_ssh: объект подключения по SSH
    """
    devc_ssh = connect_jump(cont_parm_jump)  # получаем объект подключения к jumphost
    if devc_ssh is not None:
        cmd = f'ssh {conn_parm_devc['username']}@{ip}\n'  # формируем строку подключения: ssh ug.pantyuhov_a@84.42.48.207
        devc_ssh.write_channel(cmd)  # отправляем сформированную строку в канал
        time.sleep(3)  # задержка
        outp = devc_ssh.read_channel()  # получаем ответ от устройства
        if 'assword' or 'authenticity'in outp:  # проверяем ответ на содержание приглашения для ввода пароля, если строка приглашения отсутсвует считаем что устройство недоступно
            devc_ssh.write_channel(f'{conn_parm_devc['password']}\n')  # отправляем пароль на устройство
            try:
                redispatch(devc_ssh, device_type=devc_type)  # сменяем тип устройства с указанного в подключении к jumphost на тип указанный в вызове функции
            except (Exception, NetmikoBaseException) as error:  # обработчик ошибок
                print(error)
                deactivate_connect(devc_ssh)
            return devc_ssh
        else:
            print(f'Подключение к устройству с {ip} отсутсвует')  # LOG
            return None
    else:
        return None  # возвращаем None если подключение к JumpHost отсутсвует


def identify_device_type(ip, cont_parm_devc, cont_parm_jump):
    """
    Функция подключения к устройству и определения его типа
    :param ip: ip адрес устройства тип которого определяем
    :param cont_parm_devc: словарь содержащий данные для авторизации на устройстве
    :param cont_parm_jump: словарь содержащий данные для авторизации на jumphost
    :return devc_type: тип устройства netmiko
    """
    for devc in devc_type_list:  # цикл перебора списка словарей с проверкой типа устройств
        devc_ssh = connect_device(ip, devc['device_type'], cont_parm_devc, cont_parm_jump)  # вызов функции подлючения к устройству с указанными параметрами подключения
        if devc_ssh:            #проверка на пустой объект ssh
            try:
                outp = devc_ssh.send_command(
                    devc['cmd'])  # ввод команды типа show version для определения типа устройства
            except (Exception, NetmikoBaseException) as error:
                print(error)
                deactivate_connect(devc_ssh)
                continue
            for patn in devc['patterns']:  # цикл перебора с проверкой регулярных выражений соответствующих производителю устройства
                print(patn)
                patn_serh = re.search(patn, outp)  # поиск в строке соотвествующее регулярное выражение типу устройства из списка словарей типов устройств
                if patn_serh is not None:  # если найденная строка не пустая тогда определяем что тип устройcтва определен верно
                    deactivate_connect(devc_ssh)
                    return devc['device_type']  # возвращаем определенный тип устройства
                
def deactivate_tunnel(tunnel)-> bool:
    """
    Функция отключение туннеля
    """
    result = False
    tunnel.stop()
    if tunnel.is_active:
        try:
            time.sleep(3) 
            tunnel.close()
            result = True
            print('Отключение туннеля прошло успешно') 
        except:
            print('Отключение туннеля прошло c ошибкой')
    return result


def deactivate_connect(cont) -> bool:
    """
    Функция отключения соединения с устройством

    Args:
        cont(object): объект netmiko соединения с устройством
    """
    result = False
    try:
        time.sleep(3)
        cont.disconnect()
        result = True
        print(f'Успешное отключение по SSH от устройства {cont}')  # LOG      
    except:
        result = False
        print(f'Неуспешное отключение по SSH от устройства {cont}')  # LOG
    return result

def check_icmp(connect, ip_address: str) -> bool:
    """
    Функция проверки доступности устройства по ICMP

    Args:
        connect (object): обьект netmiko соединения с устройством
        ip_address (str): строковое представление ip адрес устройства
    """
    result = False
    cmd = f'ping -c 4 {ip_address}\n'
    outp = connect.send_command(cmd, read_timeout=30)
    time.sleep(20)
    if '0% packet loss' in outp:
        print(f'Устройство c {ip_address} доступно по ICMP')
        result = True
    else:
        print(f'Устройство c {ip_address} недоступно по ICMP')
        result = False
    return result

def check_snmp(connect, ip_address, community, oid):
    """
    Функция проверки доступности устройства по SNMP

    Args:
        connect (object): обьект netmiko соединения с устройством
        ip_address (str): строковое представление ip адрес устройства
        community (str): комьюнити snmp
        oid (str): oid запрашиваемой метрики
    """
    result = False
    cmd = f'snmpwalk -v2c -c {community} {ip_address} {oid}\n'
    outp = connect.send_command(cmd, read_timeout=30)
    time.sleep(20)
    if 'Timeout: No Response' in outp:
        outp = None
        result = False
        print(f'Устройство c {ip_address} недоступно по SNMP')
    else:
        result = True
        print(f'Устройство c {ip_address} доступно по SNMP')
    return result, outp