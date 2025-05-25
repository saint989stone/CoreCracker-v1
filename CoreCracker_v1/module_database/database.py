from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text, insert, select, Table, Column, DateTime, MetaData, ForeignKey, Integer, String, SmallInteger, String
from sqlalchemy.exc import OperationalError, SQLAlchemyError, ArgumentError, IntegrityError, DataError, ProgrammingError
from datetime import datetime

class Database:
    '''
    Класс создания подключения к базе данных и методов работы с ней

    Attributes:
        dsn (str): адрес для подключения к базе данных
    '''
    def __init__(self, dsn: str, db_name: str, ) -> None:
        '''
        Функция инициализации объекта базы данных

        Args:
            dsn (str): адрес для подключения к базе данных
        '''
        self.dsn = dsn          #адрес подключения к базе данных
        self.db_name = db_name          #имя базы данных
        self.engine = None          #объект подключения к базе данных
        self.metadata = MetaData()          #объект содержащий структуру базы данных
        self.define_tables()            #запуск функции инициализации базы данных

    def create_engine(self)-> bool:
        '''
        Функция создания движка базы данных и проверки подключения к базе данных
        '''
        result = False
        try:
            self.engine = create_engine(
            url=self.dsn,
            echo = True,            #Посылает SQL запросы в консоль
            pool_size=5,            #Количество соединений к БД
            max_overflow=10         #Количество дополнительных соединений к БД
            )
            print(f'Создание движка подключения к базе данных {self.db_name} прошло успешно')       #LOG
        except (OperationalError, SQLAlchemyError) as error:
            result = False
            print(f'При создании движка подключения к базе данных {self.db_name} произошла ошибка {error}')         #LOG
        try:
            with self.engine.connect() as connect_engine:
                responce = connect_engine.execute(text('SELECT VERSION()')).scalar()           #для проверки доступности базы данных делаем запрос на получение версии базы данных. Типы запросов .scalar() — если запрос возвращает одно значение; .fetchone() — получить первую строку в виде кортежа; .fetchall() - получить все строки
                if 'PostgreSQL' in responce:
                    result = True
                    print (f'Подключение к базе данных {self.db_name} {responce} прошло успешно')          #LOG
        except (OperationalError, SQLAlchemyError) as error:
            result = False
            print(f'Подключение к базе данных {self.db_name} прошло с ошибкой {error}')         #LOG
        return result
            
    def create_tables(self)-> bool:
        '''
        Функция создания таблиц базы данных
        '''
        result = False
        if self.engine:
            try:
                self.metadata.create_all(self.engine)
                result = True
            except SQLAlchemyError as error:
                result = False
                print(f'При создании таблицы возникла ошибка {error}')
        else:
            result = False
            print (f'Отсуствует движок базы данных. Необходимо вызвать функцию create_engine')
        return result
    
    def delete_tables(self)-> bool:
        '''
        Функция удаления таблиц базы данных
        '''
        result = False
        if self.engine:
            try:
                self.metadata.drop_all(self.engine)
                result =True
            except SQLAlchemyError as error:
                result = False
                print(f'При удалении таблицы возникла ошибка {error}')
        else:
            result = False
            print (f'Отсуствует движок базы данных. Необходимо вызвать функцию create_engine')
        return result
    
    def insert_data (self, table: str, data: list)-> bool:
        '''
        Функция вставки данных в определенную таблицу

        Args:
            table: имя таблицы для вставки
            data: список словарей с данными для вставки
        '''
        result = False
        if not data:
            result = False
            print (f'Пустой список данных для вставки в таблицу {table}')
        if not isinstance (data, list) or not all(isinstance(item, dict) for item in data):
            result = False
            print ('Данные для вставки в таблицу должны быть представлены списком словарей')
        try:
            if table not in self.dict_table:
                result = False
                print (f'Указаная таблица {table} отсутсвует в базе данных {self.db_name}')
            stat_table = self.dict_table[table]
        except Exception as error:
            result = False
            print (f'При попытке доступа к таблице {table} отсутсвует в базе данных {self.db_name}')
        try:
            with self.engine.begin() as connect_engine:         #автоматический commit/
                try:
                    statement = insert(stat_table).values(data)         #подоговка заявления на запись данных
                    connect_engine.execute(statement)
                except IntegrityError as error:
                    result =  False
                    print(f'Ошибка целостности данных: {error}')
                except DataError as error:
                    result = False 
                    print(f'Ошибка данных (неверный тип/формат): {error}')
                except OperationalError as error:
                    result = False 
                    print(f'Ошибка подключения к БД: {error}')
                except ProgrammingError as error:
                    result = False 
                    print (f'Ошибка в SQL запросе: {error}')
                except SQLAlchemyError as error:
                    result = False
                    print (f'Ошибка SQLAlchemy: {error}')
                except Exception as e:
                    result = False
                    print(f'Неожиданная ошибка: {error}')                
        except (OperationalError, SQLAlchemyError) as error:
            result = False
            print(f'Подключение к базе данных {self.db_name} прошло с ошибкой {error}')         #LOG        
        return result
    
    def select_where_data(self, table: str, columns_list: list=None, where_conditions_dict: dict=None):
        '''
        Функция по выборке данных из таблиц по атрибутам указанных в кортеже

            Args:
                table: таблица из которой производится выборка
                column: атрибуты значения которых будут в выборке
                value: атрибуты по значениям которых производится выборка
        '''
        result = False
        columns_unsupported_list = []
        columns_check_list = []
        result_list = []
        if columns_list:
            columns_check_list = columns_list
        if where_conditions_dict:
            where_conditions_list = list(where_conditions_dict.keys())
            columns_check_list = list(set(columns_list) | set(where_conditions_list))
        if table in list(self.dict_table.keys()):           #проверка запрашиваемой таблицы в списке таблиц базы данных
            for column in columns_check_list:           #проверка запрашиваемых столбцов/атрибутов в списке столбцов базы данных
                check = column in list(self.dict_table_column[table].keys())            #
                if check == False:       #если атрибут отсутствует в списке столбцов базы даннных
                    columns_unsupported_list.append(column)         #добавляем атрибут в список неподдерживаемых атрибутов
            if not columns_unsupported_list:        #если список неподдерживаемых атрибутов пустой, продолжаем выполнение программы
                if columns_list is None:            #если список запрашиваемых атрибутов пустой  
                        selected_columns = [self.dict_table[table]]         #выбираем все атрибуты 
                else:           #если список запрашиваемых атрибутов непустой 
                    selected_columns = [self.dict_table_column[table][column] for column in columns_list]           #формируем список запрашиваемых атрибутов.    
                
                statement = select(*selected_columns)           #создаем базовое заявления к базе данных

                if where_conditions_dict:           #если список условий where не пустой, добавляем условия where к запросу
                    for column, value in where_conditions_dict.items():
                        statement = statement.where(self.dict_table_column[table][column] == value)         #формируем список условий
                try:
                    with self.engine.begin() as connect_engine:         #автоматический commit/rollback
                        try:
                            responce = connect_engine.execute(statement).fetchall()         #отправляем заявления к базе даннх на получение всех значений метод fetchall()
                            # Форимрование списка словарей, где каждый словарь это строка, а значение ключа столбец
                            if columns_list is None:            #если аргумент функции списка атрибутов не пустой формируем словарь на его основе. порядковый номер значения в responce, соотвествует номеру в column_list  #если атрибуты для выгрузки не указаны, берем все из таблицы
                                columns_list = list(self.dict_table_column[table].keys())
                            for row in responce:
                                temp_dict = {}
                                for i in range(len(columns_list)):
                                    temp_dict.update({columns_list[i]: row[i]})
                                result_list.append(temp_dict)
                                result = True
                        except Exception as error:
                            print (f'Выборка данных {filter} из таблицы {table} прошла с ошибкой {error}')
                except (OperationalError, SQLAlchemyError) as error:
                    print(f'Подключение к базе данных {self.db_name} прошло с ошибкой {error}')         #LOG           
            else:
                print(f'Атрибуты {columns_unsupported_list} не найдены в списке атрибутов таблицы {table}')         #LOG
        else:
            print(f'Таблица {table} отсуствует в списке таблиц базы данных')            #LOG

        return result, result_list
    
    def select_where_data_test(self, table: str, column: list, value: dict=None)-> dict:
        '''
        Функция по выборке данных из таблиц по атрибутам указанных в кортеже

            Args:
                table: таблица из которой производится выборка
                column: атрибуты значения которых будут в выборке
                value: атрибуты по значениям которых производится выборка
        '''
        result = False
        try:
            if table not in self.dict_table:
                result = False
                print (f'Указаная таблица {table} отсутсвует в базе данных {self.db_name}')
            stat_table = self.dict_table[table]
        except Exception as error:
            result = False
            print (f'При попытке доступа к таблице {table} отсутсвует в базе данных {self.db_name}')
        try:
            with self.engine.begin() as connect_engine:         #автоматический commit/rollback
                try:
                    statement = select(
                        stat_table.columns.hostname,
                        stat_table.columns.type_device
                        ).where(
                            stat_table.columns.count_unvail == None
                            )     #подоговка заявления на запись данных
                    responce = connect_engine.execute(statement).fetchall()
                    for row in responce:
                        print(row)
                except Exception as error:
                    print (f'Выборка данных {filter} из таблицы {table} прошла с ошибкой {error}')
        except (OperationalError, SQLAlchemyError) as error:
            result = False
            print(f'Подключение к базе данных {self.db_name} прошло с ошибкой {error}')         #LOG        
        return result

    def insert_data_device(self):
        with self.engine.connect() as connect:
            stmt = insert(self.table_device).values(                [
                    {"_": "_", "_": "_"},
                ]
            )
            connect.execute(stmt)
            connect.commit()


    def define_tables(self):
        '''
        Функция создания структуры базы данных
        '''
        result = False
        try:
            if 'device' not in self.metadata.tables:            #проверка содержания в объекте содержащей структуру базы данных таблицы
                self.table_device = Table(
                    'device',
                    self.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('ip_address', String(45), unique=True, nullable=False),
                    Column('jump_host', String(20), nullable=False),
                    Column('type_device', String(20), nullable=False),
                    Column('hostname', String(20), unique=True, nullable=False),
                    Column('region', String(20), nullable=False),
                    Column('filial', String(20), nullable=False),
                    Column('function', String(20), nullable=False),
                    Column('level', String(20), nullable=False),
                    Column('territory', String(20), nullable=False),
                    Column('group', String(20), nullable=False),
                    Column('utc', SmallInteger, nullable=False),
                    Column('id_host_zabbix', SmallInteger, nullable=False),
                    Column('instance_zabbix', String(20), nullable=False),
                    Column('count_ar', SmallInteger),
                    Column('count_unvail', SmallInteger),
                    Column('date_time', DateTime, default=datetime.utcnow)
                )
        except ArgumentError as error:
            result = False
            print (f'В определении таблицы device произошла ошибка {error}')
        except Exception as error:
            result = False
            print (f'При создании таблицы device произошла ошибка {error}')

        try:
            if 'physical_interface' not in self.metadata.tables:
                self.table_physical_interface = Table(
                    'physical_interface',
                    self.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('interface_a', String),
                    Column('interface_b', String),
                    Column('id_interface_b', Integer),
                    Column('id_host_a', Integer, ForeignKey('device.id', ondelete='CASCADE'))
                )
        except ArgumentError as error:
            result = False
            print (f'В определении таблицы physical_interface произошла ошибка {error}')
        except Exception as error:
            result = False
            print (f'При создании таблицы physical_interface произошла ошибка {error}')  

        self.dict_table = {
            'device': self.table_device,
            'physical_interface': self.table_physical_interface
        }
        self.dict_table_column = {
            'device': {
                'id': self.table_device.columns.id,
                'ip_address': self.table_device.columns.ip_address,
                'jump_host': self.table_device.columns.jump_host,
                'type_device': self.table_device.columns.type_device,
                'hostname': self.table_device.columns.hostname,
                'region': self.table_device.columns.region,
                'count_unvail': self.table_device.columns.count_unvail,
                'filial': self.table_device.columns.filial,
                'function': self.table_device.columns.function,
                'level': self.table_device.columns.level,
                'territory': self.table_device.columns.territory,
                'group': self.table_device.columns.group,
                'utc': self.table_device.columns.utc,
                'id_host_zabbix': self.table_device.columns.id_host_zabbix,
                'instance_zabbix': self.table_device.columns.instance_zabbix,
                'count_ar': self.table_device.columns.count_ar,
                'count_unvail': self.table_device.columns.count_unvail,
                'date_time': self.table_device.columns.date_time
            }
        }    