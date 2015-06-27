# coding: utf8
from src.tools.base import BaseHandler
from src.tools.packer import gen_link_obj, dump_list_view_pack
import os
import src.tools.path_util as path

__author__ = 'jarrah'
from src.db import service
from tornado.web import MissingArgumentError

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

UN_KNOW_CIRCLE = {ROW_TITLE: '火星', ROW_SLOGAN: '来自火星的你', ROW_HOT_COUNT: '999'}


def url_spec(**kwargs):
    return [
        (r'/circle', CircleHandler, kwargs),
        (r'/circle/follow', FollowHandler, kwargs),
        (r'/circle/static', CirleFormHandler, kwargs)
    ]


def get_circle_info(circle_id):
    row = service.get_single_row_as_dict(TABLE_CIRCLE, circle_id)
    # if row:
    #     service.filter_columns(ROW_ID, ROW_CATEGORY_ID)
    return row


class CirleFormHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(os.path.join(path.assets_path, 'circle.html'))


'''circle get and post'''


class CircleHandler(BaseHandler):
    def get(self, *args, **kwargs):
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)

        rows = service.get_rows_limit(TABLE_CIRCLE, from_index=_from)
        next_index = _from + rows.__len__()

        # for row in rows:
        #     service.filter_columns(row, ROW_ID, ROW_CATEGORY_ID)

        for r in rows:
            # remove hidden id
            service.filter_columns(r, ROW_ID, ROW_CATEGORY_ID)
            # build image path
            image_name = r[ROW_IMAGE]
            image_path = self.settings['HOST_IMAGE'] + image_name
            r[ROW_IMAGE] = image_path

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


class FollowHandler(BaseHandler):
    '''get follow list'''

    def get(self, *args, **kwargs):
        pass

    '''do follow'''

    def post(self, *args, **kwargs):
        pass
