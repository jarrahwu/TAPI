# coding: utf8
from src.tools.base import BaseHandler
from src.tools.packer import gen_link_obj, dump_list_view_pack
import os
import src.tools.path_util as path

__author__ = 'jarrah'
from src.db import service
from tornado.web import MissingArgumentError, HTTPError
from src.db.service import select_row_with_id, switch_table_row
from src.handler.user import TABLE_NAME as TABLE_USER

TABLE_CIRCLE = 'circle'
ROW_ID = '_id'
ROW_TITLE = 'title'
ROW_SLOGAN = 'slogan'
ROW_CATEGORY_ID = 'circle_category_id'
ROW_HOT_COUNT = 'hot_count'
ROW_IMAGE = 'image'

'''upload params key'''
KEY_TITLE = 'title'
KEY_SLOGAN = 'slogan'
KEY_IMAGE = 'image'
KEY_CATEGORY_ID = 'category_id'

'''circle interest'''
KEY_CIRCLE_INTEREST_OPERATION = 'operation'

TABLE_CIRCLE_INTEREST = 'circle_interest'

'''ARG circle interest'''
ARG_CIRCLE_ID = 'circle_id'

'''ARG QUERY USER ID'''
ARG_USER_ID = 'uid'
ARG_CIRCLE_INTEREST_INDEX = 'index'

MAX_INDEX_COUNT = 5

UN_KNOW_CIRCLE = {ROW_TITLE: '火星', ROW_SLOGAN: '来自火星的你', ROW_HOT_COUNT: '999'}


def url_spec(**kwargs):
    return [
        (r'/circle', CircleHandler, kwargs),
        (r'/circle/interest', CircleInterestHandler, kwargs),
        (r'/circle/static', CirleFormHandler, kwargs)
    ]


def get_circle_info(circle_id):
    row = service.select_row_with_id(TABLE_CIRCLE, circle_id, columns=[ROW_TITLE, ROW_SLOGAN])
    return row


class CirleFormHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(os.path.join(path.assets_path, 'circle.html'))


'''circle get and post'''


class CircleHandler(BaseHandler):
    def get(self, *args, **kwargs):
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)

        rows = service.select_rows_limit(TABLE_CIRCLE, _from, ROW_ID, ROW_IMAGE, ROW_SLOGAN, ROW_TITLE, ROW_HOT_COUNT)
        next_index = _from + rows.__len__()

        # for row in rows:
        #     service.filter_columns(row, ROW_ID, ROW_CATEGORY_ID)

        for r in rows:
            # remove hidden id
            # build image path
            image_name = r[ROW_IMAGE]
            image_path = self.settings['HOST_IMAGE'] + image_name
            r[ROW_IMAGE] = image_path
            follow_link = gen_link_obj("interest", self.settings['HOST_CIRCLE'] + "?circle_id=%d" % r[ROW_ID])
            r['link'] = follow_link

        next_link = gen_link_obj("next", self.settings['HOST_CIRCLE'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        items = dump_list_view_pack(rows, next_link, home_link)

        self.write(items)

    def post(self, *args, **kwargs):
        circle_data = self.get_circle_post_data()
        if circle_data is None:
            raise MissingArgumentError('add circle data!')

        image = self.save_image(KEY_IMAGE)
        if image is None:
            raise MissingArgumentError('upload image')

        service.insert_into(TABLE_CIRCLE, [ROW_TITLE, ROW_SLOGAN, ROW_IMAGE, ROW_CATEGORY_ID],
                            [circle_data[KEY_TITLE], circle_data[KEY_SLOGAN], image, circle_data[KEY_CATEGORY_ID]])

        self.write(self.ok_pack())

    def get_circle_post_data(self):
        title = self.get_argument(KEY_TITLE, None)
        slogan = self.get_argument(KEY_SLOGAN, None)
        category_id = self.get_argument(KEY_CATEGORY_ID, None)
        circle_data = dict()
        if title and slogan and category_id:
            circle_data[KEY_TITLE] = title
            circle_data[KEY_SLOGAN] = slogan
            circle_data[KEY_CATEGORY_ID] = category_id
            return circle_data
        else:
            return None


class CircleInterestHandler(BaseHandler):
    '''get follow list'''
    '''get a user interest circles'''

    def get(self, *args, **kwargs):
        query_user_id = self.get_argument(ARG_USER_ID, default=None)
        if query_user_id is None:
            raise MissingArgumentError('no user to query')

        self.get_user_info()

        index = int(self.get_argument(ARG_CIRCLE_INTEREST_INDEX, default=0))

        con = service.get_connection()
        sql = 'select circle_id FROM circle_interest WHERE user_id=%s'
        rows = con.query(sql, query_user_id)
        con.close()

        interest_circle_ids = list()
        for row in rows:
            interest_circle_ids.append(row['circle_id'])

        to_index = index + MAX_INDEX_COUNT
        if to_index >= interest_circle_ids.__len__():
            to_index = interest_circle_ids.__len__()

        rows = list()
        for i in range(index, to_index):
            r = service.select_row_with_id(TABLE_CIRCLE, interest_circle_ids[i],
                                           columns=[ROW_IMAGE, ROW_SLOGAN, ROW_TITLE, ROW_HOT_COUNT])
            rows.append(r)

        next_index = to_index
        next_link = gen_link_obj("next", self.settings['HOST_CIRCLE_INTEREST'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        items = dump_list_view_pack(rows, next_link, home_link)
        self.write(items)

    '''user interest'''

    def post(self, *args, **kwargs):
        user = self.get_user_info()

        interest_circle_id = self.get_argument(ARG_CIRCLE_ID, default=None)

        if interest_circle_id is None:
            raise MissingArgumentError('no circle id to follow')

        illegal_args = self.get_missing_arguments(KEY_CIRCLE_INTEREST_OPERATION)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        json_args = self.get_body_dict()

        # user_info = select_row_with_id(TABLE_USER, user['uid'])

        operation = json_args[KEY_CIRCLE_INTEREST_OPERATION]
        if operation == 1 or operation == 0:
            values = [int(user['uid']), interest_circle_id]
            claus = "user_id=%s and circle_id=%s"
            switch_table_row(TABLE_CIRCLE_INTEREST, ['user_id', 'circle_id'], values, claus, values)

        self.write(self.ok_pack())
