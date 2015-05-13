import tornado.web
from tornado.testing import AsyncHTTPTestCase
from src.web.api import FunnyHandler
from tornado.escape import json_decode, json_encode
from urlparse import urlparse

__author__ = 'jarrah'


class FunnyTest(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([('/funny', FunnyHandler)])

    def test_funny_api(self):
        # The following two lines are equivalent to
        response = self.fetch('/funny')
        print(response.body)
        jo = json_decode(response.body)
        self.assertEqual(len(jo), 2)
        self.assertIn("items", jo)
        self.assertIn("links", jo)

        # links
        links = jo['links']
        next_url = None
        for link in links:
            if link['rel'] == "next":
                next_url = link['href']
                break

        print("next url %s" % next_url)
        self.assertIsNotNone(next_url)
        self.on_next(next_url)

    def on_next(self, url):
        parse = urlparse(url)
        print(parse)
        response = self.fetch(parse.path)
        print(response.body)
        jo = json_decode(response.body)
        self.assertEqual(len(jo), 2)
        self.assertIn("items", jo)
        self.assertIn("links", jo)

