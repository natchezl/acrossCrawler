import scrapy


class ReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    nationality = scrapy.Field()
    travelType = scrapy.Field()
    reviewDate = scrapy.Field()
    comment = scrapy.Field()
    rating = scrapy.Field()
    source = scrapy.Field()
