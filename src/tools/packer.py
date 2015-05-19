__author__ = 'jarrah'
'''
data response packer
'''

'''
link obj item pattern
'''


def gen_link_obj(rel, href):
    link = dict()
    link['rel'] = rel
    link['href'] = href
    return link


'''
client ListView array pattern
'''


def dump_list_view_pack(rows, *args):
    pack = dict()
    pack['items'] = rows
    pack['links'] = args
    return pack