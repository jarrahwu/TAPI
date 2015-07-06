# coding: utf-8
from src.tools import app_setting
__author__ = 'jarrah'
import time

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


def select_rows_limit(table_name, from_index, *columns):
    to_index = from_index + MAX_ROWS
    print("from is %d to is %d" % (from_index, to_index))
    con = get_connection()

    columns_sql = ''
    for c in columns:
        columns_sql += c
        columns_sql += ','
        # print(columns_sql)

    if len(columns_sql):
        columns_sql = columns_sql[:-1]
        # print(columns_sql)
    else:
        columns_sql = '*'

    # print(columns_sql)

    start_sql = "select %s from %s " % (columns_sql, table_name)
    query_sql = start_sql + "limit %(_from)s,%(_to)s"
    print(query_sql)
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


def get_rows_limit_where(from_index, sql, params):
    to_index = from_index + MAX_ROWS
    print("from is %d to is %d" % (from_index, to_index))
    con = get_connection()
    query_sql = sql + " limit %s,%s"

    sql_params = list()
    for p in params:
        sql_params.append(p)

    sql_params.append(from_index)
    sql_params.append(to_index)
    items = con.query(query_sql, *sql_params)
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


def select_row_with_id(table, value, key='_id', columns=[]):
    if len(columns):
        columns_sql = encode_select_columns_clause(*columns)
    else:
        columns_sql = '*'

    con = get_connection()
    sql = "select %s FROM %s WHERE %s=" % (columns_sql, table, key)
    sql += "%s"
    row = con.query(sql, value)
    con.close()
    # print('get_single_row_as_dict')
    # print(row)
    if len(row):
        return row[0]
    else:
        return None


def encode_select_columns_clause(*columns):
    columns_sql = ''
    for c in columns:
        columns_sql += c
        columns_sql += ','
        # print(columns_sql)

    if len(columns_sql):
        columns_sql = columns_sql[:-1]
        # print(columns_sql)
    else:
        columns_sql = '*'

    return columns_sql


def switch_table_row(table_name, rows, values, delete_where_clause, delete_where_params):
    con = get_connection()
    try:
        insert_into(table_name, rows, values)
    except torndb.IntegrityError as e:
        print('favor exception', e)
        con = get_connection()
        # delete from sql
        sql = 'delete from ' + table_name + ' where ' + delete_where_clause
        con.execute(sql, *delete_where_params)
    con.close()


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
    sql = 'select _id as user_link,nick,portrait FROM user WHERE _id=%s'
    con = get_connection()
    rows = con.query(sql, user_id)
    if rows.__len__():
        rows[0]['user_link'] = app_setting.SETTINGS['HOST_USER'] + ("?user_id=%s" % user_id)
        return rows[0]
    else:
        return None

        # user = select_row_with_id('user', user_id)
        # if user:
        #     _hide_columns = ['_id', 'external_app_id', 'reg_time', 'password', 'email', 'phone']
        #     filter_columns(user, *_hide_columns)
        # return user


'''过滤不需要显示的字段'''


def filter_columns(row, *columns):
    for c in columns:
        # print("columns del name", c)
        del row[c]


'''写入post的image'''


def insert_post_image(user_id, file_path):
    timestamp = time.time()
    sql = 'insert INTO post_image(user_id,path,ts) VALUES (%s,%s,%s)'
    con = get_connection()
    row_id = con.execute(sql, user_id, file_path, timestamp)
    con.close()
    return row_id


'''查询发布的image'''


def select_post_image(image_id):
    sql = 'SELECT path FROM post_image WHERE _id=%s'
    con = get_connection()
    rows = con.query(sql, image_id)
    con.close()
    if rows.__len__():
        return rows[0]
    else:
        return None


'''添加/取消关注'''


def insert_follow(user_id, follow_id):
    try:
        sql = 'insert INTO user_follow(user_id,follow_id) VALUES (%s,%s)'
        con = get_connection()
        con.execute(sql, user_id, follow_id)
    except torndb.IntegrityError as e:
        sql = 'delete FROM user_follow where user_id=%s AND follow_id=%s'
        con = get_connection()
        con.execute(sql, user_id, follow_id)
    finally:
        con.close()


'''通过id列表获取用户列表'''


def select_multi_user_by_id_list(str_user_ids):
    '''组成in 后面的语句'''
    in_clause = ""
    for i in range(str_user_ids.__len__()):
        in_clause += '%s'
        in_clause += ','
    in_clause = in_clause[:-1]
    print(in_clause)
    sql = 'select _id,nick FROM user WHERE _id IN (%s)' % in_clause
    print(sql)
    con = get_connection()
    rows = con.query(sql, *str_user_ids)
    con.close()
    if rows.__len__():
        return rows
    else:
        return None


'''获取用户的粉丝'''


def select_user_followers(user_id):
    sql = 'select follow_id FROM user_follow WHERE user_id=%s'
    con = get_connection()
    rows = con.query(sql, user_id)
    con.close()
    if rows.__len__():
        user_ids = list()
        for row in rows:
            user_ids.append(str(row['follow_id']))
            print(user_ids)
        return select_multi_user_by_id_list(user_ids)
    else:
        return None


'''用户评论'''


def insert_moment_comment(user_id, moment_id, reply_type, content):
    sql = 'insert INTO moment_comment(user_id,moment_id,reply_type,content,ts) VALUES (%s,%s,%s,%s,%s)'
    con = get_connection()
    ts = int(time.time())
    con.execute(sql, user_id, moment_id, reply_type, content, ts)
    con.close()


'''获取评论'''


def select_moment_comment(moment_id, start=0):
    sql = "select user_id as user,reply_type,content,ts FROM moment_comment WHERE moment_id=%s limit %s,%s"
    con = get_connection()
    end = start + MAX_ROWS
    rows = con.query(sql, moment_id, start, end)
    con.close()
    if rows.__len__():
        return rows
    else:
        return None
