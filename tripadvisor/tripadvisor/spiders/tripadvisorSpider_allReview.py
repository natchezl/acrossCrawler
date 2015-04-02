import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tripadvisor.reviewItem import ReviewItem

class TripadvisorSpider_allReview(CrawlSpider):
	name = "tripadvisorSpider_allReview"
	allowed_domains = ["tripadvisor.com"]
	# start_urls = ["http://www.tripadvisor.com/AllLocations-g1066457-c1-Hotels-Shinjuku_Tokyo_Tokyo_Prefecture_Kanto.html"]
	start_urls = ["http://www.tripadvisor.com/AllLocations-g294232-c1-Hotels-Japan.html"]
	global f
	f= open('textCrawl.txt', 'w')
	global visitedUrlWriter
	visitedUrlWriter = open('visitedURL.txt','w')
	global visitedExpandedUrlWriter
	visitedExpandedUrlWriter = open('visitedExpandedReview.txt','w')

	
	# allLoc_xPath  = ['//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@id,"BODYCON")]/div/a']
	# hotelReview_xPath  = ['//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@class,"pgLinks")]/a/@href']
	rules = [
		Rule(LinkExtractor(allow=('/AllLocations-g'), \
							restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@id,"BODYCON")]/div/a')),\
			callback='parse_groupUrl' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/Hotel_Review-g'),\
							restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]','//div[contains(@class,"pgLinks")]/a')),\
			callback='parse_HotelUrl', \
			follow = 'true')

		# Rule(LinkExtractor(allow=('/AllLocations-g'), \
		# 					restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]',)),\
		# 	callback='parse_groupUrl' ,\
		# 	follow = 'true'),
		# Rule(LinkExtractor(allow=('/AllLocations-g'), \
		# 					restrict_xpaths=('//div[contains(@id,"BODYCON")]/div/a',)),\
		# 	callback='parse_groupUrl' ,\
		# 	follow = 'true'),

		# Rule(LinkExtractor(allow=('/Hotel_Review-g'),\
		# 					restrict_xpaths=('//div[contains(@id,"BODYCON")]/table[1]')),\
		# 	callback='parse_HotelUrl', \
		# 	follow = 'true'),
		# Rule(LinkExtractor(allow=('/Hotel_Review-g'),\
		# 					restrict_xpaths=('//div[contains(@class,"pgLinks")]/a/@href')),\
		# 	callback='parse_HotelUrl', \
		# 	follow = 'true')
	]
	print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

	def parse_groupURL(self, response):
		visitedUrlWriter.write(response.url+'\n')

	def parse_HotelUrl(self, response):
		# japan_groupstartNum = 298102

		visitedUrlWriter.write(response.url+'\n')

		#---Get Each Review Details-----------------------------------------------------------------------------------
		data= response.xpath('//a[contains(@href, "/ShowUserReviews")]/@href').extract()
		if(data):
			# print "+++++data[0]++++++++ "+data[0]+'\n'

			g = re.search('g[\d]{4,}',data[0])
			g= g.group(0)
			groupnum= g[1:].rstrip()

			# if(int(groupnum)>japan_groupstartNum):
				
			d = re.search('d[\d]{4,}',data[0])
			d = d.group(0)
			r= re.search('r[\d]{1,}',data[0])
			first_review_no =r.group(0)[1:].rstrip()
			review_list = set()

			for a in data:

				r= re.search('r[\d]{1,}',a)
				review_no =r.group(0)[1:].rstrip()

				# hotel_title = data[0].split('-')[-2]
				hotel_title = response.xpath('//h1[contains(@id,"HEADING")]/text()[normalize-space(.)]').extract()[0].strip();
				# url ='http://www.tripadvisor.com/ExpandedUserReviews-%s-%s?target=%s&context=1&reviews=%s&servlet=Hotel_Review' %(g,d,review_no,review_no)
				review_list.add(review_no)
				# f.write(review_no+'\n')
				# yield scrapy.Request(url, callback=lambda r:self.parse_ReviewData(r,hotel_title))


			review_list_string= ','.join(review_list)
			f.write(review_list_string+'\n')

			url= 'http://www.tripadvisor.com/ExpandedUserReviews-%s-%s?target=%s&context=1&reviews=%s&servlet=Hotel_Review' %(g,d,first_review_no,review_list_string)
			yield scrapy.Request(url, callback=lambda r:self.parse_ReviewData(r,hotel_title))

	def parse_ReviewData(self,response,title):
		visitedExpandedUrlWriter.write(response.url+'\n')

		for review in response.xpath('//div[contains(@id,"expanded_review")]'):
			item = ReviewItem()
			item['title'] = title
			name = review.xpath('.//span[contains(@class,"scrname")]/text()').extract()
			if(len(name)>=1):
				item['name'] = name[0]
				item['nationality'] = review.xpath('.//div[contains(@class,"location")]/text()').extract()[0]
				
				travelType = review.xpath('.//span[contains(@class,"recommend-titleInline")]/text()').extract()
				if(len(travelType)>0):
					item['travelType'] = travelType[0].split(',')[1]
				else: item['travelType'] = ""
				
				item['reviewDate'] = review.xpath('.//span[contains(@class,"ratingDate")]/text()').extract()[0][9:].rstrip()
				item['comment'] = review.xpath('.//div[contains(@class,"entry")]/p/text()').extract()

				rating = review.xpath('.//img[contains(@class,"rating_s_fill")]/@alt').extract()
				if(len(rating)>0):
					item['rating'] = rating[0][0:1].rstrip()
				else: item['rating'] = ""

				item['source'] = "tripadvisor"
				# print item,"\n"
				yield item