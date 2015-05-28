__author__ = 'jarrah'

from src.tools.base import BaseHandler
import os
import uuid
from src.tools import path_util as path
from src.db import service

IMG_DIR = path.img_uploads_path
FORM_FILE = os.path.join(path.assets_path, 'upload.html')


def url_spec(**kwargs):
    return [
        (r'/image', ImageHandler, kwargs),
    ]


class ImageHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render(FORM_FILE)

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

        service.insert_into('news_preview', rows=['title', 'content', 'image_url'], values=['test', 'test', image_url])

        self.write(self.make_response_pack('upload success', 200, **extra))

