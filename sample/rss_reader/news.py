class News:
    def __init__(self, title, abstract, link, date):
        self.title = title
        self.abstract = abstract
        self.link = link
        self.date = date


    def __unicode__(self):
        return "[title:%s \r\n" \
               " abstract:%s \r\n" \
               "link:%s \r\n" \
               "date:%s" \
               "]" % (self.title, self.abstract, self.link, self.date)

    def __str__(self):
        return self.__unicode__()
