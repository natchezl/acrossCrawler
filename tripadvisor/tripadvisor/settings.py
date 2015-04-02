# -*- coding: utf-8 -*-

# Scrapy settings for tripadvisor project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tripadvisor'

SPIDER_MODULES = ['tripadvisor.spiders']
NEWSPIDER_MODULE = 'tripadvisor.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tripadvisor (+http://www.yourdomain.com)'

# Save item to MongoDB
ITEM_PIPELINES = [
  'tripadvisor.pipelinesMongodb.PipelinesMongoDB',
]

MONGODB_SERVER = "128.199.109.231"
MONGODB_PORT = 9999
MONGODB_DB = "Scrapy_Reviews"
MONGODB_COLLECTION_HOTELINFO = "info"
MONGODB_COLLECTION_RATING = "rating"
MONGODB_COLLECTION_REVIEW = "review"
# MONGO_UNIQUE_KEY = 'title'