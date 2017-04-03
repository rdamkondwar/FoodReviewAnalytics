import json
import os
import sys
import codecs
from pprint import pprint

listFiles = os.listdir("zomato/")

id = 1

print("id,Name,address,city,zip code,latitude,longitude,review_count,stars,zomato_id,yelp_id")

'''for each_file in listFiles:
    with codecs.open("zomato/" +  each_file,'r', encoding='utf-8') as data_file:    
        data = json.load(data_file)
        for each_obj, value in data.iteritems():
            for each_res in data[each_obj]:
                id = id + 1
                print(str("a") + str(id) + "," + each_res["restaurant"]["name"].encode('ascii', 'ignore').replace(",","$*$") + "," + 
                    each_res["restaurant"]["location"]["address"].encode('ascii', 'ignore').replace(",","$*$") + "," + 
                    each_res["restaurant"]["location"]["city"].encode('ascii', 'ignore').replace(",","$*$") + "," +
                    each_res["restaurant"]["location"]["zipcode"].replace(",","$*$") + "," + 
                    each_res["restaurant"]["location"]["latitude"].replace(",","$*$") + "," +
                    each_res["restaurant"]["location"]["longitude"].replace(",","$*$") + "," + 
                    each_res["restaurant"]["user_rating"]["votes"] + "," + 
                    each_res["restaurant"]["user_rating"]["aggregate_rating"] + "," + 
                    str(each_res["restaurant"]["R"]["res_id"]) + "," +
                    str(0))'''

with codecs.open("yelp_dataset.json", 'r', encoding='utf-8') as data_file:    
    for line in data_file:
        data = json.loads(line)
        id = id + 1
        print(str("b") + str(id) + "," + data["name"].encode('ascii', 'ignore').replace(",","$*$") + "," + 
            data["address"].encode('ascii', 'ignore').replace(",","$*$") + "," +
            data["city"].encode('ascii', 'ignore').replace(",","$*$") + "," +
            str(data["postal_code"]).replace(",","$*$") + "," +
            str(data["latitude"]).replace(",","$*$") + "," +
            str(data["longitude"]).replace(",","$*$") + "," +
            str(data["review_count"]) + "," +
            str(data["stars"]) + "," +
            "0" + "," +
            data["business_id"].encode('ascii', 'ignore'))