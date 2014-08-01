# import urllib2
# from BeautifulSoup import BeautifulSoup
#
# __author__ = 'SOROOSH'
#
#
# class FarsCrawler:
#     def __init(self):
#         self.base_url = 'https://farsnews.com'
#
# 
#     def find_latest_news(self):
#         soup = self._get_soup()
#         last_news_tags = self._get_last_news_tags(soup)
#
#         result = list()
#         for tag in last_news_tags:
#             news = FarsNewsGenerator.from_tag(tag)
#             result.append(news)
#
#         return result
#
#
#     def _get_soup(self):
#         response = urllib2.urlopen('http://farsnews.com')
#         html = response.read()
#         soup = BeautifulSoup(html)
#
#         return soup
#
#
#     def _get_last_news_tags(self, soup):
#         a = soup.find_all('div', {'class': 'topnewsinfo'})
#         return a
#
#
#     def _get_title(self, soup):
#         pass
#
#
# class FarsNewsGenerator:
#     @staticmethod
#     def from_tag(tag):
#         part_1 = tag.find_all('div', {'class': 'newsrotitr'})
#         if len(part_1) > 0:
#             title_1 = part_1[0].string
#         else:
#             title_1 = ""
#         title_2 = tag.find_all('div', {'class': 'topnewsinfotitle'})[0].string
#
#         link = tag.find_all('a')[0].get('href')
#         abstract = tag.find_all('p', {'class': 'newslead'})[0].string
#         if title_1 == '':
#             title = title_2
#         else:
#             title = title_1 + ' : ' + title_2
#
#         return News(title, abstract, link, 'date is not implemented')
#
