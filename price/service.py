import logging
import urllib
import json

from price.models import Price


__author__ = 'SOROOSH'
import jdatetime


class PriceCrawler:
    def read_tala_price(self):
        url = urllib.urlopen('http://www.tala.ir/webservice/price_live.php?mode=ajax&nocache=1')
        response = url.readline()
        obj = json.loads(response)
        result = {}
        result['ounce'] = obj['ounce'].replace(',', '')
        result['18gram'] = obj['geram18'].replace(',', '')
        result['24gram'] = obj['geram24'].replace(',', '')
        result['coin-old'] = obj['sekke-gad'].replace(',', '')
        result['coin-new'] = obj['sekke-jad'].replace(',', '')
        result['coin-half'] = obj['sekke-nim'].replace(',', '')
        result['coin-quarter'] = obj['sekke-rob'].replace(',', '')
        result['coin-1g'] = obj['sekke-grm'].replace(',', '')
        result['usd'] = obj['dolar-tafavot'].replace(',', '')
        result['silver'] = obj['silver'].replace(',', '')
        result['oil'] = obj['oil'].replace(',', '')
        d = obj['dateam'].replace('93/', '1393/')

        update_date = jdatetime.datetime.strptime(d[8:], '%H:%M:%S %Y/%m/%d').togregorian()

        return result, update_date


price_logger = logging.getLogger("price_scheduler")


def update_prices():
    price_logger.info("Updating prices...")
    c = PriceCrawler()
    result, up_date = c.read_tala_price()

    for a in result:
        if not Price.objects.filter(item__name=a).exists():
            p = Price()
            p.date = up_date
            p.price = result[a]
            p.item_id = a
            p.save()
            price_logger.info("Price: %s saved" % p.item.name)

        else:
            p = Price.objects.filter(item__name=a).first()
            if p.date.day == up_date.day:
                p.date = up_date
                p.price = result[a]
                p.save()
                price_logger.info("Price: %s updated" % p.item.name)
            else:
                p = Price()
                p.date = up_date
                p.price = result[a]
                p.item_id = a
                p.save()
                price_logger.info("Price: %s saved" % p.item.name)

    price_logger.info("Updating finished.")
