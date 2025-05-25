from module_device.device import read_zabbix_host_json, read_host_name, check_data_device
from module_connect.connect import connect_device, deactivate_connect
from module_config.config import settings 
from module_zabxmax.zabxmax import Zabx
from module_database.database import Database


jump_host_dict = {
    'as12389': settings.cont_parm_jump_as12389
}

device_list = read_zabbix_host_json(link_json='_', instance_zabbix='_')       #Этап получения значений атрибутов ip_address, hostname, instance_zabbix, type_device из выгрузки
for device_dict in device_list:         #Перебираем словари устройств
    for jump_host_key in jump_host_dict:        #Этап определяния jump host подключения перебираем jump host
        device_connect = connect_device(         #Подключение к устройству. Проверка доступности 
            device_dict['ip_address'], 
            device_dict['type_device'], 
            settings.cont_parm_devc_as12389,
            jump_host_dict[jump_host_key]
            )
        if device_connect != None:          #Если проверка доступности прошла
            deactivate_connect(device_connect)           #Отключение от устройства
            device_dict['jump_host'] = jump_host_key            #записываем в словарь соотвествующее имя jump host
        else:
            deactivate_connect(device_connect)           #Отключение от устройства
    hostname_dict = read_host_name(device_dict['hostname'])     #Этап получения по каждому устройству словаря со значениями атрибутов region, filial, function, territory, group
    device_dict.update(hostname_dict)       #Обновляем указанные выше значения в итоговом словаре в соотвествии с полученными данными
    zabx = Zabx('_', settings.cont_zabbix_api)           #Этап получения host id в Zabbix
    result = zabx.get_api_key()
    if result:
        result, host_id, status = zabx.get_host_id(device_dict['hostname'])
        if result and status:          #если функция получения ключа возражает True и статус устройства равен 0, то есть оборудование в Zabbix включено
            device_dict['id_host_zabbix'] = host_id
zabx.logout_api()

for device_dict in device_list:            #Проверка на полноту данных по устройствам, устройство удаляется из списка если у него хотя бы одно значение ключа равно None
    if result == False:
        device_list.remove(device_dict)          #удаляем словарь с пустыми значениями из списка

db = Database(*settings.db_url_pg_psycorg)          #Этап записи очищенного списка словарей по устройствам
db.create_engine()
db.insert_data('device', device_list)
