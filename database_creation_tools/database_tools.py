import pandas as pd
import os
import json
import pprint
import collections
import pymongo
from pymongo import MongoClient
from bson.code import Code
from natsort import natsorted
from tqdm import tqdm

def connect_to_database(db_name='materials_database',collection_name='small_punch'):
    ''' Creates a local MongoDB database called material_database and connects to it
        defaults are provided for the names
    '''
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[collection_name]
    print('connected to database')
    return collection, client, db

def delete_database(client, db_name='materials_database'):
#     collection, client = connect_to_database()
    client.drop_database(db_name)
    print('database deleted')

def upload_json_objects_to_database(data,collection):


#     collection, client = connect_to_database()
    if type(data)==list:
        for item in tqdm(data , total=len(data)):

            try:
                collection.insert_one(item)
            except:
                print('inserting entry into database failed',item['filename'])

    else:
        collection.insert_one(data)
    print('json object commited to database')

#def get_database_fields(collection, query_fields_and_values={},ignore_fields=[]):
def get_database_fields(collection,ignore_fields=[]):
    mapper = Code("""
                  function() {
                              for (var key in this) { emit(key, null); }
                             }
                  """)

    reducer = Code("""
                   function(key, stuff) { return null; }
                   """)

    mr = collection.map_reduce(map = mapper,
                               reduce = reducer,
                               #query = query_fields_and_values,
                               out = "my_collection" + "_keys")
    unique_fields = []
    for doc in mr.find():
        if doc["_id"] not in ignore_fields:
            if doc["_id"] != "_id":
                unique_fields.append(doc["_id"])
    return unique_fields

def get_entries_in_field(collection, field, query=None):
    if query != {}:
        result = collection.distinct(field, query)
    else:
        result = collection.distinct(field)
    #print(result)
    return natsorted(result)

def get_type_of_entries_in_field(collection, field, query=None):
    field_type = type(collection.find_one({field: {'$exists': True} })[field]).__name__
    print(field, field_type)
    return field_type
    #return type(collection.find_one()[field]).__name__

def find_all_fields_types_in_database(collection):
    all_fields = get_database_fields(collection)
    field_and_type = {}
    for field in all_fields:
        type_of_field_contents = get_type_of_entries_in_field(collection,field)
        field_and_type[field] = type_of_field_contents
    return field_and_type

def find_all_fields_of_a_particular_types_in_database(collection,type_required):
    all_fields = get_database_fields(collection)
    field_of_correct_type = []
    for field in all_fields:
        type_of_field_contents = get_type_of_entries_in_field(collection, field)
        if type_of_field_contents == type_required:
            field_of_correct_type.append(field)
    return field_of_correct_type

def find_all_fields_not_of_a_particular_types_in_database(collection,type_not_desired):
    all_fields = get_database_fields(collection)
    field_of_correct_type = []
    for field in all_fields:
        type_of_field_contents = get_type_of_entries_in_field(collection, field)
        if type_of_field_contents != type_not_desired:
            field_of_correct_type.append(field)
    return field_of_correct_type

def get_number_of_matching_entrys(collection, query_fields_and_values):
    result = collection.find(query_fields_and_values)
    return result.count()

def get_matching_entrys(collection, query_fields_and_values,limit=10):
    result = collection.find(query_fields_and_values).limit(limit)
    return result

def find_metadata_fields_and_their_distinct_values(collection, ignore_fields=[]):
    meta_data_fields = get_database_fields(collection, ignore_fields)
    metadata_fields_and_their_distinct_values= {}
    for entry in meta_data_fields:
        values = get_entries_in_field(collection, entry)
        # metadata_values.append(values)
        metadata_fields_and_their_distinct_values[entry] = values

    meta_data_fields_and_distinct_entries = []
    for field in meta_data_fields:
        meta_data_fields_and_distinct_entries.append({'field': [field],
                                                      'distinct_values': metadata_fields_and_their_distinct_values[field]})
    return meta_data_fields_and_distinct_entries


def find_metadata_fields_and_their_distinct_values_and_types(collection, ignore_fields=[]):
    meta_data_fields = get_database_fields(collection, ignore_fields)
    metadata_fields_and_their_distinct_values = {}
    for entry in meta_data_fields:
        values = get_entries_in_field(collection, entry)
        # metadata_values.append(values)
        metadata_fields_and_their_distinct_values[entry] = values



    meta_data_fields_and_distinct_entries = []
    for field in meta_data_fields:
        meta_data_fields_and_distinct_entries.append({'field':[field],
                                                      'distinct_values':metadata_fields_and_their_distinct_values[field],
                                                      'type':type(metadata_fields_and_their_distinct_values[field])})
    return meta_data_fields_and_distinct_entries


if __name__ == '__main__':


  collection, client, db = connect_to_database()

  query = {'uploader':'shimwell','filename':'granta_upload_files/Small Punch Creep 113.txt'}
  query = {'Neutron number':'4'}

  myresults=collection.find_one(query)
  print(myresults)
  for doc in myresults:
    print(doc)
  #print('number of results found = ' ,myresults.count())

  #print('current uploader ',myresults[0]['uploader']) 

  #new_values = { "$set":{'uploader':'Mark','filename':'granta_upload_files/Small Punch Creep 113.txt'}}

  #collection.update_one(query, editted_results)





  #collection.delete_one(myquery)


  #results  = get_number_of_matching_entrys(collection, {'uploader':'shimwell'})
  # results = find_metadata_fields_and_their_distinct_values_and_types(collection)
  # for result in results:
  #   print(result['type'])
  # fields = get_database_fields(collection)
  # for f in fields:
  #   results = get_entries_in_field(collection,f)
  #   type_of_results = get_type_of_entries_in_field(collection,f)
  #   print(f, type_of_results)
  #print(find_all_fields_types_in_database(collection))
  # results = collection.find_one({'temperature':{ '$exists': True }})['temperature']
  # print(results)

  #print(find_all_fields_of_a_particular_types_in_database(collection,'list'))