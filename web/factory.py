__author__ = 'jarrah'


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
