<<<<<<< HEAD
# coding: utf-8
=======
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
import uuid
from tornado.escape import json_decode
from tornado.web import HTTPError
from src.tools import path_util
import src.tools.constant as CONSTANT
<<<<<<< HEAD
from tornado.web import MissingArgumentError
=======
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
import os

import base64
from src.tools.packer import gen_link_obj, dump_list_view_pack

__author__ = 'jarrah'

import tornado.web

# KEY_RESPONSE_CODE = 'code'
# KEY_RESPONSE_MSG = 'msg'
# KEY_RESPONSE_EXTRA = 'extra'
#
# CODE_SUCCESS = CONSTANT.CODE_SUCCESS
# CODE_ERROR = CONSTANT.CODE_ERROR
#
# MSG_OK = 'ok'
# MSG_ERROR = 'error'

EXPIRES_DAYS = 15


class BaseHandler(tornado.web.RequestHandler):
    def get_body_dict(self):
        jo = None
        try:
            jo = json_decode(self.request.body)
        except:
            print('decode body error', self.request.body)
            raise HTTPError(status_code=400, reason='data format error')
        return jo

    def make_response_pack(self, msg=CONSTANT.MSG_OK, code=CONSTANT.CODE_SUCCESS, **kwargs):
        pack = dict()
        pack[CONSTANT.KEY_RESPONSE_MSG] = msg
        pack[CONSTANT.KEY_RESPONSE_CODE] = code
        pack[CONSTANT.KEY_RESPONSE_EXTRA] = kwargs
        return pack

    def get_missing_arguments(self, *args):
        jo = self.get_body_dict()
        illegal_args = ''
        for arg in args:
            if arg not in jo:
                illegal_args += arg
                illegal_args += ','

        return (None, illegal_args)[len(illegal_args) > 0]

    def raise_if_missing_args(self, *args):
        missing = self.get_missing_arguments(*args)
        if missing:
            raise tornado.web.MissingArgumentError(missing)
        else:
            return False

    def ok_pack(self):
        extra = dict()
        return self.make_response_pack(CONSTANT.MSG_OK, CONSTANT.CODE_SUCCESS, **extra)

    def token_encode(self, uid, phone):
        uid = str(uid)
        phone = str(phone)
        uid = base64.b64encode(uid, 'utf-8')
        phone = base64.b64encode(phone, 'utf-8')
        return '%s|%s' % (uid, phone)

    def token_decode(self, token):
        uid, phone = token.split('|')
        uid = base64.b64decode(uid, 'utf-8')
        phone = base64.b64decode(phone, 'utf-8')
        return {'uid': uid, 'phone': phone}

    def set_secure_token(self, value):
        self.set_secure_cookie('token', value, expires_days=EXPIRES_DAYS)

    def set_secure_token_with(self, uid, phone):
        value = self.token_encode(uid, phone)
        self.set_secure_cookie('token', value, expires_days=EXPIRES_DAYS)

    def get_token(self, raise_error=True):
        token = self.get_secure_cookie('token')
        if token:
            return token
        elif raise_error:
            raise tornado.web.HTTPError(403)
        else:
            return None

    def get_user_info(self):
        return self.token_decode(self.get_token())

    '''save multipart image'''
<<<<<<< HEAD

=======
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
    def save_image(self, upload_param):
        image_dir = path_util.img_uploads_path
        if upload_param not in self.request.files:
            return None
        upload_file = self.request.files[upload_param][0]
        upload_file_name = upload_file['filename']
        upload_type = os.path.splitext(upload_file_name)[1]
        file_name = str(uuid.uuid4()) + upload_type
        file_path = os.path.join(image_dir, file_name)
        store_file = open(file_path, 'w')
        store_file.write(upload_file['body'])
        return file_name
<<<<<<< HEAD

    '''获取索引 ?inde='''

    def get_index(self):
        return int(self.get_argument('index', 0))

    '''获取参数, 没有的话抛出400'''

    def get_arg(self, key):
        arg = self.get_argument(key, default=None)
        print("get_arg", arg)
        if arg is None:
            raise MissingArgumentError(key)
        else:
            return arg

    '''获取post 过来的json 如果没有对应的字段, 就抛出异常'''

    def get_post_json(self, *keys):
        json = self.get_body_dict()
        print(json)
        if not json:
            raise MissingArgumentError('not found json')

        for key in keys:
            if key not in json:
                raise MissingArgumentError('json miss ' + key)
        return json

    '''输出listview items , 添加 next url, rows service查询出来的rows, index 索引, url handler对应的访问url'''

    def write_items(self, rows, url, index, *other_links):
        next_index = index + rows.__len__()

        if "?" in url:
            op = '&'
        else:
            op = '?'

        next_link = gen_link_obj("next", url + "%sindex=%d" % (op, next_index))
        links = list()
        links.append(next_link)
        for l in other_links:
            links.append(l)
        items = dump_list_view_pack(rows, *links)
        self.write(items)
=======
>>>>>>> 14dca0509e3022adbf5f2e64b42384b4d3e2746b
