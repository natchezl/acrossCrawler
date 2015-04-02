import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tripadvisor.reviewItem import ReviewItem

class TripadvisorSpider_eachReview(CrawlSpider):
	name = "tripadvisorSpider_eachReview"
	allowed_domains = ["tripadvisor.com"]
	start_urls = ["http://www.tripadvisor.com/AllLocations-g1066457-c1-Hotels-Shinjuku_Tokyo_Tokyo_Prefecture_Kanto.html"]
	global f
	f= open('textCrawl.txt', 'w')
	global visitedUrlWriter
	visitedUrlWriter = open('visitedURL.txt','w')
	global visitedExpandedUrlWriter
	visitedExpandedUrlWriter = open('visitedExpandedReview.txt','w')
	# global review_dict
	# review_dict = {}
	# global review_set
	# review_set = set()
	rules = [
		Rule(LinkExtractor(allow=('/Hotel_Review-g1066457-d301381')),\
			callback='parse_url', \
			follow = 'true'),
	]
	print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	# f.write(review_dict)

	def parse_url(self, response):
		# filename = response.url.split("/")[-2]
		# with open(filename, 'wb') as f:
		visitedUrlWriter.write(response.url+'\n')
		# print response.url+'\n'
		# heading= response.xpath('//h1[re:test(@id, "HEADING$")]/text()').extract()
		# data= response.xpath('//div[contains(@class,"quote")]/a[contains(@href, "/ShowUserReviews")]/@href').extract()
		data= response.xpath('//a[contains(@href, "/ShowUserReviews")]/@href').extract()
		print "+++++data[0]++++++++ "+data[0]+'\n'
		# f.write(heading+'\n')
		
		g = re.search('g[\d]{4,}',data[0])
		g= g.group(0)
		d = re.search('d[\d]{4,}',data[0])
		d = d.group(0)
		r= re.search('r[\d]{1,}',data[0])
		# first_review_no =r.group(0)[1:].rstrip()
		# review_list = set()

		for a in data:
			
			# groupDG = [g,d]
			r= re.search('r[\d]{1,}',a)
			review_no =r.group(0)[1:].rstrip()

			hotel_title = data[0].split('-')[-2]
			# review_dict[review_no]= d

			# f.write('http://www.tripadvisor.com/ExpandedUserReviews-%s-%s?target=%s&context=1&reviews=%s&servlet=Hotel_Review\n' %(g,d,review_no,review_no))
			
			url ='http://www.tripadvisor.com/ExpandedUserReviews-%s-%s?target=%s&context=1&reviews=%s&servlet=Hotel_Review' %(g,d,review_no,review_no)
			# review_list.add(review_no)
			f.write(review_no+'\n')
			yield scrapy.Request(url, callback=lambda r:self.parse_data(r,hotel_title))


		# review_list_string= ','.join(review_list)
		# review_list_string = review_list_string[1:]
		# f.write(review_list_string+'\n')
		# print '========================================\n'
		# print(review_dict)
		# print(review_set)
		# print '\n'

		# print "========"+review_list_string+'\n'
		# url= 'http://www.tripadvisor.com/ExpandedUserReviews-%s-%s?target=%s&context=1&reviews=%s&servlet=Hotel_Review' %(g,d,first_review_no,review_list_string)
		# yield scrapy.Request(url, callback=lambda r:self.parse_data(r,hotel_title))

	def parse_data(self,response,title):
		visitedExpandedUrlWriter.write(response.url+'\n')

		for review in response.xpath('//div[contains(@id,"expanded_review")]'):
			item = ReviewItem()
			item['title'] = [title]
			item['name'] = review.xpath('.//span[contains(@class,"scrname")]/text()').extract()
			item['nationality'] = review.xpath('.//div[contains(@class,"location")]/text()').extract()
			item['travelType'] = review.xpath('.//span[contains(@class,"recommend-titleInline")]/text()').extract()[0].split(',')[1]
			item['reviewDate'] = review.xpath('.//span[contains(@class,"ratingDate")]/text()').extract()[0][9:].rstrip()
			item['comment'] = review.xpath('.//div[contains(@class,"entry")]/p/text()').extract()
			item['rating'] = review.xpath('.//img[contains(@class,"rating_s_fill")]/@alt').extract()[0][0:1].rstrip()
			item['source'] = ["tripadvisor"]
			# print item,"\n"
			yield item