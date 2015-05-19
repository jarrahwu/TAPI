import tornado.web

__author__ = 'jarrah'

import os
import re
from app_setting import SETTINGS

my_path = (os.path.dirname(__file__))

'''get handler path'''
handler_path = os.path.join(my_path, '..', 'handler')

handler_files = os.listdir(handler_path)

'''end with .py files '''
pattern = re.compile(r'(?P<name>.+)\.py$')


'''application run'''
import_handlers = []

for handler_py in handler_files:
    match = pattern.match(handler_py)
    if match:
        handler_name = match.group('name')
        print('import handler >>', handler_name)

        if handler_name == '__init__':
            continue
        else:
            import_models = __import__(name='src.handler.' + handler_name, fromlist=['url_spec'])
            url_specs = import_models.url_spec()
            for spec in url_specs:
                import_handlers.append(spec)

print("import handlers :", import_handlers)

application = tornado.web.Application(handlers=import_handlers, **SETTINGS)

PORT = 8888
if __name__ == '__main__':
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()