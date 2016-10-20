# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyPostspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    title = scrapy.Field()
    writer = scrapy.Field()
    read = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
    pass
