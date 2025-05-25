from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JH_AS12389_IP: str
    JH_AS12389_USER: str
    JH_AS12389_PASS: str
    JH_AS12389_AUTO: bool
    DV_AS12389_USER: str
    DV_AS12389_PASS: str
    ZABX_API_USER: str
    ZABX_API_PASS: str
    ZABX_API_COMMUNITY_GENERAL: str
    ZABX_SERVER_USER: str

    @property
    def jump_as12389(self):
        parm = {
            'device_type': 'terminal_server',
            'ip': self.JH_AS12389_IP,
            'username': self.JH_AS12389_USER,
            'password': self.JH_AS12389_PASS,
            'allow_auto_change': self.JH_AS12389_AUTO
        }
        return parm
    
    @property
    def devc_as12389(self):
        parm = {
            'username': self.DV_AS12389_USER,
            'password': self.DV_AS12389_PASS
        }
        return parm

    @property
    def zabbix_api(self):
        parm = {
            'username': self.ZABX_API_USER,
            'password': self.ZABX_API_PASS,
            'communities' : {
                'general' : self.ZABX_API_COMMUNITY_GENERAL
            },
            'instance': {
                'mpls': '_',
                'rspd': '-',
                'east': '_'
            }
        }
        return parm

    @property
    def zabbix_server(self):
        parm = {
            'username': self.ZABX_SERVER_USER,
            'key_file': '_',
            'instance': {
                'mpls': '_',
                'rspd': '_'
            }
        }
        return parm

    @property
    def db_url_sqlite(self):
        return 'sqlite:///c:/projects/CoreCracker/db/app.db'

    @property
    def db_url_pg_psycorg(self):
        #DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}', self.DB_NAME
    #
    model_config = SettingsConfigDict(env_file='c:/projects/CoreCracker_V1/.env')

settings = Settings()