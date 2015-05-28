from src.tools.base import BaseHandler

__author__ = 'jarrah'

FAVOR_NEWS_PATH = '/favor/news'


def url_spec(**kwargs):
    return [
        (r'/favor/news', FavorHandler, kwargs),
        ]


class FavorHandler(BaseHandler):

    def post(self, *args, **kwargs):
        p1 = self.get_argument('index', default=-1)
        self.write(self.make_response_pack(p=p1))
