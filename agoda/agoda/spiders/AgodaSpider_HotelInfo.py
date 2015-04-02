import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from agoda.hotelItem import HotelItem
import re

class AgodaSpider_HotelInfo(CrawlSpider):
	name = "AgodaSpider_HotelInfo"
	allowed_domains= ["agoda.com"]
	start_urls = ["http://www.agoda.com/country/japan.html"]
	global urlWriter
	urlWriter = open('rating-VisitedGroupURL.txt','w')
	global hotelURLwriter
	hotelURLwriter = open('rating-VisitedHotelURL.txt','w')
	global normalize_titlename
	# rules = [Rule(LinkExtractor(allow=('/hotel')), 'parse_reviewScore')]
	rules = [
		Rule(LinkExtractor(allow=('/region/','/city/'), \
							restrict_xpaths=('//div[contains(@id,"ctl00_ctl00_MainContent_ContentStates_divStates")]')),\
			callback='parse_regionURL' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/hotel/'),\
							restrict_xpaths=('//div[contains(@id,"ctl00_ctl00_Area_areacity_pnlHotelList")]')),\
			callback='parse_hotelURL', \
			follow = 'true'),
		Rule(LinkExtractor(allow=('-jp.html'),\
							restrict_xpaths=('//div[contains(@id,"ctl00_ctl00_Area_areacity_pnlHotelList")]')),\
			callback='parse_regionURL', \
			follow = 'true')
		
	]


	def parse_regionURL(self,response):
		urlWriter.write(response.url +'\n')

	def parse_hotelURL(self, response):
		hotelURLwriter.write(response.url +'\n')
		
		# --Get Hotel Details----------------------------------------------------------------------------------------
		name = response.xpath('//span[contains(@id,"lblHotelName")]/text()').extract().pop()
		title = normalize_titlename(name)

		detail = HotelItem()
		detail['name'] =  name
		detail['title'] = title

		address = response.xpath('//table[contains(@class,"header_hotel")]//p[contains(@class,"fontsmalli sblueboldunder")]/text()[normalize-space(.)]').extract()
		detail['address'] = address[0].strip()[:-1].strip()
		city = response.xpath('//div[contains(@id ,"breadCrumb_nav_breadcrumb")]//table//td/div/a[contains(@href, "/city/")]/span/text()').extract()
		detail['city'] = city[0]
		detail['country'] = 'jp'
		detail['link'] = response.url
		yield detail

		# --Get Hotel Details----------------------------------------------------------------------------------------
		# score = HotelScoreItem()
		# score_box = response.xpath('//table[contains(@id,"tableLoading")]')
		# title = response.xpath('//span[contains(@id,"lblHotelName")]/text()').extract().pop()
		# title = normalize_titlename(title)
		# score['title'] =  title
		# score['source'] = "agoda"
		# score['url'] = response.url
		# if(score_box):
		# 	score['total_score'] = response.xpath('//span[contains(@id,"lblTotalScore")]/text()').extract().pop()
		# 	score['cleanliness'] = response.xpath('//span[contains(@id,"lblHotelCond")]/text()').extract().pop()
		# 	score['comfort'] =  response.xpath('//span[contains(@id,"lblRoomComfort")]/text()').extract().pop()
		# 	score['location'] = response.xpath('//span[contains(@id,"lblLocation")]/text()').extract().pop()
		# 	score['staff'] = response.xpath('//span[contains(@id,"lblStaff")]/text()').extract().pop()
		# 	score['value'] = response.xpath('//span[contains(@id,"lblValueOfMoney")]/text()').extract().pop()
		# 	yield score

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
