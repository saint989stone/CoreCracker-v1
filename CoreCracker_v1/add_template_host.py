from module_connect.connect import deactivate_connect, deactivate_tunnel, connect_server, connect_tunnel, check_icmp, check_snmp
from module_config.config import settings
from module_zabxmax.zabxmax import Zabx
from module_device.directory_models_templates import models_templates
from module_device.directory_oids import oids
from module_device.device import read_function_hostname
import openpyxl
import re

tunnel_rspd, ip_address_rspd, port_rspd = connect_tunnel(settings.zabbix_server['instance']['rspd'], '127.0.0.2', settings.jump_as12389)
zabx_rspd = connect_server(ip_address_rspd, port_rspd, settings.zabbix_server)

oid_model = oids['generic']['device description']
oid_isis = oids['generic']['isis_ip']

zabx_api_rspd = Zabx('rspd', settings.zabbix_api)
zabx_api_rspd.get_api_key()



book = openpyxl.load_workbook(filename='_')
table = book.active
count = 2
for row in table['A']:
    hostname = table['A' + str(count)].value
    ip_address = table['B' + str(count)].value
    print (count, hostname, ip_address)
    result_snmp, descr = check_snmp(zabx_rspd, str(ip_address), settings.zabbix_api['communities']['general'], oid_model)
    table['C' + str(count)] = result_snmp
    if result_snmp:
        table['D' + str(count)] = descr
        model_lower = descr.lower()
        for vendor in models_templates['rspd']:
            regular_vendor = vendor['vendor']
            if vendor['vendor'] == 'all': continue
            result_search_vendor = re.search(regular_vendor, model_lower)
            if result_search_vendor:
                for model in vendor['models']:
                    for regular_model in model['regulars']:
                        result_search_model = re.search(regular_model, model_lower)
                        if result_search_model:
                            result_read_hostname = read_function_hostname(hostname)
                            for function in model['functions']:
                                #print(result_read_hostname['function'])
                                if result_read_hostname['function'] in function['regulars']:
                                    table['E' + str(count)] = result_read_hostname['function']
                                    result_snmp, isis_status = check_snmp(zabx_rspd, str(ip_address), settings.zabbix_api['communities']['general'], oid_isis)
                                    if 'No Such Instance' in isis_status:       #ospf
                                        type_template = 'ospf'
                                    else:
                                        type_template = 'isis'
                                    table['F' + str(count)] = type_template
                                    for type in function['type']:
                                        if type['regulars'] == type_template:
                                            standart_template = type['templates']
                                            table['G' + str(count)] = str(standart_template)
                                    result_host_id, host_id, status = zabx_api_rspd.get_host_id(hostname)
                                    if result_host_id:
                                        result_host_templates_id, host_template = zabx_api_rspd.get_host_templates_id(host_id)
                                        if result_host_templates_id:
                                            diff_host = set(host_template.values()) - set(standart_template.values()) #удалить
                                            print(diff_host)
                                            zabx_api_rspd.switch_host_poll(host_id, False)
                                            zabx_api_rspd.delete_host_template(host_id, diff_host)
                                            zabx_api_rspd.add_host_template(host_id, set(standart_template.values()))
    book.save(filename='_')
    count += 1
    if count > 128:
        break