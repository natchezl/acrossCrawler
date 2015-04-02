import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re

class TripadvisorSpider(CrawlSpider):
	name = "tripadvisorSpider"
	allowed_domains = ["tripadvisor.com"]
	start_urls = ["http://www.tripadvisor.com/AllLocations-g294232-c1-Hotels-Japan.html"]
	global f
	f= open('textCrawl.txt', 'w')
	global urlWriter
	urlWriter = open('visitedURL.txt','w')
	global parse_data_writer
	parse_data_writer = open('visitedExpandedReview.txt','w')
	global review_dict
	review_dict = {}
	global review_set
	review_set = set()
	rules = [
		Rule(LinkExtractor(allow=('/Hotel_Review-g1066457-d301381')),\
			callback='parse_url', \
			follow = 'true'),
	]