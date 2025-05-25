devc_type_list = [
    {
        "device_type": "juniper_junos",
        "cmd": "show version",
        "patterns": [r"JUNOS Software Release", r"JUNOS .+ Software", r"JUNOS OS Kernel", r"JUNOS Base Version"]
    },
    {
        "device_type": "huawei",
        "cmd": "display version",
        "patterns": [r"HUAWEI", r"Huawei Technologies", r"Huawei Versatile Routing Platform Software"]
    },
    {
        "device_type": "nokia_sros",
        "cmd": "show version",
        "patterns": [r"Nokia", r"Alcatel"]
    },
    {
        "device_type": "zte_zxros",
        "cmd": "show version",
        "patterns": [r"ZTE\s+Corporation"]
    },
    {
        "device_type": "eltex",
        "cmd": "show version",
        "patterns": [r"Eltex"]
    },
    {
        "device_type": "eltex",
        "cmd": "show system",
        "patterns": [r"System\sDescription\s*:\s+MES\-*\d+", r"\d+\s+MES\-*\d+"]
    },
    {
        "device_type": "eltex",
        "cmd": "show system information",
        "patterns": [r"System\sDescription\s*:\s+MES\-*\d+"]
    },
    {
        "device_type": "cisco_xe",
        "cmd": "show version",
        "patterns": [r"Cisco IOS.XE Software"]
    },
    {
        "device_type": "cisco_xr",
        "cmd": "show version",
        "patterns": [r"Cisco IOS.XR",r"ASR9K Series"]
    },
    {
        "device_type": "cisco_nxos",
        "cmd": "show version",
        "patterns": [r"Cisco Nexus Operating System", r"NX-OS"]
    },
    {
        "device_type": "cisco_ios",
        "cmd": "show version",
        "patterns": [r"Cisco IOS Software", r"Cisco Internetwork Operating System Software"]
    },
    {
        "device_type": "cisco_ios",
        "cmd": "show version",
        "patterns": [r"EcoNAT", r"Ecotelecom", r"RDP\.RU", r"QTECH"]
    },
    {
        "device_type": "generic",
        "cmd": "show version",
        "search_patterns": [r"EcoNAT", r"Ecotelecom", r"RDP\.RU", r"QTECH"]
    }
]