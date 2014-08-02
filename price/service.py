import urllib
import json

__author__ = 'SOROOSH'


class PriceCrawler:
    def read_gold_price(self):
        url = urllib.urlopen('http://www.tala.ir/webservice/price_live.php?mode=ajax&nocache=1')
        response = url.readline()
        obj = json.loads(response)
        return obj


if __name__ == '__main__':
    c = PriceCrawler()
    result = c.read_gold_price()
    for a in result:
        print "%s : %s" % (a, result[a])