import os
import uuid
<<<<<<< HEAD
import tornado
=======
>>>>>>> 78f14c8950bc4584eae3989584b141a012385210
from src.tools.base import BaseHandler
from src.tools.packer import gen_link_obj, dump_list_view_pack
from src.tools import path_util as path
from src.db import service
<<<<<<< HEAD
from tornado.escape import json_encode, json_decode

ROW_USER_ID = 'user_id'
ROW_COME_FROM = 'come_from'
ROW_IMAGE = 'image'
ROW_CONTENT = 'content'
ROW_TITLE = 'title'

KEY_COME_FROM = 'come_from'
KEY_CONTENT = 'content'
KEY_TITLE = 'title'

__author__ = 'jarrah'

UPLOAD_IMAGE_PARAMS = ['image0', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8']

=======
from tornado.escape import  json_encode, json_decode

__author__ = 'jarrah'

>>>>>>> 78f14c8950bc4584eae3989584b141a012385210

def url_spec(**kwargs):
    return [
        (r'/moment', MomentHandler, kwargs),
    ]


IMG_DIR = path.img_uploads_path

<<<<<<< HEAD

class MomentHandler(BaseHandler):
=======
class MomentHandler(BaseHandler):

>>>>>>> 78f14c8950bc4584eae3989584b141a012385210
    def get(self, *args, **kwargs):
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        items = self.get_items(_from=_from)
        self.write(items)

<<<<<<< HEAD
    def get_items(self, _from=0):
        rows = service.get_moment_limit(_from)

        '''build image path'''
=======
    def post(self, *args, **kwargs):
        upload_arg = self.request.files['image'][0]
        upload_file_name = upload_arg['filename']
        upload_type = os.path.splitext(upload_file_name)[1]

        file_name = str(uuid.uuid4()) + upload_type
        file_path = os.path.join(IMG_DIR, file_name)

        store_file = open(file_path, 'w')
        store_file.write(upload_arg['body'])

        image_url = self.settings['HOST_IMAGE'] + file_name

        extra = dict()
        extra['file_name'] = image_url

        images = list()
        images.append(file_name)

        image_json_array = json_encode(images)

        service.insert_into('moment', rows=['title', 'content', 'image', 'come_from', 'user_id'],
                            values=['test', 'test', image_json_array, 'Blue C', 1])

        self.write(self.make_response_pack('upload success', 200, **extra))

    def get_items(self, _from=0):
        rows = service.get_moment_limit(_from)

>>>>>>> 78f14c8950bc4584eae3989584b141a012385210
        for i in range(rows.__len__()):
            row = rows.__getitem__(i)
            image = row['image']
            image_json_array = json_decode(image)

            url_images = list()
<<<<<<< HEAD
            for image_name in image_json_array:
                image_path = self.settings['HOST_IMAGE'] + image_name
                url_images.append(image_path)

            row['image'] = url_images
=======
            for json_image in image_json_array:
                image_path = self.settings['HOST_IMAGE'] + json_image
                url_images.append(image_path)

            row['image'] = url_images
            print(row)
>>>>>>> 78f14c8950bc4584eae3989584b141a012385210

        next_index = _from + rows.__len__()
        next_link = gen_link_obj("next", self.settings['HOST_MOMENT'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
<<<<<<< HEAD
        items = dump_list_view_pack(rows, next_link, home_link)
        return items

    def post(self, *args, **kwargs):

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

        service.insert_into('moment', rows=[ROW_TITLE, ROW_CONTENT, ROW_IMAGE, ROW_COME_FROM, ROW_USER_ID],
                            values=[moment_data[KEY_TITLE], moment_data[KEY_CONTENT], image_json_array,
                                    moment_data[KEY_COME_FROM], 1])

        extra = dict()
        extra['file_name'] = images
        self.write(self.make_response_pack('upload success', 200, **extra))

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
=======
        funny = dump_list_view_pack(rows, next_link, home_link)
        return funny
>>>>>>> 78f14c8950bc4584eae3989584b141a012385210
