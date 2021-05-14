# -*- coding: utf-8 -*-
import sys,os
CONFIG_FILE = "../config/miner_chia.cfg"

if sys.version_info.major == 2:   # Python 2
    import ConfigParser
else:                             # Python 3
    import configparser as ConfigParser

def get_database_setting():
    """
    通过外层配置文件获得数据库设置
    """
    config=ConfigParser.ConfigParser()

    if sys.version_info.major == 2:  # Python 2
        config.read('../config/miner_chia.cfg')
    else:  # Python 3
        config.read('../config/miner_chia.cfg', encoding="utf-8")

    host=config.get('db','host')
    database=config.get('db','database')
    dbuser=config.get('db','dbuser')
    dbpass=config.get('db','dbpass')

    return {
    "default": {
        "ENGINE": "django.db.backends.mysql", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": database,                       # Or path to database file if using sqlite3.
        "USER": dbuser,                             # Not used with sqlite3.
        "PASSWORD": dbpass,                         # Not used with sqlite3.
        "HOST": host,                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "3306",                             # Set to empty string for default. Not used with sqlite3.
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
        'OPTIONS':{
         "init_command":"SET sql_mode='STRICT_TRANS_TABLES'"
        }
        },
    }