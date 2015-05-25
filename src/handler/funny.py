from src.db import service
from src.tools.base import BaseHandler
from src.tools.packer import dump_list_view_pack
from src.tools.packer import gen_link_obj

__author__ = 'jarrah'

def url_spec(**kwargs):
    return [
        (r'/funny', FunnyHandler, kwargs),
        ]


class FunnyHandler(BaseHandler):
    def get(self, *args, **kwargs):
        arg = self.get_argument(name="index", default=0)
        _from = int(arg)
        self.write(self.get_items(_from=_from))

    def post(self, *args, **kwargs):
        pass

    def get_items(self, _from=0):
        rows = service.get_funny_limit(_from)
        next_index = _from + rows.__len__()
        next_link = gen_link_obj("next", self.settings['HOST_FUNNY'] + "?index=%d" % next_index)
        home_link = gen_link_obj("home", self.settings['HOST'])
        funny = dump_list_view_pack(rows, next_link, home_link)
        return funny