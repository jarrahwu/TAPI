import os
import uuid
from src.tools.base import BaseHandler
from src.tools.packer import gen_link_obj, dump_list_view_pack
from src.tools import path_util as path
from src.db import service
from tornado.escape import  json_encode, json_decode

__author__ = 'jarrah'


def url_spec(**kwargs):
    return [
        (r'/moment', MomentHandler, kwargs),
    ]


IMG_DIR = path.img_uploads_path

class MomentHandler(BaseHandler):

    def get(self, *args, **kwargs):
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        items = self.get_items(_from=_from)
        self.write(items)

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

        for i in range(rows.__len__()):
            row = rows.__getitem__(i)
            image = row['image']
            image_json_array = json_decode(image)

            url_images = list()
            for json_image in image_json_array:
                image_path = self.settings['HOST_IMAGE'] + json_image
                url_images.append(image_path)

            row['image'] = url_images
            print(row)

        next_index = _from + rows.__len__()
        next_link = gen_link_obj("next", self.settings['HOST_MOMENT'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        funny = dump_list_view_pack(rows, next_link, home_link)
        return funny
