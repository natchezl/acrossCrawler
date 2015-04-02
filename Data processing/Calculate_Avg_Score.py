'''
Created on Mar 2, 2558 BE

@author: natchez
'''

import pymongo
from pymongo import MongoClient
from bson.code import Code

client = MongoClient('mongodb://128.199.109.231:9999')
db = client.HotelReviews
collection = db.rating

# a = db.rating.aggregate([
# #     { $project : {"total_score" : 1 , "keyname" : 1, "title" : 1, "source" : 1, "count" : 1 , "total_score": 1}},
#     { "$group" : { 
#             "_id" : "$keyname", 
#             "title" : {"$push": "$title"} ,
#             "source" : {"$push": "$source"} , 
#             "count" : {"$sum":1} , 
#             "avg" : { "$avg": ("$total_score")}
#         }},
#     { "$sort" : { "_id": 1} }
# ])
# # for data in a:
# #         print data
# for data in a.get("result"):
#     print data  

# ===================================================================================

mapper = """function() {
                var weight = 1
                if (this.source == "tripadvisor")
                    weight = 2
                    
                values = {
                    total_score : weight * parseFloat(this.total_score), 
                    comfort : weight * parseFloat(this.comfort), 
                    value : weight * parseFloat(this.value), 
                    location : weight * parseFloat(this.location), 
                    cleanliness : weight * parseFloat(this.cleanliness),
                    staff :  weight * parseFloat(this.staff)
                }
                emit(this.keyname , values)
            }
        """
reducer = """
            function (key, values){
                var avgRating = {
                    total_score :0 ,
                    comfort :0 ,
                    value : 0 ,
                    location : 0 , 
                    cleanliness : 0 ,
                    staff :0
                }
                
                for (var i=0; i<values.length; i++){
                    avgRating.total_score += values[i].total_score
                    avgRating.comfort += values[i].comfort
                    avgRating.value += values[i].value
                    avgRating.location += values[i].location
                    avgRating.cleanliness += values[i].cleanliness
                    avgRating.staff += values[i].staff  
                }
                
                avgRating.total_score /= values.length
                avgRating.comfort /= values.length
                avgRating.value /= values.length
                avgRating.location /= values.length
                avgRating.cleanliness /= values.length
                avgRating.staff /= values.length
                
                return avgRating
            }
        """
result = db.rating.map_reduce(mapper, reducer, "avg_total_score")
# for doc in result.find():
#         print doc
print "finished"
        