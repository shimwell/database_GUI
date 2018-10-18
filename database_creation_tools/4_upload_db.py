import pymongo 
import json
import os
import sys
import numpy as np
import math

#from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage,ProgressBar, ReverseBar, RotatingMarker, SimpleProgress, Timer
from tqdm import tqdm
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string

import natsort
from nuc_data_lib import *

def load_list_of_all_files(filename):
    print('loading data')
    list_of_data = json.load(open(filename))
    return list_of_data

def organise_queing_system_for_database(list_of_data):

    print(list_of_data[0])
    q = Queue(maxsize = len(list_of_data))
  
    key_list_split = split_list_to_parts(list_of_data)
    
    cpu_count = mp.cpu_count()
    
    with ThreadPoolExecutor(max_workers = cpu_count) as executor:
        for lst in key_list_split :
          executor.submit(build_cloud_database, lst)
          #executor.submit(build_cloud_database, lst,q)

def build_cloud_database(list_of_data):

    database_name = 'xs_database'
    collection_name = 'cross_sections_collection'

    username="cross-section-admin"
    connection='connectionkey'#input()

    connection_string="mongodb+srv://"+username+":"+connection+"@cross-section-plotter-cluster-zqdfc.mongodb.net/test?retryWrites=true"
    client = pymongo.MongoClient(connection_string)


    db = client[database_name]
  
    collection = db[collection_name]
  
    serverStatusResult=db.command("serverStatus")
    pprint(serverStatusResult)
      

    for data in tqdm(list_of_data , total=len(list_of_data)):
       try:
          collection.insert(data)
       except:
          print('trying to add data to cloud')
          print('error ')
          print(data)
    print('done ')

def split_list_to_parts(lst):
  cpu_count = mp.cpu_count()
  part_list = []
  len_part = int(math.ceil(len(lst) / cpu_count))

  #print "cpus", cpu_count
  #print "list len", len(lst)
  #print "partlen", len_part

  if cpu_count >= len(lst) :
    for item in lst :
      part_list.append([item])
  else :
    for i in range(cpu_count - 1):
      print("range", i*len_part, ":", (i+1)*len_part)
      part_list.append(lst[i * len_part: (i + 1) * len_part])
    part_list.append(lst[(cpu_count -1)*len_part : ])

  return part_list

def wipe_database():

    database_name = 'xs_database'
    collection_name = 'cross_sections_collection'

    username="cross-section-admin"
    connection='connectionkey'#input()

    connection_string="mongodb+srv://"+username+":"+connection+"@cross-section-plotter-cluster-zqdfc.mongodb.net/test?retryWrites=true"
    client = pymongo.MongoClient(connection_string)

    client.drop_database(database_name)

#wipe_database()
list_of_data = load_list_of_all_files('list_of_data.txt')
organise_queing_system_for_database(list_of_data)
#build_cloud_database(list_of_data)
