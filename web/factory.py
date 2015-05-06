from db import service

__author__ = 'jarrah'


def gen_link_obj(rel, href):
    link = dict()
    link['rel'] = rel
    link['href'] = href

class APK:
    def get_items(self):
        items = []
        for i in range(10):
            item = dict()
            item['title'] = "title NO.%d" % i
            item['size'] = "%dMB" % i
            items.append(item)
        return items

    def get_links(self):
        links = []
        link = dict()
        link['rel'] = "next"
        link['href'] = "http://192.168.17.132:8888/apks"
        links.append(link)
        return links

    def create(self):
        apk = dict()
        apk['items'] = self.get_items()
        apk['links'] = self.get_links()
        return apk

class FUNY:
    def get_items(self):
        news = service.get_news()

        funny = dict()
        funny["items"] = news

        links = list()
        links.append(gen_link_obj("next", "http://192.168.2.140:8888/funny"))
        funny["links"] = links

        return news