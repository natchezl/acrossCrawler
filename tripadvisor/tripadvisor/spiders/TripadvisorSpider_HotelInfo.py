import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tripadvisor.hotelItem import HotelItem

class TripadvisorSpider_HotelInfo(CrawlSpider):
	name = "TripadvisorSpider_HotelInfo"
	allowed_domains = ["tripadvisor.com"]
	# start_urls = ["http://www.tripadvisor.com/AllLocations-g1066457-c1-Hotels-Shinjuku_Tokyo_Tokyo_Prefecture_Kanto.html"]
	start_urls = ["http://www.tripadvisor.com/AllLocations-g294232-c1-Hotels-Japan.html"]
	global visitedUrlWriter
	visitedUrlWriter = open('info-visitedURL_hotel.txt','w')
	global scoreWriter
	scoreWriter =  open('info-tripadvisorHotelScore.json','w')
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
		
		detail = HotelItem()
		name = response.xpath('//h1[contains(@id,"HEADING")]/text()[normalize-space(.)]').extract()[0].strip()
		title = normalize_titlename(name)
		detail['name'] =  name
		detail['title'] = title

		address = response.xpath('//address')
		a= address.pop()
		full_addr = a.xpath('.//span[contains(@class,"format_address")]/span[descendant-or-self::text()]/text()[normalize-space(.)]').extract()
		# street_addr=  address.xpath('.//span[contains(@class,"street-address")]/text()').extract()
		print '=============================================='
		print full_addr
		# locality_addr = address.xpath('.//span[contains(@class,"locality")]/span/text()').extract()
		# street_addr.extend(locality_addr)
		city = response.xpath('//div[contains(@id , "SECONDARY_NAV_BAR")]/div[contains(@class, "crumbs dark")]/div/ul/li/a[contains(@onclick, "City")]/span/text()').extract()
		detail['address'] = (' ').join(full_addr)
		detail['city'] = city.pop().split('-')[0]
		detail['country'] = 'jp'
		detail['link'] = response.url
		yield detail

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
