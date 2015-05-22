from tornado.web import HTTPError, MissingArgumentError
from torndb import IntegrityError
from src.db.service import insert_into

from src.tools.base import BaseHandler

'''user pack code'''
CODE_SUCCESS = 200
CODE_EXISTED_USER = 101

__author__ = 'jarrah'


def url_spec(**kwargs):
    return [(r'/user/signIn', SignInHandler, kwargs), (r'/user', UserHandler, kwargs)]


KEY_PHONE = 'phone'
KEY_PASSWORD = 'password'
KEY_NICK = 'nick'

TABLE_NAME = 'user'
ROW_PHONE = 'phone'
ROW_PASSWORD = 'password'
ROW_NICK = 'nick'


class SignInHandler(BaseHandler):

    def post(self, *args, **kwargs):
        user = self.get_body_dict()
        '''check params'''
        illegal_args = self.get_illegal_arguments(KEY_PHONE, KEY_PASSWORD)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        else:
            self.write(user)



class UserHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        user = self.get_body_dict()
        '''check params'''
        illegal_args = self.get_illegal_arguments(KEY_NICK, KEY_PHONE, KEY_PASSWORD)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        else:
            self.register(**user)

    def register(self, **kwargs):
        insert_id = 0
        try:
            insert_id = insert_into(TABLE_NAME, [ROW_PHONE, ROW_PASSWORD, ROW_NICK],
                                    [kwargs[KEY_PHONE], kwargs[KEY_PASSWORD], kwargs[KEY_NICK]])
        except IntegrityError:
            self.write(self.make_response_pack('existed user', CODE_EXISTED_USER))

        if insert_id:
            self.write(self.make_response_pack('success', CODE_SUCCESS, userid=insert_id))