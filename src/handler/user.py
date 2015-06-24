from tornado.web import HTTPError, MissingArgumentError
from torndb import IntegrityError
from src.db.service import insert_into
from src.db.service import get_connection

from src.tools.base import BaseHandler
import src.tools.constant as USER_DEFINE

__author__ = 'jarrah'


def url_spec(**kwargs):
    return [(r'/user/login', LoginHandler, kwargs), (r'/user', UserHandler, kwargs)]


KEY_PHONE = 'phone'
KEY_PASSWORD = 'password'
KEY_NICK = 'nick'
KEY_MSG_CODE = 'msg_code'

TABLE_NAME = 'user'
ROW_PHONE = 'phone'
ROW_PASSWORD = 'password'
ROW_NICK = 'nick'
ROW_ID = '_id'


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write("login")

    def post(self, *args, **kwargs):
        user = self.get_body_dict()
        '''check params'''
        illegal_args = self.get_missing_arguments(KEY_PHONE, KEY_PASSWORD)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        else:
            self.query_user(user)

    def query_user(self, user):
        print(user)
        con = get_connection()
        query = 'select * from user where phone=%s'
        rows = con.query(query, user[KEY_PHONE])
        con.close()

        if rows is not None and len(rows) > 0:
            row_user = rows[0]
            row_pwd = row_user[ROW_PASSWORD]
            row_phone = row_user[ROW_PHONE]
            row_id = row_user[ROW_ID]

            if row_pwd == user[KEY_PASSWORD]:
                token = self.token_encode(row_id, row_phone)
                row_user.__delitem__(ROW_ID)
                row_user.__delitem__(ROW_PASSWORD)

                self.set_secure_token(token)
                self.write(self.make_response_pack('login success', user=row_user, token=token))
            else:
                self.write(self.make_response_pack('password error', USER_DEFINE.CODE_PASSWORD_ERROR))
        else:
            self.write(self.make_response_pack('user does not exist', USER_DEFINE.CODE_USER_NOT_EXIST))


class UserHandler(BaseHandler):
    def get(self, *args, **kwargs):
        token = self.get_token()
        user = self.token_decode(token)
        print("user get token", token)
        print("create sign value", self.create_signed_value("token", token, version=None))
        self.write(self.make_response_pack(token=self.token_encode(**user)))

    def post(self, *args, **kwargs):
        user = self.get_body_dict()
        '''check params'''
        illegal_args = self.get_missing_arguments(KEY_NICK, KEY_PHONE, KEY_PASSWORD)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        else:
            self.register(**user)

    def register(self, **kwargs):

        # if '696969' != kwargs[KEY_MSG_CODE]:
        #     self.write(self.make_response_pack('msg code error', USER_DEFINE.CODE_USER_MSG_CODE_ERROR))
        #     return

        insert_id = 0
        try:
            insert_id = insert_into(TABLE_NAME, [ROW_PHONE, ROW_PASSWORD, ROW_NICK],
                                    [kwargs[KEY_PHONE], kwargs[KEY_PASSWORD], kwargs[KEY_NICK]])
        except IntegrityError:
            self.write(self.make_response_pack('existed user', USER_DEFINE.CODE_EXISTED_USER))

        if insert_id:
            self.write(self.make_response_pack('success', USER_DEFINE.CODE_SUCCESS, userid=insert_id))
