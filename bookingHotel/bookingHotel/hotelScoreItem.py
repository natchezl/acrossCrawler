# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelScoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    total_score = scrapy.Field()
    cleanliness = scrapy.Field()
    comfort = scrapy.Field()
    location = scrapy.Field()
    staff = scrapy.Field()
    value  = scrapy.Field()
    url = scrapy.Field()
