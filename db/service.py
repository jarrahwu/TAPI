__author__ = 'jarrah'
import torndb

from web import conf


def get_connection():
    c = conf.get_db()
    con = torndb.Connection(host=c["host"], database=c["db_name"], password=c["pwd"], user=c["name"])
    return con


def get_funny():
    con = get_connection()
    items = con.query(query="select * from news_preview")
    con.close()
    return items