# __author__ = 'jarrah'
# import tornado.web
# import tornado.ioloop
# from tornado.options import define, options
#
# from src.web.factory import Funny
#
#
# define(name="host", default="http://192.168.160.128:8888")
# define(name="host_funny", default=options.host + "/funny")
#
#
# class HomeHandler(tornado.web.RequestHandler):
#     def get(self, *args, **kwargs):
#         self.write("hello TAPI!")
#
# class FunnyHandler(tornado.web.RequestHandler):
#     def get(self, *args, **kwargs):
#         funny = Funny()
#         arg = self.get_argument(name="index", default=0)
#         _from = int(arg)
#         self.write(funny.get_items(_from=_from))
#
#     def post(self, *args, **kwargs):
#         pass
#
#
# app = tornado.web.Application([(r"/", HomeHandler), (r"/funny", FunnyHandler)])
#
# # if __name__ == '__main__':
# #     app.listen(8888)
# #     tornado.ioloop.IOLoop.instance().start()