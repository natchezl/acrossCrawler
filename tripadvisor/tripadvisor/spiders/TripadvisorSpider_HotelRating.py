import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tripadvisor.hotelItem import HotelItem
from tripadvisor.hotelScoreItem import HotelScoreItem

class TripadvisorSpider_HotelRating(CrawlSpider):
	name = "TripadvisorSpider_HotelRating"
	allowed_domains = ["tripadvisor.com"]
	# start_urls = ["http://www.tripadvisor.com/AllLocations-g1066457-c1-Hotels-Shinjuku_Tokyo_Tokyo_Prefecture_Kanto.html"]
	start_urls = ["http://www.tripadvisor.com/AllLocations-g294232-c1-Hotels-Japan.html"]
	global visitedUrlWriter
	visitedUrlWriter = open('rating-visitedURL_hotel.txt','w')
	global scoreWriter
	scoreWriter =  open('rating-tripadvisorHotelScore.json','w')
	global normalize_titlename
	
	# allLoc_xPath  = ['//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@id,"BODYCON")]/div/a']
	# hotelReview_xPath  = ['//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@class,"pgLinks")]/a/@href']
	rules = [
		Rule(LinkExtractor(allow=('/AllLocations-g'), \
							restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@id,"BODYCON")]/div/a')),\
			callback='parse_groupUrl' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/Hotel_Review-g'),\
							restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]')),\
			callback='parse_HotelUrl', \
			follow = 'true')
	]
	print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

	def parse_groupURL(self, response):
		visitedUrlWriter.write(response.url+'\n')

	def parse_HotelUrl(self, response):
		# japan_groupstartNum = 298102

		visitedUrlWriter.write(response.url+'\n')
		
		# --Get Hotel Details----------------------------------------------------------------------------------------
		
		# detail = HotelItem()
		# name = response.xpath('//h1[contains(@id,"HEADING")]/text()[normalize-space(.)]').extract()[0].strip()
		# title = normalize_titlename(name)
		# detail['name'] =  name
		# detail['title'] = title

		# address = response.xpath('//address')
		# a= address.pop()
		# full_addr = a.xpath('.//span[contains(@class,"format_address")]/span[descendant-or-self::text()]/text()[normalize-space(.)]').extract()
		# # street_addr=  address.xpath('.//span[contains(@class,"street-address")]/text()').extract()
		# print '=============================================='
		# print full_addr
		# # locality_addr = address.xpath('.//span[contains(@class,"locality")]/span/text()').extract()
		# # street_addr.extend(locality_addr)
		# city = response.xpath('//div[contains(@id , "SECONDARY_NAV_BAR")]/div[contains(@class, "crumbs dark")]/div/ul/li/a[contains(@onclick, "City")]/span/text()').extract()
		# detail['address'] = (' ').join(full_addr)
		# detail['city'] = city.pop().split('-')[0]
		# detail['country'] = 'jp'
		# detail['link'] = response.url
		# yield detail

		# --Get Hotel Details----------------------------------------------------------------------------------------
		score_box = response.xpath('//div[contains(@id,"SUMMARYBOX")]')
		score = HotelScoreItem()
		
		if(score_box):
			score['title'] = title
			score['source'] = "tripadvisor"
			score['url'] = response.url
			# score['review_num'] = response.xpath('//div[contains(@class,"locationContent")]/div[contains(@class,"userRating")]/div/a/span/text()').extract()
			score['total_score'] = response.xpath('//div[contains(@class,"userRating")]/div/span/img/@content').extract().pop()
			cleanliness = score_box.xpath('.//ul/li[contains(.//div/text(), "Cleanliness")]/span/img/@alt')
			if(cleanliness):
				score['cleanliness'] = cleanliness.extract()[0].split(' ')[0]
			
			comfort = score_box.xpath('.//ul/li[contains(.//div/text(), "Sleep Quality")]/span/img/@alt')
			if(comfort):
				score['comfort'] = comfort.extract()[0].split(' ')[0]  
			
			location = score_box.xpath('.//ul/li[contains(.//div/text(), "Location")]/span/img/@alt')
			if(location):
				score['location'] = location.extract()[0].split(' ')[0]
			
			staff = score_box.xpath('.//ul/li[contains(.//div/text(), "Service")]/span/img/@alt')
			if(staff):
				score['staff'] = staff.extract()[0].split(' ')[0] 
			
			value = score_box.xpath('.//ul/li[contains(.//div/text(), "Value")]/span/img/@alt')
			if(value):
				score['value'] = value.extract()[0].split(' ')[0]

		# scoreWriter.write(score)

			yield score

	def normalize_titlename (title):
		title = title.split('(')[0]
		title = title.lower()
		title = title.replace('hotel','')
		title = title.replace(' ','')
		title = title.replace('-','')
		title = title.replace('&','and')
		title = title.replace(',','')
		title = title.replace('.','')
		title = title.replace('\'','')
		title = title.replace('northexit','kitaguchi')
		title = title.replace('southexit','minamiguchi')
		title = title.replace('eastexit','higashiguchi')
		title = title.replace('westexit','nishiguchi')
		title = re.sub(r'station\b', 'ekimae', title)
		title = title.replace('station', 'eki')
		title = title.replace('no1','1')
		title = title.replace('no2','2')  
		return title
