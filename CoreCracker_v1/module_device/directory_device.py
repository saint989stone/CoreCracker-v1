template_type_device = [
    {
        'pattern' : r'Juniper',
        'type_device' : 'juniper_junos'
    },
    {
        'pattern' : r'Huawei',
        'type_device' : 'huawei'
    },
    {
        'pattern' : r'Eltex',
        'type_device' : 'eltex'
    },
    {
        'pattern' : r'Nokia',
        'type_device' : 'nokia_sros'        
    },
    {
        'pattern' : r'ZTE',
        'type_device' : 'zte_zxros'        
    },
    {
        'pattern' : r'ECONAT',
        'type_device' : 'generic'
    }       
]

template_filial = [
    {
        'pattern' : [r'_'],
        'region' : '_',
        'filial' : '_',
        'utc' : 3
    }
]
template_function = [
    {
        'pattern' : [r'_'],
        'function' : '_',
        'level' : '_'
    }
]

template_level_instance_zabbix = [
    {
        'level' : ['_'],
        'instance_zabbix' : '_'
    }
]
template_territory_exception = [
    {
        'pattern' : [r'_'],
        'territory' : '_'
    }
]