from db import service

__author__ = 'jarrah'


def gen_link_obj(rel, href):
    link = dict()
    link['rel'] = rel
    link['href'] = href
    return link


def dump_pack(rows, *args):
    pack = dict()
    pack['items'] = rows
    pack['links'] = args
    return pack


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
        rows = service.get_funny()
        next_link = gen_link_obj("next", "http://192.168.2.140:8888/funny")
        home_link = gen_link_obj("next", "http://192.168.2.140:8888/apks")
        funny = dump_pack(rows, next_link, home_link)
        return funny





