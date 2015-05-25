__author__ = 'jarrah'

import os

tools_path = os.path.abspath(os.path.dirname(__file__))

src_path = os.path.join(tools_path, '..')

handler_path = os.path.join(src_path, 'handler')

db_path = os.path.join(src_path, 'db')

ROOT = os.path.join(src_path, '..')

img_uploads_path = os.path.join(ROOT, 'img_uploads')

assets_path = os.path.join(ROOT, 'assets')
