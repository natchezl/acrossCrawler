import subprocess
import json
import os
# import sys

script_dir = os.path.dirname(__file__)
json_data=open(script_dir+'reviewScore2.json')

data = json.load(json_data)
json_data.close()

output_dir = script_dir+'review'
# hotel_url = "http://www.booking.com/hotel/jp/sakura-ikebukuro.en-gb.html"

writer =open('downloadedLink.html','w')

for line in data:
	if(line['title']):
		title = line['title'][0]
		review_num = line['review_num'][0]

		print title, review_num
		offset_num =0

		while (offset_num < int(review_num)):
			url= "http://www.booking.com/reviewlist.en-gb.html?dcid=4;cc1=jp;dist=1;pagename=%s;type=total&;offset=%s;rows=99" %(title,offset_num)

			print "downloading %s" %url
			writer.write(url)
			writer.write("\n")
			# subprocess.call(["wget",url])
			subprocess.call(["wget",
				"--header='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'", 
				"--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'", 
				"--header='Accept-Encoding: gzip, deflate, sdch'",
				"--header='Accept-Language: th,en-US;q=0.8,en;q=0.6'",
				"--header='Cache-Control: max-age=0'", 
				"--load-cookies=cookies.txt", 
				"-d",
				"-O", output_dir+"/%s-%s-%s.html" %('jp',title,(offset_num/99)), url])
			# print url
			offset_num += 99
print "finished" 

