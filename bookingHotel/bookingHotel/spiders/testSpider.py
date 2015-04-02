import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bookingHotel.hotelScoreItem import HotelScoreItem
from bookingHotel.reviewItem import ReviewItem
import re

class testSpider(scrapy.Spider):
	name = "testSpider"
	allowed_domains= ["booking.com"]
	start_urls = ["http://www.booking.com/hotel/jp/toyoko-inn-okhotsk-abashiri-ekimae.th.html?sid=5a4dfd1bed5d171faa6e016829274896;dcid=4#tab-reviews"]
	global urlWriter
	urlWriter = open('testVisitedURL.txt','w')
	# rules = [Rule(LinkExtractor(allow=('/hotel')), 'parse')]

	def parse(self, response):
		urlWriter.write(response.url +'\n')
		pagename = response.xpath('//option[contains(@data-customer-type, "total")]/@data-pagename').extract()[0]
		review_num = response.xpath('//option[contains(@data-customer-type, "total")]/@data-quantity').extract()[0]
		# if(line['title']):
		# title = line['title'][0]
		# review_num = line['review_num'][0]

		print pagename, review_num
		offset_num =0

		while (offset_num < int(review_num)):
			url= "http://www.booking.com/reviewlist.en-gb.html?dcid=4;cc1=jp;dist=1;pagename=%s;type=total&;offset=%s;rows=99" %(pagename,offset_num)

			print "downloading %s" %url
			# urlWriter.write(url)
			# urlWriter.write("\n")

			yield scrapy.Request( url, \
		        headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
		                 'Accept-Encoding': 'gzip,deflate,sdch',\
		                 'Accept-Language': 'th,en-US;q=0.8,en;q=0.6',\
		                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'\
		                 'Cache-Control: max-age=0',\
		                 },\
		        callback=self.parse_reviewScore
	    )

			offset_num += 99

	def parse_reviewScore(self, response):
		urlWriter.write(response.url + '\n')

		for review in response.xpath('//ul[contains(@class,"review_list")]/li'):
			item = ReviewItem()			
			item['name'] = review.xpath('div[contains(@class,"review_item_reviewer")]/h4/text()').extract()
			item['nationality'] = review.xpath('div[contains(@class,"review_item_reviewer")]/span[contains(@class,"reviewer_country")]/text()').extract()
			item['travelType'] = review.xpath('div[contains(@class,"review_item_review")]//ul[contains(@class,"review_item_info_tags")]/li/text()').extract()
			item['reviewDate'] = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_header_date")]/text()').extract()
			pos = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_content")]/p[contains(@class,"review_pos")]/text()').extract()
			neg = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_content")]/p[contains(@class,"review_neg")]/text()').extract()

			item['comment'] = [pos,neg]
			item['rating'] = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_score")]/text()').extract()
			item['source'] = "booking"
			# print item,"\n";
			yield item
