from src.tools.base import BaseHandler
from src.db import service

__author__ = 'jarrah'

FAVOR_NEWS_PATH = '/favor/news'

KEY_ITEMS = 'items'
KEY_FAVOR = 'favor'
KEY_REL_ID = 'rel_id'

TABLE = 'favor_news'
ROW_REL_ID = 'rel_id'
ROW_OPERATION = 'operation'
ROW_USER_ID = 'user_id'

def url_spec(**kwargs):
    return [
        (r'/favor/news', FavorHandler, kwargs),
        ]


def set_favor(user_id, **kwargs):

    keys = kwargs.keys()
    if KEY_FAVOR in keys and KEY_REL_ID in keys:
        favor_value = kwargs[KEY_FAVOR]
        rel_id = kwargs[KEY_REL_ID]
        rows = [ROW_REL_ID, ROW_OPERATION, ROW_USER_ID]
        op = (0, 1)[favor_value]
        values = [rel_id, op, user_id]
        service.insert_into(TABLE, rows, values)

class FavorHandler(BaseHandler):

    def post(self, *args, **kwargs):

        error = self.raise_if_missing_args(KEY_ITEMS)

        if not error:
            items = self.get_body_dict()[KEY_ITEMS]
            user = self.get_user_info()
            print(user)

            for item in items:
                user_id = user['uid']
                set_favor(user_id, **item)
