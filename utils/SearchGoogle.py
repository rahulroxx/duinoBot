'''
Search google for top results
'''
import chatvoice
from googlesearch import GoogleSearch


def SearhcGoogle(string):
    gs = GoogleSearch(string)
    for hit in gs.top_results():
        # send(hit[u'content'])
        chatvoice(hit[u'content'])
