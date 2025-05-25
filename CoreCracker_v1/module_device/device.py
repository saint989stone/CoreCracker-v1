import csv, json
import copy
import re

if __name__ == '__main__':
    from module_device.directory_device import template_type_device, template_filial, template_function, template_territory_exception, template_level_instance_zabbix
    from test_data_set import device_list
else:
    from module_device.directory_device import template_type_device, template_filial, template_function, template_territory_exception, template_level_instance_zabbix

def read_list_csv():
    device_list = []
    with open ('-', newline='', encoding='utf-8') as file:
        result = csv.reader(file)
        for row in result:
            data = row[0].split(';')
            print (data)
            device_dict = {
                'hostname' : data[0],
                'ip_address': data[1],
                'id_host_zabbix': data[2],
                'instance_zabbix': data[3],
                'type_device': data[4]
            }
            device_list.append(device_dict)
        print(device_list)
    return device_list

def read_zabbix_host_json(link_json: str, instance_zabbix: str)-> list:
    '''
    Функция разбора json полученного из Zabbix из выгрузки по соотвествующей Host Groups. На выходе получаем словарь со значениями следующих атрибутов: ip_address, hostname, instance_zabbix, type_device
    :param link_json: ссылка на json
    :param instance_zabbix: объект Zabbix из которого получена выгрузка
    :return device_list: Список подгтовленный список словарей по каждому устройству со всеми необходимыми атрибутами.
    '''
    device_list = []            #пустой список наполняемый словарями по каждому устройству
    keys = [
        'ip_address',           #список ключей для создания словаря
        'jump_host',
        'type_device', 
        'hostname', 
        'region',
        'filial',
        'function',
        'level',
        'territory',
        'group',
        'utc',
        'id_host_zabbix',
        'instance_zabbix',
    ]
    device_dict = dict.fromkeys(keys)           #создание словаря в соотвествии с ключами и значениями None
    with open(link_json, 'r', encoding='utf-8') as file:            #открываем json файл выгрузки из Zabbix Data Collections - Host Groups - Выбор Host Group - Export - JSON
        data = json.load(file)          #преобразуем json в словарь
        for host in data['zabbix_export']['hosts']:     #перебираем хосты из соотвествующих разделов словаря
            copy = device_dict.copy()           #делаем копию ранее созданного пустого словаря
            copy['ip_address'] = host['interfaces'][0]['ip']            #из соотвествущего раздела словаря вносим значение ip адреса
            copy['hostname'] = host['host']         #из соотвествущего раздела словаря вносим значение хостнейм
            copy['instance_zabbix'] = instance_zabbix           #вносим информацию об объекте Zabbix из которого получена выгрузка
            copy['type_device'] = None          #тип устройства будет определен позднее в цикле переборов соотвествующих шаблонов типам устройств
            for template in host['templates']:          #перебираем шаблоны устройств полученных из выгрузки
                if copy['type_device'] is not None: break           #если тип устройства определен и внесен в словарь останавливаем выполнение цикла
                for search in template_type_device:          #перебираем шаблоны с регулярными выражениями для определения типа устройства
                    result = re.search(search['pattern'], template['name'])         #поиск в шаблонах из выгрузки Zabbix выражений для определения типа устройства
                    if result is not None:      #по первому не пустому результату определяем тип устройства
                        copy['type_device'] = search['type_device']     #определяем значение типа устройства в словаре
                        #print(f'hostname - {host['host']} template - {template['name']} type_device - {search['type_device']}')
            device_list.append(copy)
    return device_list

