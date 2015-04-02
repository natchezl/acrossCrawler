# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

from tripadvisor.hotelItem import HotelItem
from tripadvisor.hotelScoreItem import HotelScoreItem
from tripadvisor.reviewItem import ReviewItem

class PipelinesMongoDB(object):
	def __init__(self):
		connection = pymongo.Connection(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection_rating = db[settings['MONGODB_COLLECTION_RATING']]
		self.collection_hotelinfo = db[settings['MONGODB_COLLECTION_HOTELINFO']]
		self.collection_review = db[settings['MONGODB_COLLECTION_REVIEW']]

	def process_item(self, item, spider):
		if isinstance(item, HotelItem):
			self.collection_hotelinfo.insert(dict(item))
		elif isinstance(item, HotelScoreItem):
			self.collection_rating.update({'title': item['title'],'source': item['source']}, dict(item), upsert=True)
		elif isinstance(item, ReviewItem):
			self.collection_review.insert(dict(item))
		else :
			raise DropItem()
		return item
