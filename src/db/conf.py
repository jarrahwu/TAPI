__author__ = 'jarrah'

# data base setting
USER_NAME = "bluetest"
PASSWORD = "123456"
HOST = "10.10.81.163"
DB_NAME = "BlueTest"


def get_db_conf():
    db = dict()
    db['name'] = USER_NAME
    db['pwd'] = PASSWORD
    db['host'] = HOST
    db['db_name'] = DB_NAME
    return db
