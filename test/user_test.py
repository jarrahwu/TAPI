from tornado.escape import json_encode
from test.base import BaseAsyncTest
from src.handler import user
from src.db.service import get_connection
import base64
import src.tools.constant as CONSTANT


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


class LoginTest(BaseAsyncTest):
    def get_handlers(self):
        return user.url_spec()

    def tearDown(self):
        del_test_user()

    def test_sign_in(self):
        print("test_sign_in")
        del_test_user()
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
        print("test_login_user_not_exist")
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
        self.assertEqual(jo_rsp[CONSTANT.KEY_RESPONSE_CODE], CONSTANT.CODE_USER_NOT_EXIST)


class UserTest(BaseAsyncTest):
    def get_handlers(self):
        return user.url_spec()

    def fetch_insert(self):
        print("fetch_insert")
        jo = dict()
        jo[user.KEY_PHONE] = TEST_PHONE
        jo[user.KEY_PASSWORD] = TEST_PASSWORD
        jo[user.KEY_NICK] = TEST_NICK
        response = self.fetch(PATH, method='POST', body=self.json_encode_body(**jo))
        return response

    def test_reg_args_error(self):
        print("test_reg_args_error")
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
        self.assertEqual(CONSTANT.CODE_SUCCESS, bjo[CONSTANT.KEY_RESPONSE_CODE])

    def test_duplicated_reg(self):
        print("test duplicated reg")
        response = self.fetch_insert()
        self.assertIsNotNone(response)
        self.assertEqual(response.code, 200)
        bjo = self.json_decode_body(response)
        self.assertEqual(CONSTANT.CODE_SUCCESS, bjo[CONSTANT.KEY_RESPONSE_CODE])

        response = self.fetch_insert()
        self.assertIsNotNone(response)
        self.assertEqual(response.code, 200)
        bjo = self.json_decode_body(response)
        self.assertEqual(CONSTANT.CODE_EXISTED_USER, bjo[CONSTANT.KEY_RESPONSE_CODE])

    def tearDown(self):
        print("tearDown")
        del_test_user()