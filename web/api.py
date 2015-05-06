__author__ = 'jarrah'
import tornado.web
import tornado.ioloop
from factory import APK


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello world!")


class ItemsHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        apk = APK()
        self.write(apk.create())

app = tornado.web.Application([(r"/", MainHandler), (r"/apks", ItemsHandler)])

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()