from src.tools.base import BaseHandler

__author__ = 'jarrah'

def url_spec(**kwargs):
    return [(r'/', HomeHandler, kwargs)]

class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write('Welcome To Blue - . -')