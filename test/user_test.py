from tornado.escape import json_encode
from src.tools import base as handler_base
from test.base import BaseAsyncTest
from src.handler import user
from src.db.service import get_connection
import base64


__author__ = 'jarrah'

TEST_NICK = 'jtest_user'
TEST_PASSWORD = base64.b64encode('123456', 'utf-8')
TEST_PHONE = '13316850712'

PATH = '/user'
PATH_LOGIN = '/user/login'


def del_test_user():
    sql = 'delete from user where ' + user.ROW_PHONE + '=%s' + ' and ' + user.ROW_NICK + '=%s'
    con = get_connection()
    con.execute(sql, TEST_PHONE, TEST_NICK)
    con.close()


class SignInTest(BaseAsyncTest):
    def get_handlers(self):
        return user.url_spec()

    def tearDown(self):
        del_test_user()

    def test_sign_in(self):
        del_test_user()
        print('setup sign in')
        sql = 'insert into user(%s,%s,%s)' % (
            user.ROW_NICK, user.ROW_PHONE, user.ROW_PASSWORD)
        sql += ' values(%s,%s,%s)'
        con = get_connection()
        con.execute(sql, TEST_NICK, TEST_PHONE, TEST_PASSWORD)
        con.close()

        si = dict()
        si[user.KEY_PHONE] = TEST_PHONE
        si[user.KEY_PASSWORD] = TEST_PASSWORD
        jo = self.json_encode_body(**si)
        response = self.fetch(path=PATH_LOGIN, method='POST', body=jo)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        print("login", response.body)

    def test_login_user_not_exist(self):
        del_test_user()
        sql = 'insert into user(%s,%s,%s)' % (
            user.ROW_NICK, user.ROW_PHONE, user.ROW_PASSWORD)
        sql += ' values(%s,%s,%s)'
        con = get_connection()
        con.execute(sql, TEST_NICK, TEST_PHONE, TEST_PASSWORD)
        con.close()

        si = dict()
        si[user.KEY_PHONE] = "123344213"
        si[user.KEY_PASSWORD] = TEST_PASSWORD
        jo = self.json_encode_body(**si)
        response = self.fetch(path=PATH_LOGIN, method='POST', body=jo)
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(response.body)
        jo_rsp = self.json_decode_body(response)
        self.assertEqual(jo_rsp[handler_base.KEY_RESPONSE_CODE], user.CODE_USER_NOT_EXIST)


class UserTest(BaseAsyncTest):
    def get_handlers(self):
        return user.url_spec()

    def fetch_insert(self):
        jo = dict()
        jo[user.KEY_PHONE] = TEST_PHONE
        jo[user.KEY_PASSWORD] = TEST_PASSWORD
        jo[user.KEY_NICK] = TEST_NICK
        response = self.fetch(PATH, method='POST', body=self.json_encode_body(**jo))
        return response

    def test_reg_args_error(self):
        jo = dict()
        jo[user.KEY_PHONE] = TEST_PHONE
        jo[user.KEY_PASSWORD] = TEST_PASSWORD
        body = json_encode(jo)
        response = self.fetch(path=PATH, method='POST', body=body)
        self.assertEqual(400, response.code)
        del jo

        response = self.fetch(path=PATH, method='POST', body="")
        self.assertEqual(400, response.code)

    def test_reg(self):
        print("test reg")
        response = self.fetch_insert()
        self.assertIsNotNone(response)
        self.assertEqual(response.code, 200)
        bjo = self.json_decode_body(response)
        self.assertEqual(user.CODE_SUCCESS, bjo[handler_base.KEY_RESPONSE_CODE])

    def test_duplicated_reg(self):
        print("test duplicated reg")
        response = self.fetch_insert()
        self.assertIsNotNone(response)
        self.assertEqual(response.code, 200)
        bjo = self.json_decode_body(response)
        self.assertEqual(user.CODE_SUCCESS, bjo[handler_base.KEY_RESPONSE_CODE])

        response = self.fetch_insert()
        self.assertIsNotNone(response)
        self.assertEqual(response.code, 200)
        bjo = self.json_decode_body(response)
        self.assertEqual(user.CODE_EXISTED_USER, bjo[handler_base.KEY_RESPONSE_CODE])

    def tearDown(self):
        del_test_user()