from urlparse import urlparse
import tornado
from tornado.escape import json_decode
from src.tools.app_setting import SETTINGS
__author__ = 'jarrah'
import abc

from tornado.testing import AsyncHTTPTestCase


class BaseAsyncTest(AsyncHTTPTestCase):
    __metaclass__ = abc.ABCMeta

    def get_app(self):
        return tornado.web.Application(self.get_handlers(), **SETTINGS)

    @abc.abstractmethod
    def get_handlers(self):
        pass

    def on_next(self, url):
        parse = urlparse(url)
        response = self.fetch(parse.path + "?" + parse.query)
        print("[on next response :]", response.body)
        print("[parse url :]", parse)
        jo = json_decode(response.body)
        self.assertTrue(len(jo) >= 2)
        self.assertIn("items", jo)
        self.assertIn("links", jo)

    def assert_items_in(self, response):
        jo = json_decode(response.body)
        self.assertIn("items", jo)

    def get_next_url(self, response_json_object):
        links = response_json_object['links']
        next_url = None
        for link in links:
            if link['rel'] == "next":
                next_url = link['href']
                break
        return next_url

    def get_json_body(self, response):
        jo = json_decode(response.body)
        return jo