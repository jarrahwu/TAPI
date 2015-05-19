from tornado.web import HTTPError
from src.tools.base import BaseHandler

__author__ = 'jarrah'

def url_spec(**kwargs):
    return [(r'/user/signIn', SignInHandler, kwargs), (r'/user', UserHandler, kwargs)]


KEY_ACCOUNT = 'account'
KEY_PASSWORD = 'password'
KEY_DEVICE_ID = 'did'
KEY_NICK = 'nick'

class SignInHandler(BaseHandler):

    def post(self, *args, **kwargs):
        jo = self.get_body_dict()
        account = jo[KEY_ACCOUNT]
        password = jo[KEY_PASSWORD]
        device_id = jo[KEY_DEVICE_ID]
        if account and password and device_id:
            self.valid(account, password, device_id)
        else:
            raise HTTPError(status_code=403, reason='user do not exist!')

    def valid(self, account, password, device_id):

        if self.block(device_id):
            self.write(self.make_response_pack('block', '200'))

        if account == password:
            self.write(self.ok_pack())

    def block(self, device_id):
        if device_id:
            return False
        return True


class UserHandler(BaseHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
