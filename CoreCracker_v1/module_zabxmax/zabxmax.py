import requests, json
import time

timeout = 5
timeout_update = 30

class Zabx:
    '''
    Класс создания объекта подключения к Zabbix API и методов работы с ним

    Attributes:
        intance (str): Короткое обозначение instance Zabbix: mpls, rspd, east
        cont_zabbix_api (dict): Словарь с конфигурацией подключения к Zabbix API, содержащий username, password, instance 
    '''
    def __init__(self, instance: str, cont_zabbix_api: dict)-> None:
        '''
        Функция инициализации объекта Zabbix.

        Args:
            intance (str): Короткое обозначение instance Zabbix: mpls, rspd, east
            cont_zabbix_api (dict): Словарь с конфигурацией подключения к Zabbix API, содержащий username, password, список instance 
        '''
        self.username = cont_zabbix_api['username']
        self.password = cont_zabbix_api['password']
        self.instances = cont_zabbix_api['instance']
        #self.add_url = 'zabbix/api_jsonrpc.php'
        self.proxies = {
            'https': 'socks5://localhost:1080',
            'http' : 'socks5://localhost:1080'
        }
        self.count_request = 0

        if instance not in self.instances:
            print('Данный instance отсутствует')           #LOG
            self.url = None
        else:
            self.url = self.instances[instance]


    def get_api_key (self)-> bool:
        '''
        Фукция покдключения к Zabbix API. Получение ключа.
        '''
        result = False
        if self.url == None: result = False
        else:
            self.count_request += 1
            data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "username": self.username, 
                    "password": self.password    
                },
                "id": self.count_request
            }
        try:
            time.sleep(timeout)
            responce = requests.post(self.url, json=data, proxies=self.proxies)
            self.key = responce.json()['result']
            result = True
            print (f'Подключение к {self.url} прошло успешно. Получен ключ {self.key}')
        except Exception as error:
            self.key = None
            result = False
            print (f'Подключение к {self.url} прошло с ошибкой {error}')            #LOG
        return result

    def logout_api (self)-> bool:
        '''
        Функция отключения от Zabbix API
        '''
        result = bool
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": {},
            "auth": self.key,
            "id": self.count_request,
        }
        try:
            responce = requests.post(self.url, json=data, proxies=self.proxies)
        except Exception as error:
            result = False
            print (f'Отключение от {self.key} instance {self.url} прошло с ошибкой {error}')            #LOG   
        if result:
            result = True
            print (f'Отключение успешно от {self.key} instance {self.url} код ответа {responce}')            #LOG
        else:
            result = False
            print (f'Отключение неуспешно от {self.key} instance {self.url}')          #LOG
        return result
    
    def get_host_id (self, hostname: str)-> bool | str:
        '''
        Функция получения идентификатора host в Zabbix по строковому представлению hostname

        Args:
            hostname (str): строковое представление hostname
        Return:
            result (bool): результат выполнения
            host_id (int): идентификатор хоста в Zabbix
            status (int): статус оборудования в Zabbix, 0 - опрос включен возвращаем True, 1 - опрос выключен возвращаем False
        '''
        result = bool
        host_id = str
        status = bool
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host", "status"],
                "filter": {
                    "host": [hostname]
                }   
            },
            "auth": self.key,
            "id": self.count_request
        }
        try:
            time.sleep(timeout)
            responce = requests.post(self.url, json=data, proxies=self.proxies)
        except Exception as error:
            result = False
            print (f'Подключение c {self.key} instance {self.url} для получения host id прошло с ошибкой {error}')            #LOG   
        if responce.json()['result'] == []:           #проверка на возвращение пустого результата означает хост отсуствует в Zabbix
            host_id = False
            result = False
            status = False
            print (f'Host {hostname} не найден в Zabbix')           #LOG
        elif hostname == responce.json()['result'][0]['host']:      #проверка hostname полученного от Zabbix и запрашиваемого
            host_id = responce.json()['result'][0]['hostid']
            if responce.json()['result'][0]['status'] == 0:
                status = True
            else:
                status = False
            result = True
            print (f'Получение host id {host_id} для host {hostname} успешно')           #LOG
        else:           #во всех остальных случай
            host_id = False
            result = False
            print (f'Получение host id {result} для host {hostname} неуспешно')         #LOG
        return result, host_id, status
    
    def get_proxy(self):
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "proxy.get",
            "params": {
                "output": ["proxyid", "host"]
            },
            "auth": self.key,
            "id": self.count_request
        }
        response = requests.post(self.url, json=data, proxies=self.proxies)
        result = json.dumps(response.json(), indent=4)
        return result
    
    def get_host_ip (self, hostname)-> str:
        '''
        Функция получения ip адресса по hostname устойства
        Args:
            hostname (str): имя хоста
        Return:
            ip address (str): ip адрес интерфейс устройства
        '''
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["host"],
                "selectInterfaces": ["ip"],
                "filter": {
                   "host": [hostname]
                }
            },
            "auth": self.key,
            "id": self.count_request
        }      
        responce = requests.post(self.url, json=data, proxies=self.proxies)
        print(responce.json())

    def get_host_templates_id (self, host_id)-> dict:
        result = bool
        templates_dict = dict()
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [],
                "hostids": [host_id],
                "selectParentTemplates": ["name", "temlatedid"]
            },
        "auth": self.key,
        "id": self.count_request   
        }
        try:
            time.sleep(timeout)
            response = requests.post(self.url, json=data, proxies=self.proxies)
        except Exception as error:
            result = False
            print (f'Подключение c {self.key} instance {self.url} для получения id шаблонов устройства c id {host_id} прошло с ошибкой {error}')
        try:
            error = response.json()['error']
            result = False
            print(f'Для устройства с id {host_id} не получен список шаблонов. Ошибка {error}')     
        except Exception:
            result = True
            print (f'Для устройства с id {host_id} получен список шаблонов')
        if response.json()['result'] == []:     #проверка на возвращение пустого результата означает что хост отсуствует
            result = False
            templates_dict = False
            print (f'Устройство с id {host_id} не найдено в Zabbix') 
        else:
            result = True
            for template in response.json()['result'][0]['parentTemplates']:
                name = template['name']
                id = template['templateid']
                templates_dict[name] = id
        return result, templates_dict



    def create_host_snmpv2 (self, hostname: str, ip_address: str, community: str, proxy_id: str, groups_list:list, templates_list:list)-> bool:
        '''
        Функция добавления хоста в Zabbix
        Args:
            hostname (str): имя хоста устройства
            ip_address (str): ip адрес хоста
            community_macros (str): макрос указывающий на комьюнити SNMP
            proxy_id (str): id прокси через который опрашивается устройство
            groups_list (list): список id групп
            templates_list (list): список id шаблонов   
        '''
        result = bool
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": hostname,
                "interfaces": [
                    {
                        "type": 2,
                        "main": 1,
                        "useip": 1,
                        "ip": ip_address,
                        "port": "161",
                        "dns": "",
                        "details": {
                            "version": 2,  # SNMPv2
                            "community": "{$SNMP_COMMUNITY}",  # Community string
                            "bulk": 1,  # Использовать bulk requests
                            "max_repetitions": 10  # Оптимальное значение
                        }
                    }
                ],
                "groups": [{"groupid": group} for group in groups_list],
                "templates": [{"templateid": template} for template in templates_list],
                "proxy_hostid": proxy_id,
                "macros": [
                    {
                        "macro": "{$SNMP_COMMUNITY}",
                        "value": community,
                        "type": 1
                    }
                ]
            },
            "auth": self.key,
            "id": self.count_request
        }              
        try:
            time.sleep(timeout)
            response = requests.post(self.url, json=data, proxies=self.proxies)
        except Exception as error:
            result = False
            print (f'Подключение c {self.key} instance {self.url} для создание {hostname} прошло с ошибкой {error}')
        try:
            error = response.json()['error']
            result = False
            print(f'Устройство {hostname} не добавлено в {self.url}. Ошибка {error}')     
        except Exception:
            result = True
            print (f'Устройство {hostname} успешно добавлено в {self.url}')              
        return result

    def delete_host (self, host_id: str)-> bool:
        '''
        Функция удаления host в Zabbix по его host id

        Args:
            host_id (str): идентификатор host в Zabbix
        Return:
            result (bool): результат выполнения
        '''
        result = False
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [host_id],
            "auth":  self.key,
            "id": self.count_request
        }
        try:
            time.sleep(timeout_update)
            response = requests.post(self.url, json=data, proxies=self.proxies)                        
        except Exception as error:
            print (f'Подключение c {self.key} instance {self.url} для удаления host по host id {host_id} прошло с ошибкой {error}')            #LOG   
        if host_id == response.json()['result']['hostids'][0]:
            result = True
            print (f'Удаление host с id {host_id} прошло успешно')          #LOG
        else:
            result = False
            print (f'Удаление host с id {host_id} прошло неуспешно')            #LOG
        return result
    
    def delete_host_template (self, host_id:str, templates_tuple:tuple):
        """
        Функция удаления списка шаблонов с template id от хосту по его host id

        Args:
            host_id (str): идентификатор host в Zabbix
            template_list (list): список id 
        Return:
            result (bool): результат выполнения
        """        
        result = False
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.massupdate",
            "params": {
                "hosts": [{"hostid": host_id}],
                "templates_clear": [{"templateid": template} for template in templates_tuple]
            },
            "auth": self.key,
            "id": self.count_request
        }
        try:
            time.sleep(timeout_update)
            response = requests.post(self.url, json=data, proxies=self.proxies)
            response_json = response.json()
        except Exception as error:
            print (f'Подключение c {self.key} instance {self.url} для удаления шаблонов {templates_tuple} с host по host id {host_id} прошло с ошибкой {error}')
        try:
            if host_id == response.json()['result']['hostids'][0]:
                result = True
                print (f'Удаление шаблонов с id {templates_tuple} прошло успешно к host по host id {host_id}')          #LOG
            else:
                result = False
                print (f'Удаление шаблона с id {templates_tuple} прошло неуспешно к host по host id {host_id}')            #LOG
        except:
            result = False
            error_code = response_json['error']['code']
            error_message = response_json['error']['message']
            error_data = response_json['error']['data']
            print(f'Удаление шаблонов с id {templates_tuple} c host c id {host_id} прошло с кодом ошибки {error_code} сообщение {error_message} {error_data}')
        return result
    
    def add_host_template (self, host_id: str, templates_tuple: tuple)-> bool:
        """
        Функция добавления списка шаблонов с template id к хосту по его host id

        Args:
            host_id (str): идентификатор host в Zabbix
            template_tuple (tuple): список id 
        Return:
            result (bool): результат выполнения
        """
        result = False
        if self.key == None: result = False
        self.count_request += 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.massupdate",
            "params": {
                "hosts": [{"hostid": host_id}],
                "templates": [{"templateid": template} for template in templates_tuple]
            },
            "auth": self.key,
            "id": self.count_request
        }
        try:
            time.sleep(timeout_update)
            response = requests.post(self.url, json=data, proxies=self.proxies)
            response_json = response.json()
        except Exception as error:
            print (f'Подключение c {self.key} instance {self.url} для добавления шаблонов {templates_tuple} с host по host id {host_id} прошло с ошибкой {error}')
        try:
            if host_id == response.json()['result']['hostids'][0]:
                result = True
                print (f'Добавление шаблонов с id {templates_tuple} прошло успешно к host по host id {host_id}')          #LOG
            else:
                result = False
                print (f'Добавление шаблона с id {templates_tuple} прошло неуспешно к host по host id {host_id}')            #LOG
        except:
            result = False
            error_code = response_json['error']['code']
            error_message = response_json['error']['message']
            error_data = response_json['error']['data']
            print(f'Добавление шаблонов с id {templates_tuple} к host c id {host_id} прошло с кодом ошибки {error_code} сообщение {error_message} {error_data}')
        return result

    def switch_host_poll (self, host_id: str, status_bool: bool)-> bool:
        result = False
        if self.key == None: result = False
        self.count_request += 1
        if status_bool: status = 0
        else: status = 1
        data = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": host_id,
                "status": status            # 1 - отключен, 0 - включен
            },
            "auth": self.key,
            "id": self.count_request
        }
        try:
            time.sleep(timeout_update)
            response = requests.post(self.url, json=data, proxies=self.proxies)
            response_json = response.json()
        except Exception as error:
            print (f'Подключение c {self.key} instance {self.url} для изменения статуса host опроса на {status} по host id {host_id} прошло с ошибкой {error}')
        try:
            if host_id == response.json()['result']['hostids'][0]:
                result = True
                print (f'Изменения статуса host опроса на {status} по host id {host_id} прошло успешно')          #LOG
            else:
                result = False
                print (f'Изменения статуса host опроса на {status} по host id {host_id} прошло неуспешно')          #LOG
        except:
            result = False
            error_code = response_json['error']['code']
            error_message = response_json['error']['message']
            error_data = response_json['error']['data']
            print(f'Изменения статуса host опроса на {status} по host id {host_id} прошло с кодом ошибки {error_code} сообщение {error_message} {error_data}')
        return result                   