__author__ = 'jarrah'

# data base setting
USER_NAME = "root"
PASSWORD = "zxcvbnm,./"
HOST = "localhost"
DB_NAME = "API"


def get_db_conf():
    db = dict()
    db['name'] = USER_NAME
    db['pwd'] = PASSWORD
    db['host'] = HOST
    db['db_name'] = DB_NAME
    return db