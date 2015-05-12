__author__ = 'jarrah'

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def settings(self):
        return super(BaseHandler, self).settings()