def read_host_name (hostname: str ) -> dict:
    '''
    Функция определения признаков устройста по его hostname. На получаем hostname устройства. На выходе получаем словарь со значениями следующих атрибутов: region, filial, function, territory, group

    Args:
        hostname (str): хостнейм устройства

    Return:
      device_dict (dict): словарь содержащий значения принадлежности устройтва к региону, филиалу, функции, уровню, группе устройств, временному поясу
    '''
    keys = [
        'region',
        'filial',
        'function',
        'level',
        'territory',
        'group',
        'utc',       
    ]
    device_dict = dict.fromkeys(keys)           #создание словаря в соотвествии с ключами и значениями None
    for search in template_filial:          #цикл определения значения региона, филиала, utc
        if device_dict['filial'] is not None: break         #если признак филиала для устройства определен прерываем цикл
        for pattern in search['pattern']:           #перебираем шаблоны
            result = re.match(pattern, hostname)        #осуществляем поиск шаблона в строке хостнейм
            if result is not None:          #если результат поиска не пустой
                device_dict['region'] = search['region']        #запоняем атрибуты словаря устройства в соотвествии со значениями из шаблона
                device_dict['filial'] = search['filial']
                device_dict['utc'] = search['utc']
                break
    for search in template_function:        #цикл определения функциональной принадлежности и уровня устройства
        if device_dict['function'] is not None: break           #если функциональная принадлежность устройства определена прерываем цикл
        for pattern in search['pattern']:        #перебираем шаблоны
            result = re.search(pattern, hostname)        #осуществляем поиск шаблона в строке 
            if result is not None:           #если результат поиска не пустой    
                device_dict['function'] = search['function']        #запоняем атрибуты словаря устройства в соотвествии со значениями из 
                device_dict['level'] = search['level']
    for search in template_territory_exception:     #цикл определения территориальной принадлежности устройства в словаре исключений устройств
        if device_dict['territory'] is not None: break           #если функциональная принадлежность устройства определена прерываем цикл
        for pattern in search ['pattern']:          #перебираем шаблоны
            result = re.search(pattern, hostname)           #осуществляем поиск шаблона в строке хостнейм
            if result is not None:          #если результат поиска не пустой    
                device_dict['territory'] = search['territory']          #запоняем атрибуты словаря устройства в соотвествии со значениями из шаблона    
                device_dict['group'] = device_dict['territory'] + '-' + device_dict['function']
    if device_dict['territory'] is None:            #если устройство не найдено в списке исключений по территориальному признаку        
        result = re.search(r'[A-Z]{4,7}', hostname)         #осуществляем поиск строки в хостнейме состоящий из заглавных букв в количестве от 4 до 7, соотвествующей территориальному признаку
        device_dict['territory'] = result.group()
        device_dict['group'] = device_dict['territory'] + '-' + device_dict['function']
    return device_dict

def read_function_hostname (hostname: str)-> dict:
    """
    Функция получения по hostname устройства атрибутов принадлежности к функции, уровню сети и экземпляра zabbix к которому относится устройство, в соотвествии с уровнем сети
    
    Args:
        hostname (str): хостнейм устройства
    
    Return:
        device_dict (dict): словарь , содержащий атрибуты 'function', 'level', 'instance_zabbix'
    """
    keys = [
    'function',
    'level',
    'instance_zabbix'
    ]
    device_dict = dict.fromkeys(keys)           #создание словаря в соотвествии с ключами и значениями None
    for search in template_function:        #цикл определения функциональной принадлежности и уровня устройства
        if device_dict['function'] is not None: break           #если функциональная принадлежность устройства определена прерываем цикл
        for pattern in search['pattern']:        #перебираем шаблоны
            result = re.search(pattern, hostname)        #осуществляем поиск шаблона в строке 
            if result is not None:           #если результат поиска не пустой    
                device_dict['function'] = search['function']        #запоняем атрибуты словаря устройства в соотвествии со значениями из 
                device_dict['level'] = search['level']
    if device_dict['function']:
        for search in template_level_instance_zabbix:           #по принадлежности устройства к уровню определяем целевой интанс Zabbix
            if device_dict['instance_zabbix'] is not None: break
            for pattern in search['level']:         #перебираем список уровней соотвествующих интанс Zabbix
                if device_dict['level'] == pattern:
                    device_dict['instance_zabbix'] = search['instance_zabbix']
        print(f'Для устройства c hostname {hostname} найден шаблон в template_function')
    else:
        print(f'Для устройства c hostname {hostname} отсуствует шаблон в template_function')
    return device_dict


def check_data_device (device_dict: dict)-> bool:
    '''
    Функция проверки полноты данных значений в словаре по устройству

    Args:
        device_dict: словарь со значениями ключей определенных в функции read_zabbix_host_json
    Return:
        bool: Значение True если все значения заполнены, False если хотя бы одно значение отсуствует   
    '''
    result = True
    none_list = []
    for key in device_dict:
        if device_dict[key] is None:
            none_list.append(key)
            if result:
                result = False
    if none_list != []:
        print (f'Для устройства {device_dict['hostname']} не определены следующие атрибуты {none_list}')
    return result