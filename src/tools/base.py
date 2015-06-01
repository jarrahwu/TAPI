from tornado.escape import json_decode
from tornado.web import HTTPError

import base64

__author__ = 'jarrah'

import tornado.web

KEY_RESPONSE_CODE = 'code'
KEY_RESPONSE_MSG = 'msg'
KEY_RESPONSE_EXTRA = 'extra'

CODE_SUCCESS = 1000
CODE_ERROR = 1002
MSG_OK = 'ok'
MSG_ERROR = 'error'

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

    def make_response_pack(self, msg=MSG_OK, code=CODE_SUCCESS, **kwargs):
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
        return self.make_response_pack(MSG_OK, CODE_SUCCESS, **extra)

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

    def get_request_token(self, raise_error=True):
        token = self.get_secure_cookie('token')
        if token:
            return token
        elif raise_error:
            raise tornado.web.HTTPError(403)
        else:
            return None