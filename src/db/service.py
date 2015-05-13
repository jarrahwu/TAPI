__author__ = 'jarrah'
import torndb

funny_display_nums = 10

from src.web import conf


def get_connection():
    c = conf.get_db()
    con = torndb.Connection(host=c["host"], database=c["db_name"], password=c["pwd"], user=c["name"])
    return con


def get_funny():
    con = get_connection()
    items = con.query(query="select * from news_preview")
    con.close()
    return items


def get_funny_limit(_from):
    _to = _from + funny_display_nums
    print("from is %d to is %d" % (_from, _to))
    con = get_connection()
    items = con.query("select * from news_preview limit %(_from)s,%(_to)s", _from=_from, _to=_to)
    con.close()
    return items