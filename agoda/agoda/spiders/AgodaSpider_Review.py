import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from agoda.hotelScoreItem import HotelScoreItem
from agoda.reviewItem import ReviewItem
import re

class AgodaSpider_Review(CrawlSpider):
	name = "AgodaSpider_Review"
	allowed_domains= ["agoda.com"]
	start_urls = ["http://www.agoda.com/country/japan.html"]
	global urlWriter
	urlWriter = open('review-VisitedGroupURL.txt','w')
	global hotelURLwriter
	hotelURLwriter = open('review-VisitedHotelURL.txt','w')
	global hotelnumWriter
	hotelnumWriter = open('review-hotelReviewNum.txt','w')
	global hotelReviewURLwriter
	hotelReviewURLwriter = open('review-hotelReviewURL.txt','w')
	global normalize_titlename
	global isEnglish

	rules = [
		Rule(LinkExtractor(allow=('/region/','/city/'), \
							restrict_xpaths=('//div[contains(@id,"ctl00_ctl00_MainContent_ContentStates_divStates")]')),\
			callback='parse_regionURL' ,\
			follow = 'true'),
		Rule(LinkExtractor(allow=('/hotel/'),\
							restrict_xpaths=('//div[contains(@id,"ctl00_ctl00_Area_areacity_pnlHotelList")]')),\
			callback = 'parse_hotelURL', \
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
		hotel_title = response.xpath('//span[contains(@id,"lblHotelName")]/text()').extract().pop()
		hotel_title = normalize_titlename(hotel_title)
		temp = response.url.split('/')
		temp[4] = 'reviews'
		reviewURL = '/'.join(temp)
		yield scrapy.Request(reviewURL, callback=lambda r:self.parse_review(r,hotel_title))

	def parse_review(self, response,hotel_title):
		hotelReviewURLwriter.write(response.url +'\n')

		# print "======= data " + response.url
		allreview = response.xpath('//div[contains(@id, "ctl00_ctl00_MainContent_ContentMain_HotelReview1_updReviewList")]')
		# print len(allreview.xpath('table[contains(@class,"hotelreviewlist")]').extract())

		baseUrl = response.url
		viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").extract().pop()
		# eventvalidation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract().pop()
		moreReviewBTN = response.xpath('//a[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_btnLoadMoreReview")]').extract()
		if(len(moreReviewBTN)>0):
            # argument =  u"'Page$"+ str(i+1) + u"'"
			# print "+++ call dopostback \n"
			data = {'__EVENTTARGET': 'ctl00$ctl00$MainContent$ContentMain$HotelReview1$btnLoadMoreReview', '__EVENTARGUMENT': '', '__VIEWSTATE': viewstate, '__EVENTVALIDATION': ''}
			currentPage = scrapy.FormRequest(baseUrl, formdata = data, dont_filter = True, callback = lambda r:self.parse_review(r,hotel_title))
			yield currentPage

		else :
			
			allreview = response.xpath('//div[contains(@id, "ctl00_ctl00_MainContent_ContentMain_HotelReview1_updReviewList")]')
			
			# print len(allreview.xpath('table[contains(@class,"hotelreviewlist")]').extract())
			review_num = len(allreview.xpath('table[contains(@class,"hotelreviewlist")]/tr').extract())
			hotel_num = hotel_title + '\t'+ str(review_num)+'\n'
			# print "+++++++++++++++++++++++++++++++++++++++++++++ yield "+ hotel_num
			hotelnumWriter.write(hotel_num)

			for review in allreview.xpath('table[contains(@class,"hotelreviewlist")]/tr') :
				item = ReviewItem()	
				item['title'] = hotel_title
				item['name'] = review.xpath('td/span[contains(@id,"lblMemberName")]/text()').extract()[0]
				
				nationality = review.xpath('.//td/span[contains(@id,"lblMemberNationality")]/text()').extract()
				if(len(nationality)>0):
					item['nationality'] = nationality[0] 
				else: 
					item['nationality'] = ""

				item['travelType'] = review.xpath('.//td/span[contains(@id,"lblTravelerType")]/text()').extract()[0]
				item['reviewDate'] = review.xpath('.//td/span[contains(@id,"lblReviewDate")]/text()').extract()[0]
				topic = [''.join(review.xpath('.//div[contains(@class,"blue fontmediumb")]/text()').extract()).strip()]
				pos = review.xpath('.//div[contains(@id,"trPros")]/span/text()').extract()
				morecomment = review.xpath('.//span[contains(@id,"lblCommentText")]/text()').extract()
				topic.extend(pos)
				topic.extend(morecomment)
				comment = topic

				item['comment'] = comment
				item['rating'] = review.xpath('.//span[contains(@id,"lblGuestRating")]/text()').extract()[0]
				item['source'] = "agoda"

				if isEnglish(comment):
					yield item
				else :
					print 'Drop item contained non-English character....'
					# print item['name']
					# print comment

	def isEnglish(listComment):
		for item in listComment:
			try:
				item.decode('ascii')
			except UnicodeDecodeError:
				# print "*********** non ascii"
				return False
			except UnicodeEncodeError:
				# print "*********** non ascii"
				return False
		# print "****** ascii " + item
		return True

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
