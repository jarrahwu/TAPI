__author__ = 'jarrah'
# coding: utf-8
import torndb

MAX_ROWS = 5

from src.db import conf


def get_connection():
    c = conf.get_db_conf()
    con = torndb.Connection(host=c["host"], database=c["db_name"], password=c["pwd"], user=c["name"])
    return con


def get_rows_limit(table_name, from_index):
    to_index = from_index + MAX_ROWS
    print("from is %d to is %d" % (from_index, to_index))
    con = get_connection()
    start_sql = "select * from %s " % table_name
    query_sql = start_sql + "limit %(_from)s,%(_to)s"
    items = con.query(query_sql, _from=from_index, _to=to_index)
    con.close()
    return items


def get_rows_limit_order(table_name, from_index, order_claus):
    to_index = from_index + MAX_ROWS
    print("from is %d to is %d" % (from_index, to_index))
    con = get_connection()
    start_sql = "select * from %s " % table_name
    query_sql = start_sql + order_claus + " limit %(_from)s,%(_to)s"
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
    # print('inserted', insert_id)
    return insert_id


def get_single_row_as_dict(table, value, key='_id'):
    con = get_connection()
    sql = "select * FROM %s WHERE %s=" % (table, key)
    sql += "%s"
    row = con.query(sql, value)
    con.close()
    print('get_single_row_as_dict')
    print(row)
    if len(row):
        return row[0]
    else:
        return None


'''------------------------'''


def get_funny_limit(_from):
    items = get_rows_limit(table_name="news_preview", from_index=_from)
    return items


'''获取moment的信息 倒序排列 limit限制'''


def get_moment_limit(_from):
    items = get_rows_limit_order(table_name="moment", from_index=_from, order_claus="order by _id desc")
    return items


'''根据用户id获取用户信息'''


def get_user_with(user_id):
    user = get_single_row_as_dict('user', user_id)
    if user:
        _hide_columns = ['_id', 'external_app_id', 'reg_time']
        filter_columns(user, *_hide_columns)
    return user


'''过滤不需要显示的字段'''


def filter_columns(row, *columns):
    row = dict(row)
    for c in columns:
        print("columns del name", c)
        del row[c]
