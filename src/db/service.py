__author__ = 'jarrah'
import torndb

funny_display_nums = 10

from src.db import conf


def get_connection():
    c = conf.get_db_conf()
    con = torndb.Connection(host=c["host"], database=c["db_name"], password=c["pwd"], user=c["name"])
    return con


def get_rows_limit(table_name, from_index):
    to_index = from_index + funny_display_nums
    print("from is %d to is %d" % (from_index, to_index))
    con = get_connection()
    start_sql = "select * from %s " % table_name
    query_sql = start_sql + "limit %(_from)s,%(_to)s"
    items = con.query(query_sql, _from=from_index, _to=to_index)
    con.close()
    return items


def insert_into(table_name, rows=[], values=[]):
    start_sql = "insert into " + table_name
    params_sql = (None, '(')[len(rows) > 0]
    if params_sql is not None:
        for r in rows:
            params_sql += r
            params_sql += ','
        params_sql = params_sql[:-1]
        params_sql += ')'

    values_sql = (None, ' values (')[len(values) > 0]
    if values_sql is not None:
        for i in range(len(values)):
            values_sql += '%s'
            values_sql += ','

        values_sql = values_sql[:-1]
        values_sql += ')'

    if params_sql and values_sql is not None:
        query_sql = start_sql + params_sql + values_sql
        print('insert sql>>', query_sql)

    con = get_connection()
    insert_id = con.execute(query_sql, *values)
    con.close()
    print('inserted', insert_id)
    return insert_id


def get_funny_limit(_from):
    items = get_rows_limit(table_name="news_preview", from_index=_from)
    return items


# if __name__ == '__main__':
#     insert_into('user', ['phone', 'password'], ['18682212241', '123456'])