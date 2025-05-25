from module_connect.connect import deactivate_connect, deactivate_tunnel, connect_server, connect_tunnel, check_icmp, check_snmp
from module_device.device import read_function_hostname
from module_config.config import settings
from module_zabxmax.zabxmax import Zabx
from module_zabxmax.directory_proxies import proxies
import csv
import openpyxl
import time

tunnel_mpls, ip_address_mpls, port_mpls = connect_tunnel(settings.zabbix_server['instance']['mpls'], '127.0.0.1',settings.jump_as12389)
tunnel_rspd, ip_address_rspd, port_rspd = connect_tunnel(settings.zabbix_server['instance']['rspd'], '127.0.0.2', settings.jump_as12389)

zabx_mpls = connect_server(ip_address_mpls, port_mpls, settings.zabbix_server)
zabx_rspd = connect_server(ip_address_rspd, port_rspd, settings.zabbix_server)

zabx_api_mpls = Zabx('mpls', settings.zabbix_api)
zabx_api_mpls.get_api_key()

zabx_api_rspd = Zabx('rspd', settings.zabbix_api)
zabx_api_rspd.get_api_key()

oid_model = '1.3.6.1.2.1.1.1.0'
groups_mpls = ['544']           #Discovery_SURMS
groups_rspd = ['246']          
teplates_mpls = ['10204']           #Template Module Generic SNMPv2
teplates_rspd = ['10523']

book = openpyxl.load_workbook(filename='-')    #открываем фаил для чтения и записи
table = book.active  #получаем доступ к таблице на первом листе
count = 2
for row in table['D']:
    hostname = table['D' + str(count)].value.upper()
    ip_address = table['E' + str(count)].value
    print(count, hostname, ip_address)
    #Проверка hostname
    device_dict = read_function_hostname(hostname)
    if device_dict['function'] is not None:
        table['F' + str(count)].value = device_dict['level']
        table['G' + str(count)].value = device_dict['instance_zabbix']
        #Проверка MPLS
        if device_dict['instance_zabbix'] == 'mpls':
            #Проверка ICMP
            result_icmp = check_icmp(zabx_mpls, ip_address)
            table['H' + str(count)].value = str(result_icmp)

            #Проверка SNMP
            model, result_snmp = check_snmp(zabx_mpls, ip_address, settings.zabbix_api['communities']['general'], oid_model)
            table['I' + str(count)].value = str(result_snmp)
            if result_snmp:
                table['J' + str(count)].value = str(model)
                #Проверка наличия хоста в Zabbix
                result_host_id, host_id, status = zabx_api_mpls.get_host_id(hostname)
                if result_host_id:
                    table['K' + str(count)].value = str(result_host_id)
                else:
                    zabx_api_mpls.create_host_snmpv2(hostname, ip_address, settings.zabbix_api['communities']['general'], proxies['mpls']['-'], groups_mpls, teplates_mpls)
                    table['K' + str(count)].value = str('Create')
        
        #Проверка RSPD
        elif device_dict['instance_zabbix'] == 'rspd':
            #Проверка ICMP
            result_icmp = check_icmp(zabx_rspd, ip_address)
            table['H' + str(count)].value = str(result_icmp)

            #Проверка SNMP
            model, result_snmp = check_snmp(zabx_rspd, ip_address, settings.zabbix_api['communities']['general'], oid_model)
            table['I' + str(count)].value = str(result_snmp)
            if result_snmp:
                table['J' + str(count)].value = str(model)
                #Проверка наличия хоста в Zabbix
                result_host_id, host_id, status = zabx_api_rspd.get_host_id(hostname)
                if result_host_id:
                    table['K' + str(count)].value = str(result_host_id)
                else:
                    zabx_api_rspd.create_host_snmpv2(hostname, ip_address, settings.zabbix_api['communities']['general'], proxies['rspd']['-'], groups_rspd, teplates_rspd)
                    table['K' + str(count)].value = str('Create')

    book.save(filename='-')
    count += 1
    if count > 503:
         break

book.save(filename='-')
zabx_api_mpls.logout_api()
zabx_api_rspd.logout_api()
deactivate_connect(zabx_mpls)
deactivate_tunnel(tunnel_mpls)
deactivate_connect(zabx_rspd)
deactivate_tunnel(tunnel_rspd)