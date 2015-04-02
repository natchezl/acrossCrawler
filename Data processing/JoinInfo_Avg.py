'''
Created on Mar 11, 2558 BE

@author: natchez
'''
import pymongo
from pymongo import MongoClient
from bson.code import Code

client = MongoClient('mongodb://128.199.109.231:9999')
db = client.Scrapy_Reviews
INFOCOLLECTION = db.info
AVGCOLLECTION = db.avg_total_score
SUMMARYCOLLECTION= db.summary

print "start"
hotelinfos = list(INFOCOLLECTION.find().sort("title",1))
print len(hotelinfos)
# summaries = list(SUMMARYCOLLECTION.find({},{"_id":"1"}))
# print len(summaries)

for hotel in hotelinfos:
    print hotel.get("name"),hotel.get("title"),hotel.get("city"),hotel.get("country")
    summary = SUMMARYCOLLECTION.find_one({"_id": hotel.get("title")},{"_id":"1"})
#     print summary
    if summary== None:
        valid=0
    else:
        valid=1
    AVGCOLLECTION.update(
        {"_id": hotel.get("title")},
        {"$set":
            {"name": hotel.get("name"),
             "city": hotel.get("city"),
             "country": hotel.get("country"),
             "address": hotel.get("address"),
             "valid": valid}
        }
    )

# for summary in summaries:
#     print summary.get("_id")
#     AVGCOLLECTION.update(
#         {"_id": summary.get("_id")},  
#         {"$set":
#             {"valid" : 9}
#         }      
#     )
print "success"
#     print hotel.get("title")
#     print hotel.get("city")
#     print hotel.get("country")
#     AVGCOLLECTION.update(
#                          )