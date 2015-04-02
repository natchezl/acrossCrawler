import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bookingHotel.hotelItem import HotelItem
import re

class BookingSpider_HotelInfo(CrawlSpider):
	name = "BookingSpider_HotelInfo"
	allowed_domains= ["booking.com"]
	start_urls = ["http://www.booking.com/destination/country/jp.html?sid=e46be3f9268c509c0d5b178d23d0db56;dcid=4"]
	global urlWriter
	urlWriter = open('info-VisitedGroupURL.txt','w')
	global hotelURLwriter
	hotelURLwriter = open('info-VisitedHotelURL.txt','w')
	global normalize_titlename

	rules = [
		Rule(LinkExtractor(allow=('/destination/city/jp/'), \
							restrict_xpaths=('//div[contains(@class,"deslast")]/table[1]')),\
			callback='parse_groupURL' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/hotel/jp'),\
							restrict_xpaths=('//div[contains(@class,"deslast")]/table')),\
			callback='parse_reviewURL', \
			follow = 'true')
	]

	def parse_groupURL(self,response):
		urlWriter.write(response.url +'\n')

	def parse_reviewURL(self, response):
		hotelURLwriter.write(response.url +'\n')
		filename = response.url.split("/")[-1]
		filename = filename.split(".")[0]

		# for sel in response.xpath('//div[contains(@data-tab,"reviews")]'):
		name = response.xpath('//span[contains(@id, "hp_hotel_name")]/text()').extract()[0]
		title = normalize_titlename(name)

		# --Get Hotel Details----------------------------------------------------------------------------------------
		
		detail = HotelItem()
		detail['name'] =  name
		detail['title'] = title

		address = response.xpath('//span[contains(@id, "hp_address_subtitle")]/text()').extract()
		detail['address'] = address.pop().strip()
		cityTemp = response.xpath('//div[contains(@id, "subheader-wrap")]/div/div[contains(@data-google-track, "city")]/a/text()').extract()
		city= cityTemp.pop().split(' ')
		detail['city'] = city[0].lower()
		detail['country'] = 'jp'
		detail['link'] = response.url
		yield detail

		# ==== Get Hotel Rating ===============================================================================
		# item = HotelScoreItem()
		# item['title'] = titlename
		# item['source'] = 'booking'
		# item['url'] = response.url
		# # item['review_num'] = response.xpath('//option[contains(@data-customer-type, "total")]/@data-quantity').extract()
			
		# sel = response.xpath('//div[contains(@data-tab,"reviews")]')
		# total_score = sel.xpath('.//div[contains(@class, "review_list_score")]/@data-total').extract()
		# if(len(total_score)>0):
		# 	item['total_score'] = total_score[0]
		# 	item['cleanliness'] =  sel.xpath('.//ul[contains(@class, "review_score_breakdown_list")]/@data-total_hotel_clean').extract()[0]
		# 	item['comfort'] = sel.xpath('.//ul[contains(@class, "review_score_breakdown_list")]/@data-total_hotel_comfort').extract()[0]
		# 	item['location'] = sel.xpath('.//ul[contains(@class, "review_score_breakdown_list")]/@data-total_hotel_location').extract()[0]
		# 	item['staff'] = sel.xpath('.//ul[contains(@class, "review_score_breakdown_list")]/@data-total_hotel_staff').extract()[0]
		# 	item['value'] = sel.xpath('.//ul[contains(@class, "review_score_breakdown_list")]/@data-total_hotel_value').extract()[0]
		# 	# print item
		# 	yield item

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
