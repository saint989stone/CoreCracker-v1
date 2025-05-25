models_templates = {
    'mpls' : [
        {
            'vendor' : 'all',
            'models' : [
                {
                    'regulars' : ['all'],
                    'functions' : [
                        {
                            'regulars' : ['all'],
                            'type' : {
                                'regulars' : 'all',
                                'templates' : {
                                    'Template Module Generic SNMPv2' : '10204' 
                                }
                            }
                        }                           
                    ]
                }
            ]
        },
        {
            'vendor' : r'huawei',
            'models' : [
                {
                    'regulars' : [r'ce68'],
                    'functions' : [
                        {
                            'regulars' : ['SSTK', 'SSW', 'RGS', 'PSW', 'SW', 'ASTK'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei CE68 ASW' : '10560',
                                        'Huawei Stack' : '27642',
                                    }
                                }
                            ]                    
                        }
                    ]
                }
            ]
        },
        {
            'vendor' : r'eltex',
            'models' : [
                {
                    'regulars' : [r'mes5200'],
                    'functions' : [
                        {
                            'regulars' : ['SSTK', 'ASTK', 'ASW', 'PSW', 'SSW'],
                            'type' : [
                                {
                                    'regulars' : 'all',
                                    'templates' : {
                                        'Template Eltex MES 53xx' : '14833'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },        
                {
                    'regulars' : [r'mes3348'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'all',
                                    'templates' : {
                                        'Template Eltex MES 3324 4.0.13' : '10592'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },   
            ]
        },
    ],
    'rspd' : [
       {
            'vendor' : 'all',
            'models' : [
                {
                    'regulars' : ['all'],
                    'functions' : [
                        {
                            'regulars' : ['all'],
                            'type' : [
                                {
                                    'regulars' : 'all',
                                    'templates' : {
                                        'Template Module Generic SNMPv2' : '10523' 
                                    }
                                }
                            ]
                        }                           
                    ]
                }
            ]
        },
        {
            'vendor' : r'huawei',
            'models' : [
                {
                    'regulars' : [r'cx600'],
                    'functions' : [
                        {
                            'regulars' : ['AR', 'DR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei CX600 v2' : '14932',
                                        'OSPF Huawei CX600 VRP ver.8' : '13783',
                                        'LLDP Huawei' : '10598'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei CX600 v2' : '14932',
                                        'ISIS Huawei CX600' : '15029',
                                        'LLDP Huawei' : '10598'
                                    }
                                }                               
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'netengine 8000 m8', r'ne8000'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei NetEngine 8000' : '13785',
                                        'OSPF Huawei NE only neibor' : '13784'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei NetEngine 8000' : '13785',
                                        'ISIS Huawei' : '14972'
                                    }
                                }                               
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r's53', r's63'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei S53XX ASW' : '10615',
                                        'OSPF Huawei S53xx VRP ver.8' : '15031'
                                    }
                                },                         
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r's93'],
                    'functions' : [
                        {
                            'regulars' : ['AR', 'ASBR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei S93XX AR' : '10525',
                                        'OSPF Huawei S93xx VRP ver.5' : '13786'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei S93XX AR' : '10525',
                                        'ISIS Huawei' : '14972'
                                    }                                    
                                }                         
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'ne40'],
                    'functions' : [
                        {
                            'regulars' : ['AR', 'DR', 'BPE'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei NE40' : '10602',
                                        'OSPF Huawei NE only neibor' : '13784'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei NE40' : '10602',
                                        'ISIS Huawei NE40E' : '15034'
                                    }                                    
                                }                         
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'ce68'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Huawei CE68' : '15015',
                                        'Huawei Stack' : '14082',
                                        'OSPF Huawei NE only neibor' : '13784'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei CE68' : '15015',
                                        'Huawei Stack' : '14082',
                                        'ISIS Huawei NE40E' : '15034'
                                    }                                    
                                }                         
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'atn9'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Huawei ATN9xx' : '15032',
                                        'ISIS Huawei NE40E' : '15034'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },         
            ]
        },
        {
            'vendor' : r'juniper',
            'models' : [
                {
                    'regulars' : [r'mx480', r'mx240', r'mx960', r'mx40', r'mx80', r'mx104'],
                    'functions' : [
                        {
                            'regulars' : ['AR', 'DR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Juniper AR' : '10560',
                                        'LACP Juniper' : '10596',
                                        'LLDP Juniper' : '10599',
                                        'Juniper Commit' : '14049',
                                        'Jiniper VPN' : '14050',
                                        'OSPF Public Template' : '13776'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Juniper AR' : '10560',
                                        'LACP Juniper' : '10596',
                                        'LLDP Juniper' : '10599',
                                        'Juniper Commit' : '14049',
                                        'Jiniper VPN' : '14050',
                                        'ISIS Juniper' : '13778'
                                    }
                                },                                                         
                            ]                    
                        },
                        {
                            'regulars' : ['BPE'],
                            'type' : [
                                {
                                    'regulars' : 'generic',
                                    'templates' : {
                                        'Juniper BPE' : '12793',
                                        'LACP Juniper' : '10596',
                                        'LLDP Juniper' : '10599',
                                        'Juniper Commit' : '14049',
                                        'Jiniper MPLS VRF' : '14051',
                                        'Jiniper VPN' : '14050'
                                    }
                                }                                                    
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'ex92', r'ex82'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Juniper EX v2' : '10560',
                                        'Juniper Commit' : '14049',
                                        'OSPF Public Template' : '13776'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Juniper EX v2' : '10560',
                                        'Juniper Commit' : '14049',
                                        'ISIS Juniper' : '13778'
                                    }
                                }                                                         
                            ]                    
                        }
                    ]
                },
                {
                    'regulars' : [r'acx', r'ex82'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Juniper ACX' : '15033',
                                        'OSPF Public Template' : '13776'
                                    }
                                },
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Juniper ACX' : '15033',
                                        'ISIS Juniper' : '13778'
                                    }
                                }                                                         
                            ]                    
                        }
                    ]
                }                                                                                
            ]
        },
        {
            'vendor' : r'eltex',
            'models' : [
                {
                    'regulars' : [r'mes5'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Template Eltex MES 53xx' : '14088'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },        
                {
                    'regulars' : [r'mes3'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'ospf',
                                    'templates' : {
                                        'Template Eltex MES 3324 4.0.13' : '10592'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },   
            ]
        },
        {
            'vendor' : r'nokia',
            'models' : [
                {
                    'regulars' : [r'7250'],
                    'functions' : [
                        {
                            'regulars' : ['AR'],
                            'type' : [
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Nokia AR 7250' : '10542',
                                        'LACP Nokia' : '10597',
                                        'LLDP Nokia' : '10600',
                                        'Optical Modules Nokia' : '12795',
                                        'ISIS Nokia' : '13775',
                                        'PIM Nokia' : '14001'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                },        
                {
                    'regulars' : [r'7750'],
                    'functions' : [
                        {
                            'regulars' : ['AR', 'DR'],
                            'type' : [
                                {
                                    'regulars' : 'isis',
                                    'templates' : {
                                        'Nokia AR 7750' : '12799',
                                        'LACP Nokia' : '10597',
                                        'LLDP Nokia' : '10600',
                                        'Optical Modules Nokia' : '12795',
                                        'ISIS Nokia' : '13775',
                                        'PIM Nokia' : '14001'
                                    }
                                }                         
                            ]                    
                        }
                    ]
                }   
            ]
        }
    ]
}
    