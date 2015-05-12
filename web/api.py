__author__ = 'jarrah'
import tornado.web
import tornado.ioloop

from factory import APK
from factory import Funny


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello world!")


class ItemsHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        apk = APK()
        self.write(apk.create())


class FunnyHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        funny = Funny()
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        self.write(funny.get_items(_from=_from))


app = tornado.web.Application([(r"/", MainHandler), (r"/apks", ItemsHandler), (r"/funny", FunnyHandler)])

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()