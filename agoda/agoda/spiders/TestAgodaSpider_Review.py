import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from agoda.hotelScoreItem import HotelScoreItem
from agoda.reviewItem import ReviewItem
import re

class TestAgodaSpider_Review(scrapy.Spider):
	name = "TestAgodaSpider_Review"
	allowed_domains= ["agoda.com"]
	# start_urls = ["http://www.agoda.com/apa-hotel-roppongi-itchome-ekimae/reviews/tokyo-jp.html?asq=5iOgMXvfwD0ZUPUhUZ3dXVfdtOi7b2wr%2bSfzJbMiF%2fLvq3u2CWL%2fqSgfMSSIItCEctSW%2bV9nAHoxbB%2brCc2FmpkWPmorhKaCX2mstAUJpae3NFdaTYjHQ7yd6BEt9yDhCNnR9DUaHOZhkxROSPDsPmztg4WLU7veiC04lypjyKDi9gFJ3zoRUUxA1bXicT8i"]
	global urlWriter
	urlWriter = open('testVisitedURL.txt','w')
	# rules = [Rule(LinkExtractor(allow=('/hotel')), 'parse')]

	def start_requests(self):
		baseUrl = "http://www.agoda.com/apa-hotel-roppongi-itchome-ekimae/reviews/tokyo-jp.html"
		SearchPage = scrapy.Request(baseUrl, callback = lambda r:self.parse_review(r,''))
		return [SearchPage]

	def parse_review(self, response,hotel_title):
		# sel = Selector(response)
		print "======= data \n"
		allreview = response.xpath('//div[contains(@id, "ctl00_ctl00_MainContent_ContentMain_HotelReview1_updReviewList")]')
		print len(allreview.xpath('table[contains(@class,"hotelreviewlist")]').extract())

		title = response.xpath('//span[contains(@id,"ctl00_ctl00_MainContent_ContentMain_hotelheader1_lblHotelName")]/text()').extract()
		print len(title)
		print title
		if(len(title)>0): 
			hotel_title = title.pop()
		print hotel_title

		baseUrl = "http://www.agoda.com/apa-hotel-roppongi-itchome-ekimae/reviews/tokyo-jp.html"
		viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").extract().pop()
		# eventvalidation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract().pop()
		moreReviewBTN = response.xpath('//a[contains(@id,"ctl00_ctl00_MainContent_ContentMain_HotelReview1_btnLoadMoreReview")]').extract()
		if(len(moreReviewBTN)>5):
            # argument =  u"'Page$"+ str(i+1) + u"'"
			print "+++ call dopostback \n"
			data = {'__EVENTTARGET': 'ctl00$ctl00$MainContent$ContentMain$HotelReview1$btnLoadMoreReview', '__EVENTARGUMENT': '', '__VIEWSTATE': viewstate, '__EVENTVALIDATION': ''}
			currentPage = scrapy.FormRequest(baseUrl, formdata = data, dont_filter = True, callback = lambda r:self.parse_review(r,hotel_title))
			yield currentPage

		else :
			print "======= data \n"
			allreview = response.xpath('//div[contains(@id, "ctl00_ctl00_MainContent_ContentMain_HotelReview1_updReviewList")]')
			print len(allreview.xpath('table[contains(@class,"hotelreviewlist")]').extract())
			print len(allreview.xpath('table[contains(@class,"hotelreviewlist")]/tr').extract())


			for review in allreview.xpath('table[contains(@class,"hotelreviewlist")]/tr') :
				item = ReviewItem()	
				item['title'] = hotel_title
				item['name'] = review.xpath('td/span[contains(@id,"lblMemberName")]/text()').extract()[0]
				item['nationality'] = review.xpath('.//td/span[contains(@id,"lblMemberNationality")]/text()').extract()[0]
				item['travelType'] = review.xpath('.//td/span[contains(@id,"lblTravelerType")]/text()').extract()[0]
				item['reviewDate'] = review.xpath('.//td/span[contains(@id,"lblReviewDate")]/text()').extract()[0]
				topic = ''.join(map(unicode.strip, review.xpath('.//div[contains(@class,"blue fontmediumb")]/text()').extract()))
				pos = ''.join(map(unicode.strip, review.xpath('.//div[contains(@id,"trPros")]/span/text()').extract()))
				comment = ''.join(map(unicode.strip, review.xpath('.//span[contains(@id,"lblCommentText")]/text()').extract()))

				item['comment'] = [topic,pos,comment]
				item['rating'] = review.xpath('.//span[contains(@id,"lblGuestRating")]/text()').extract()[0]
				item['source'] = "agoda"
				# print item,"\n";
				yield item
