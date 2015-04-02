import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bookingHotel.reviewItem import ReviewItem
import re

class BookingSpider_Review(CrawlSpider):
	name = "BookingSpider_Review"
	allowed_domains= ["booking.com"]
	start_urls = ["http://www.booking.com/destination/country/jp.html?sid=e46be3f9268c509c0d5b178d23d0db56;dcid=4"]
	global urlWriter
	urlWriter = open('review-visitedURL.txt','w')
	global reviewURLwriter
	reviewURLwriter = open('review-visitedReview.txt','w')
	global normalize_titlename
	global isEnglish

	rules = [
		Rule(LinkExtractor(allow=('/destination/city/jp/'), \
							restrict_xpaths=('//div[contains(@class,"deslast")]/table[1]')),\
			callback='parse_groupURL' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/hotel/jp'),\
							restrict_xpaths=('//div[contains(@class,"deslast")]/table')),\
			callback='parse_reviewURL', \
			follow = 'false')
	]

	
	def parse_groupURL(self,response):
		urlWriter.write(response.url +'\n')


	def parse_reviewURL(self, response):
		urlWriter.write(response.url +'\n')
		pagename = response.url.split('/')[-1].split('.')[0]
		# pagename = response.xpath('//option[contains(@data-customer-type, "total")]/@data-pagename').extract()[0]
		review_numTmp = response.xpath('//option[contains(@data-customer-type, "total")]/@data-quantity').extract()
		if(len(review_numTmp)>0):
			review_num = review_numTmp[0]
			print pagename, review_num
			offset_num =0

			while (offset_num < int(review_num)):
				url= "http://www.booking.com/reviewlist.en-gb.html?dcid=4;cc1=jp;dist=1;pagename=%s;type=total&;offset=%s;rows=99" %(pagename,offset_num)

				print "downloading %s" %url
				# urlWriter.write(url)
				# urlWriter.write("\n")
				hotel_title = response.xpath('//span[contains(@id, "hp_hotel_name")]/text()').extract()[0]
				hotel_title = normalize_titlename (hotel_title)


				yield scrapy.Request( url, \
			        headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
			                 'Accept-Encoding': 'gzip,deflate,sdch',\
			                 'Accept-Language': 'th,en-US;q=0.8,en;q=0.6',\
			                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'\
			                 'Cache-Control: max-age=0',\
			                 },\
			        callback=lambda r:self.parse_reviewScore(r,hotel_title)\
			    )
				offset_num += 99

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

	def parse_reviewScore(self, response, title):
		reviewURLwriter.write(response.url + '\n')

		for review in response.xpath('//ul[contains(@class,"review_list")]/li'):
			item = ReviewItem()	
			item['title'] = title		
			item['name'] = review.xpath('div[contains(@class,"review_item_reviewer")]/h4/text()').extract()[0].strip('\n')
			item['nationality'] = review.xpath('div[contains(@class,"review_item_reviewer")]/span[contains(@class,"reviewer_country")]/text()').extract()[1].strip('\n')
			item['travelType'] = review.xpath('div[contains(@class,"review_item_review")]//ul[contains(@class,"review_item_info_tags")]/li/text()').extract()
			item['reviewDate'] = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_header_date")]/text()').extract()[1].strip('\n')
			comment = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_header_content_container")]/div[contains(@class,"review_item_header_content")]/text()').extract()
			pos = review.xpath('.//div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_content")]/p[contains(@class,"review_pos")]/text()').extract()
			neg = review.xpath('.//div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_content")]/p[contains(@class,"review_neg")]/text()').extract()
			comment.extend(pos)
			comment.extend(neg)
			comment[0] = comment[0].strip()
			# print comment

			item['comment'] = comment
			item['rating'] = review.xpath('div[contains(@class,"review_item_review")]//div[contains(@class,"review_item_review_score")]/text()').extract()[0].strip('\n')
			item['source'] = "booking"
			# print item,"\n";
			# yield item
			if isEnglish(comment):
					yield item
			else :
				print 'Drop item contained non-English character....'
				# print comment

	def isEnglish(listComment):
		for item in listComment:
			try:
				item.decode('ascii')
			except UnicodeDecodeError:
				return False
			except UnicodeEncodeError:
				return False
		return True