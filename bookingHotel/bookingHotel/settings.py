# -*- coding: utf-8 -*-

# Scrapy settings for bookingHotel project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bookingHotel'

SPIDER_MODULES = ['bookingHotel.spiders']
NEWSPIDER_MODULE = 'bookingHotel.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bookingHotel (+http://www.yourdomain.com)'
ITEM_PIPELINES = [
  'bookingHotel.pipelinesMongodb.PipelinesMongoDB',
]

MONGODB_SERVER = "128.199.109.231"
MONGODB_PORT = 9999
MONGODB_DB = "Scrapy_Reviews"
MONGODB_COLLECTION_HOTELINFO = "info"
MONGODB_COLLECTION_RATING = "rating"
MONGODB_COLLECTION_REVIEW = "review"