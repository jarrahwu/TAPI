# coding: utf-8
import os
import uuid
import time
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
ROW_IMAGE = 'image'
ROW_CONTENT = 'content'
ROW_TITLE = 'title'
ROW_CIRCLE_ID = "circle_id"
<<<<<<< HEAD
ROW_TIMESTAMP = 'ts'

KEY_DATA = 'data'
KEY_CONTENT = 'content'
KEY_TITLE = 'title'
KEY_COMMENT_LINK = 'link_comment'

=======
ROW_TIMESTAMP = 'timestamp'

KEY_CONTENT = 'content'
KEY_TITLE = 'title'
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b

''':key response circle json key'''
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

<<<<<<< HEAD
=======
        # print("moment get , cookie ", self.get_cookie("token", default="no cookie"))

>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        moment_items = self.get_moment_items(_from=_from)

        self.write(moment_items)

    def get_moment_items(self, _from=0):
        rows = service.get_moment_limit(_from)

<<<<<<< HEAD
        '''build image path and extra info'''
        for i in range(rows.__len__()):
            row = rows.__getitem__(i)

            '''read moment user info'''
            user_id = row[ROW_USER_ID]
            moment_user = self.get_moment_user(user_id)

            '''read circle info'''
            circle_id = row[ROW_CIRCLE_ID]
            circle_info = get_circle_info(circle_id)

            '''append user dict'''
=======
        '''build image path'''
        for i in range(rows.__len__()):
            row = rows.__getitem__(i)

            user_id = row[ROW_USER_ID]
            moment_user = self.get_moment_user(user_id)

            circle_id = row[ROW_CIRCLE_ID]
            circle_info = get_circle_info(circle_id)

>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
            row[KEY_USER] = moment_user
            if circle_info:
                row[KEY_CIRCLE] = circle_info
            else:
                row[KEY_CIRCLE] = UN_KNOW_CIRCLE

<<<<<<< HEAD
            '''build image json array'''
            image = row[ROW_IMAGE]
            image_json_array = json_decode(image)

            '''get image row by image id'''
            url_images = list()
            for image_id in image_json_array:
                image_row = service.select_post_image(image_id)
                if image_row is not None:
                    image_path = self.settings['HOST_IMAGE'] + image_row['path']
                    url_images.append(image_path)

            row[ROW_IMAGE] = url_images

            '''add comment link'''
            row[KEY_COMMENT_LINK] = gen_link_obj("comment", self.settings['HOST_COMMENT'] + "?moment_id=%s" % row[ROW_ID])

            '''filter hide column'''
            _hide_columns = [ROW_USER_ID, ROW_ID, ROW_CIRCLE_ID]
            service.filter_columns(row, *_hide_columns)

        '''add link'''
=======
            image = row[ROW_IMAGE]
            image_json_array = json_decode(image)

            url_images = list()
            for image_name in image_json_array:
                image_path = self.settings['HOST_IMAGE'] + image_name
                url_images.append(image_path)

            row[ROW_IMAGE] = url_images

            '''filter hide column'''
            _hide_columns = [ROW_USER_ID, ROW_ID]
            service.filter_columns(row, *_hide_columns)

>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
        next_index = _from + rows.__len__()
        next_link = gen_link_obj("next", self.settings['HOST_MOMENT'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        items = dump_list_view_pack(rows, next_link, home_link)
        return items

    '''获取关联的moment user'''

    def get_moment_user(self, user_id):
        return service.get_user_with(user_id)

<<<<<<< HEAD
    '''发布moment'''
=======
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
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
<<<<<<< HEAD
            if file_name is None:
                break
            image_id = service.insert_post_image(user['uid'], file_name)
            images.append(image_id)
=======

            if file_name is None:
                break

            # image_url = self.settings['HOST_IMAGE'] + file_name
            images.append(file_name)
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b

        image_json_array = json_encode(images)

        ts = int(time.time())
        service.insert_into('moment',
                            rows=[ROW_TITLE, ROW_CONTENT, ROW_IMAGE, ROW_USER_ID, ROW_CIRCLE_ID,
                                  ROW_TIMESTAMP],
                            values=[moment_data[KEY_TITLE], moment_data[KEY_CONTENT], image_json_array, user["uid"],
                                    circle_id, ts])

<<<<<<< HEAD
        self.write(self.ok_pack())

    def get_moment_data(self):
        data = self.get_argument(KEY_DATA, None)
        if data is None:
            return None
        data = json_decode(data)
        if KEY_TITLE in data and KEY_CONTENT in data:
            return data
=======
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
        moment_data = dict()
        if title and content:
            moment_data[KEY_TITLE] = title
            moment_data[KEY_CONTENT] = content
            return moment_data
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
        else:
            return None
