import time
from tornado.web import HTTPError, MissingArgumentError
from torndb import IntegrityError
from src.db.service import insert_into
from src.db.service import get_connection
from src.db.service import select_row_with_id

from src.tools.base import BaseHandler
import src.tools.constant as USER_DEFINE
from tornado.escape import json_decode, json_encode

__author__ = 'jarrah'


def url_spec(**kwargs):
    return [(r'/user/login', LoginHandler, kwargs), (r'/user', UserHandler, kwargs),
            (r'/user/circle', UserCircleHandler, kwargs)]


KEY_PHONE = 'phone'
KEY_PASSWORD = 'password'
KEY_NICK = 'nick'
KEY_MSG_CODE = 'msg_code'

TABLE_NAME = 'user'
ROW_PHONE = 'phone'
ROW_PASSWORD = 'password'
ROW_NICK = 'nick'
ROW_ID = '_id'
ROW_REG_TIME = "reg_time"
ROW_FOLLOW = 'follow_circles'


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
            reg_time = int(time.time())
            insert_id = insert_into(TABLE_NAME, [ROW_PHONE, ROW_PASSWORD, ROW_NICK, ROW_REG_TIME],
                                    [kwargs[KEY_PHONE], kwargs[KEY_PASSWORD], kwargs[KEY_NICK], reg_time])
        except IntegrityError:
            self.write(self.make_response_pack('existed user', USER_DEFINE.CODE_EXISTED_USER))

        if insert_id:
            self.write(self.make_response_pack('success', USER_DEFINE.CODE_SUCCESS, userid=insert_id))


'''user follow circle'''

'''1 FOLLOW 0 UN_FOLLOW'''
KEY_CIRCLE_OPERATION = 'operation'

ARG_CIRCLE_ID = 'circle_id'


class UserCircleHandler(BaseHandler):

    def post(self, *args, **kwargs):

        user = self.get_user_info()

        follow_circle_id = self.get_argument(ARG_CIRCLE_ID, default=None)

        if follow_circle_id is None:
            raise MissingArgumentError('no circle id to follow')

        illegal_args = self.get_missing_arguments(KEY_CIRCLE_OPERATION)
        if illegal_args:
            raise MissingArgumentError(illegal_args)
        json_args = self.get_body_dict()

        user_info = select_row_with_id(TABLE_NAME, user['uid'])

        if user_info is None:
            raise HTTPError(status_code=404, log_message='user not found')
        else:
            update_user_circle_follow(user_info, json_args, follow_circle_id)

        self.write(self.ok_pack())


def update_user_circle_follow(user_info, json_args, follow_circle_id):
    last_circle_follow = user_info[ROW_FOLLOW]
    if last_circle_follow is None:
        circle_follow_list = []
    else:
        circle_follow_list = json_decode(last_circle_follow)

    if json_args[KEY_CIRCLE_OPERATION] == 1:
        '''follow'''
        circle_follow_list = set(circle_follow_list)
        circle_follow_list.add(follow_circle_id)
    else:
        circle_follow_list = set(circle_follow_list)
        circle_follow_list.remove(follow_circle_id)

    current_circle_list = list(circle_follow_list)

    '''write to db'''
    con = get_connection()
    sql = 'UPDATE %s SET %s=%s WHERE %s=%s' % (TABLE_NAME, ROW_FOLLOW, '%s', ROW_ID, '%s')
    param = json_encode(current_circle_list)
    print("sql", sql, "params", [param, str(user_info[ROW_ID])])
    con.execute(sql, *[param, user_info[ROW_ID]])
    con.close()

