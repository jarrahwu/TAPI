from src.handler.funny import FunnyHandler
from test.base import BaseAsyncTest

__author__ = 'jarrah'


class FunnyApiTest(BaseAsyncTest):

    def get_handlers(self):
        self.rs = r"/funny"
        self.path = "/funny"
        return [(self.rs, FunnyHandler)]

    def test_response(self):
        response = self.fetch(self.path)
        self.assert_items_in(response)

        bjo = self.json_decode_body(response)
        self.assertIsNotNone(bjo)

        next_url = self.get_next_url(bjo)
        self.assertIsNotNone(next_url)
        self.on_next(next_url)
