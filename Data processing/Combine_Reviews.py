'''
Created on Mar 6, 2558 BE

@author: natchez
'''

from pymongo import MongoClient
from bson.code import Code

client = MongoClient('mongodb://128.199.109.231:9999')
db = client.Scrapy_Reviews
collection = db.review

pipeline = [
    { "$match" : {"source": {"$in" :["agoda", "tripadvisor"]}}},
    { "$group" : { 
            "_id" : "$title", 
            "count" : {"$sum":1} , 
            "comment" : {"$addToSet": '$comment'} ,
        }
    },
    {"$unwind" : "$comment"}, 
    {"$unwind" : "$comment"}, 
    {"$group" : {
            "_id" : "$_id",
            "count" : {"$first" : "$count"},
            "comment" : {"$addToSet" : "$comment"}
        }
    },
    { "$match": { "count" : { "$gt" : 100 }}},
    { "$sort" : {"count":-1 , "_id": 1} },
    { "$out" : "review_all_nobooking"}
]
itemCursor = db.review.aggregate(pipeline, allowDiskUse=True)
print 'finish'
# for data in a:
#         print data
# for data in a.get("result"):
#     print data  
