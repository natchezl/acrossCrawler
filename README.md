
# ACROSS_Crawler
Web Crawler for ACROSS project

## Details
This project contains 3 scrapy projects.

- agoda
- booking
- tripadvisor

Each project contains

	 - hotelItems.py
		 - <projectname>_HotelRatingInfo.py
				 - for crawling Hotel rating
		 - <projectname>_Review.py
				 - for crawling Horel reviews
	 - hotelscoreItem.py
	 - pipelinesMongodb.py
	 - reviewItem.py
	 - setting.py
	   - set database information here.



----------
##Crawler Usage
To crawl hotel rating
> `scrapy crawl <projectname>_HotelRatingInfo.py -o <output_file>.json`

To crawl hotel reviews
> `scrapy crawl <projectname>_Review.py -o <output_file>.json`

The output will be saved into database automatically


You may run the program in background process by using the following command.
> `screen -L scrapy crawl <filename> -o <output_file>.json`

----------

##Data Processing folder
This folder contains
>- Calculate_Avg_Score.py
- Combine_Reviews.py
- getSummaryFromDB.py
- joinInfoAvg.py
- keywords.json

###Usage
After finished crawling data, run these files in order.

1. Calculate_Avg_Score.py
2. joinInfoAvg.py
3. Combine_Reviews.py
4. getSummaryFromDB.py
