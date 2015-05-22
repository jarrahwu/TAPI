from tornado.escape import json_decode
from tornado.web import HTTPError

__author__ = 'jarrah'

import tornado.web
import abc

KEY_RESPONSE_CODE = 'code'
KEY_RESPONSE_MSG = 'msg'
KEY_RESPONSE_EXTRA = 'extra'


class BaseHandler(tornado.web.RequestHandler):
    def get_body_dict(self):
        jo = None
        try:
            jo = json_decode(self.request.body)
        except:
            raise HTTPError(status_code=400, reason='data format error')
        return jo

    def make_response_pack(self, msg, code, **kwargs):
        pack = dict()
        pack[KEY_RESPONSE_MSG] = msg
        pack[KEY_RESPONSE_CODE] = code
        pack[KEY_RESPONSE_EXTRA] = kwargs
        return pack

    def get_illegal_arguments(self, *args):
        jo = self.get_body_dict()
        illegal_args = ''
        for arg in args:
            if arg not in jo:
                illegal_args += arg
                illegal_args += ','
        return (None, illegal_args)[len(illegal_args) > 0]


    def ok_pack(self):
        extra = dict()
        return self.make_response_pack('ok', 200, **extra)