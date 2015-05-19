from tornado.escape import json_decode

__author__ = 'jarrah'

import tornado.web
import abc


class BaseHandler(tornado.web.RequestHandler):

    def get_body_dict(self):
        jo = json_decode(self.request.body)
        return jo

    def make_response_pack(self, msg, code, **kwargs):
        pack = dict()
        pack['msg'] = msg
        pack['code'] = code
        pack['extra'] = kwargs
        return pack

    def ok_pack(self):
        extra = dict()
        return self.make_response_pack('ok', 200, **extra)