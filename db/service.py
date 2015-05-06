__author__ = 'jarrah'
import torndb
from web import conf

def get_news_connection():
    c = conf.get_db()
    con = torndb.Connection(host=c["host"], database=c["db_name"], password=c["pwd"], user=c["user"])
    return con

def get_news():
    con = get_news_connection()
    items = con.query(query="select * from news_preview")
    con.close()
    return items