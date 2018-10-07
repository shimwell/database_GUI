
import collections
import pymongo
from pymongo import MongoClient
from database_tools import *


collection, client, db = connect_to_database()

query = {'uploader':'shimwell','filename':'a/Small Punch Creep 105.txt'}

myresults=collection.find(query)

print('number of results found = ' ,myresults.count())

print('current uploader ',myresults[0]['uploader']) 

new_values = { "$set":{'uploader':'Mark','filename':'a/Small Punch Creep 105.txt'}}

collection.update_one(query, new_values)