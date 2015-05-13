__author__ = 'jarrah'
from src.web import constant


def get_db():
    db = dict()
    db['name'] = constant.name
    db['pwd'] = constant.password
    db['host'] = constant.host
    db['db_name'] = constant.db_name
    return db