
import collections
import pymongo
from pymongo import MongoClient
from database_tools import *


collection, client, db = connect_to_database()

query = {'filename':'a/Small Punch Creep 105.txt'}

myresults=collection.find(query)

print('number of results found = ' ,myresults.count())

current_load = myresults[0]['Load']
current_extens = myresults[0]['Extens']

print('current Load has ',len(current_load),' datapoints') 
print('current Load has ',len(current_extens),' datapoints') 

new_load=[]
new_extens=[]

for l, e in zip(current_load,current_extens):
    if l > 0.3 and l < 0.67:
        new_load.append(l)
        new_extens.append(e)

print('new Load has ',len(new_load),' datapoints') 
print('new Load has ',len(new_extens),' datapoints') 

editted_results = { "$set":{'Load':new_load,'Extens':new_extens}}

collection.update_one(query, editted_results)