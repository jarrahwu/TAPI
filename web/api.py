__author__ = 'jarrah'
import tornado.web
import tornado.ioloop
from factory import APK
from factory import FUNY

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello world!")


class ItemsHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        apk = APK()
        self.write(apk.create())

class FunnyHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        funny = FUNY()
        self.write(funny.get_items())

app = tornado.web.Application([(r"/", MainHandler), (r"/apks", ItemsHandler), (r"/funny", FunnyHandler)])

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()