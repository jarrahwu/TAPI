# coding: utf-8
import os
import uuid
import tornado
from src.tools.base import BaseHandler
from src.tools.packer import gen_link_obj, dump_list_view_pack
from src.tools import path_util as path
from src.db import service
from tornado.escape import json_encode, json_decode
from tornado.web import MissingArgumentError
from circle import UN_KNOW_CIRCLE
from circle import get_circle_info

KEY_USER = 'user'

ROW_ID = '_id'
ROW_USER_ID = 'user_id'
ROW_COME_FROM = 'come_from'
ROW_IMAGE = 'image'
ROW_CONTENT = 'content'
ROW_TITLE = 'title'
ROW_CIRCLE_ID = "circle_id"

KEY_COME_FROM = 'come_from'
KEY_CONTENT = 'content'
KEY_TITLE = 'title'
KEY_CIRCLE = 'circle'

__author__ = 'jarrah'

UPLOAD_IMAGE_PARAMS = ['image0', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8']

def url_spec(**kwargs):
    return [
        (r'/moment', MomentHandler, kwargs),
    ]


IMG_DIR = path.img_uploads_path


class MomentHandler(BaseHandler):

    def get(self, *args, **kwargs):

        # print("moment get , cookie ", self.get_cookie("token", default="no cookie"))

        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        moment_items = self.get_moment_items(_from=_from)

        self.write(moment_items)

    def get_moment_items(self, _from=0):
        rows = service.get_moment_limit(_from)

        '''build image path'''
        for i in range(rows.__len__()):
            row = rows.__getitem__(i)

            user_id = row[ROW_USER_ID]
            user_info = self.get_moment_user(user_id)

            circle_id = row[ROW_CIRCLE_ID]
            circle_info = get_circle_info(circle_id)

            row[KEY_USER] = user_info
            if circle_info:
                row[KEY_CIRCLE] = circle_info
            else:
                row[KEY_CIRCLE] = UN_KNOW_CIRCLE

            image = row[ROW_IMAGE]
            image_json_array = json_decode(image)

            url_images = list()
            for image_name in image_json_array:
                image_path = self.settings['HOST_IMAGE'] + image_name
                url_images.append(image_path)

            row[ROW_IMAGE] = url_images

            '''filter hide column'''
            # _hide_columns = [ROW_CIRCLE_ID]
            # service.filter_columns(row, *_hide_columns)

        next_index = _from + rows.__len__()
        next_link = gen_link_obj("next", self.settings['HOST_MOMENT'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        items = dump_list_view_pack(rows, next_link, home_link)
        return items

    '''获取关联的moment user'''
    def get_moment_user(self, user_id):
        return service.get_user_with(user_id)

    def post(self, *args, **kwargs):
        # if no circle id do not allow publish
        circle_id = self.get_argument('circle_id', default=None)

        # default info
        if not circle_id:
            raise MissingArgumentError('follow a circle first')

        # print("moment post , cookie " + self.get_cookie("token"))
        user = self.get_user_info()

        moment_data = self.get_moment_data()
        if not moment_data:
            raise tornado.web.MissingArgumentError('missing args')

        images = list()
        for param in UPLOAD_IMAGE_PARAMS:
            file_name = self.save_image(param)

            if file_name is None:
                break

            # image_url = self.settings['HOST_IMAGE'] + file_name
            images.append(file_name)

        image_json_array = json_encode(images)

        service.insert_into('moment', rows=[ROW_TITLE, ROW_CONTENT, ROW_IMAGE, ROW_COME_FROM, ROW_USER_ID, ROW_CIRCLE_ID],
                            values=[moment_data[KEY_TITLE], moment_data[KEY_CONTENT], image_json_array,
                                    moment_data[KEY_COME_FROM], user["uid"], circle_id])

        extra = dict()
        extra['file_name'] = images
        self.write(self.make_response_pack('upload success', 200, **extra))

    def save_image(self, upload_param):

        if upload_param not in self.request.files:
            return None

        upload_file = self.request.files[upload_param][0]
        upload_file_name = upload_file['filename']
        upload_type = os.path.splitext(upload_file_name)[1]
        file_name = str(uuid.uuid4()) + upload_type
        file_path = os.path.join(IMG_DIR, file_name)
        store_file = open(file_path, 'w')
        store_file.write(upload_file['body'])
        return file_name

    def get_moment_data(self):
        title = self.get_argument(KEY_TITLE, None)
        content = self.get_argument(KEY_CONTENT, None)
        come_from = self.get_argument(KEY_COME_FROM, None)
        moment_data = dict()
        if title and content and come_from:
            moment_data[KEY_TITLE] = title
            moment_data[KEY_CONTENT] = content
            moment_data[KEY_COME_FROM] = come_from
            return moment_data
        else:
            return None
