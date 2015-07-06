from src.tools.base import BaseHandler
from src.db import service
from src.tools.packer import gen_link_obj, dump_list_view_pack

__author__ = 'jarrahwu'


def url_spec(**kwargs):
    return [
        (r'/comment', MomentCommentHandler, kwargs),
    ]


ARG_MOMENT_ID = 'moment_id'

KEY_CONTENT = 'content'
KEY_REPLY_TYPE = 'reply_type'


class MomentCommentHandler(BaseHandler):
    def post(self, *args, **kwargs):
        user = self.get_user_info()
        moment_id = self.get_arg(ARG_MOMENT_ID)
        data = self.get_post_json(KEY_CONTENT, KEY_REPLY_TYPE)
        service.insert_moment_comment(user['uid'], moment_id, data[KEY_REPLY_TYPE], data[KEY_CONTENT])
        self.write(self.ok_pack())

    def get(self, *args, **kwargs):
        index = self.get_index()
        moment_id = self.get_arg(ARG_MOMENT_ID)
        rows = service.select_moment_comment(moment_id, start=index)

        if rows is None:
            rows = []
            
        for r in rows:
            user_id = r['user']
            r['user'] = service.get_user_with(user_id)

        handler_url = self.settings['HOST_COMMENT'] + '?' + ARG_MOMENT_ID + '=%s' % moment_id

        self.write_items(rows, handler_url, index)
