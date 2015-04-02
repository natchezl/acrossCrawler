import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
# from agoda.hotelItem import HotelItem
from agoda.hotelScoreItem import HotelScoreItem

class TestAgodaSpider_HotelRating(CrawlSpider):
	name = "TestAgodaSpider_HotelRating"
	allowed_domains = ["tripadvisor.com"]
	# start_urls = ["http://www.tripadvisor.com/AllLocations-g1066457-c1-Hotels-Shinjuku_Tokyo_Tokyo_Prefecture_Kanto.html"]
	start_urls = ["http://www.agoda.com/apa-hotel-roppongi-itchome-ekimae/reviews/tokyo-jp.html"]
	# global urlWriter
	# urlWriter = open('testHotelRating-VisitedGroupURL.txt','w')
	# global hotelURLwriter
	# hotelURLwriter = open('testHotelRating-VisitedHotelURL.txt','w')

	# rules = [
	# 	Rule(LinkExtractor(allow=('/AllLocations-g'), \
	# 						restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@id,"BODYCON")]/div/a')),\
	# 		callback='parse_groupUrl' ,\
	# 		follow = 'true'),
	# 	Rule(LinkExtractor(allow=('/Hotel_Review-g'),\
	# 						restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]')),\
	# 		callback='parse_HotelUrl', \
	# 		follow = 'true')
	# ]
	# print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

	# def parse_groupURL(self, response):
	# 	visitedUrlWriter.write(response.url+'\n')

	def parse(self, response):
		# japan_groupstartNum = 298102

		# visitedUrlWriter.write(response.url+'\n')

		# --Get Hotel Details----------------------------------------------------------------------------------------
		
		# detail = HotelItem()
		# name = response.xpath('//h1[contains(@id,"HEADING")]/text()[normalize-space(.)]').extract()[0].strip()
		# detail['name'] =  [name]
		# detail['title'] = response.url.split('/')[-1]

		# address = response.xpath('//div[contains(@class,"infoBox")]/address')
		# street_addr=  address.xpath('.//span[contains(@class,"street-address")]/text()').extract()
		# locality_addr = address.xpath('.//span[contains(@class,"locality")]/span/text()').extract()
		# detail['address'] = street_addr.extend(locality_addr)
		# detail['city'] = locality_addr[0]
		# detail['country'] = ['jp']
		# detail['link'] = [response.url]

		# --Get Hotel Details----------------------------------------------------------------------------------------
		score = HotelScoreItem()
		score_box = response.xpath('//table[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_tableLoading")]')
		score['title'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_hotelheader1_lblHotelName")]/text()').extract().pop()
		score['source'] = "agoda"
		if(score_box):
			score['total_score'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblTotalScore")]/text()').extract().pop()
			score['cleanliness'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblHotelCond")]/text()').extract().pop()
			score['comfort'] =  response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblRoomComfort")]/text()').extract().pop()
			score['location'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblLocation")]/text()').extract().pop()
			score['staff'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblStaff")]/text()').extract().pop()
			score['value'] = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_lblValueOfMoney")]/text()').extract().pop()

		# scoreWriter.write(score)

		yield score
