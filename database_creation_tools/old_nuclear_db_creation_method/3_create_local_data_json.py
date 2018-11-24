import pymongo 
import json
import os
import sys

import numpy as np
#from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, FileTransferSpeed, FormatLabel, Percentage,ProgressBar, ReverseBar, RotatingMarker, SimpleProgress, Timer
from tqdm import tqdm
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string

import natsort
from nuc_data_lib import *


def split_list_to_parts(lst):
    cpu_count = mp.cpu_count()
    part_list = []
    len_part = len(lst) / cpu_count

    #print "cpus", cpu_count
    #print "list len", len(lst)
    #print "partlen", len_part

    if cpu_count >= len(lst) :
        for item in lst :
            part_list.append([item])
    else:
        for i in range(cpu_count - 1) :
            #print "range", i*len_part, ":", (i+1)*len_part
            part_list.append(lst[i*len_part : (i+1) * len_part] )
        part_list.append(lst[(cpu_count -1)*len_part : ])

    return part_list


def make_json_obj_from_evaluation_file(root,file):
    print(os.path.join(root, file))
    chop_up = root.split(os.sep)
    mt_number=file 
    library = chop_up[-1]
    # if library.lower() == 'tendl.2015':
    #   library='talys.2015'
    nucleon_number = chop_up[-2]
    element = chop_up[-3]
    incident_particle = chop_up[-4]
    proton_number= str(find_protons_from_element_symbol(element))
    element_full = element_lookup(element).lower()

    if nucleon_number.endswith('m') or nucleon_number.endswith('n'):
        protons_and_neutrons = nucleon_number[:-1]
    else:
        protons_and_neutrons=nucleon_number

    if nucleon_number=='000':
        neutron_number='natural'
        nucleon_number='natural'
    else:
        neutron_number = str(int(protons_and_neutrons)-int(proton_number))
        if int(neutron_number)<0:
            print('neutron number can not be negative ',neutron_number)
            print('protons_and_neutrons',protons_and_neutrons)
            print('proton_number',proton_number)
            #print(root,dirs,file)
            sys.exit()

    products = mtlookup(incident_particle,mt_number)

    if products.startswith('none found') ==False:

        #textfield =  element_full+ ' '+element+' ' +nucleon_number +' '+incident_particle+','+products+  ' MT'+mt_number +' '+ library 
        energy,xs, =np.genfromtxt(fname=os.path.join(root, file), usecols = (0, 1) ,unpack=True,comments='#')
        data = {'Element':element_full,
                'Element symbol':element.title(),
                'Nucleon number':nucleon_number,
                'Proton number':proton_number,
                'Neutron number':neutron_number,
                'Incident particle':incident_particle,
                'Products':products,
                'MT number':mt_number,
                'Library':library,
                'filename':element.title()+nucleon_number+' ('+incident_particle+','+products+') '+ library,
                'energy':list(energy),#np.array2string(energy).replace('\n', ''),
                'xs':list(xs),#np.array2string(xs).replace('\n', ''),
                #'textfield':textfield
                }
        return data

def make_json_obj_from_exfor_file(root,file):
    print(os.path.join(root, file))
    chop_up = (os.path.join(root, file)).split(os.sep)
    if chop_up[-1] =='all':
      experiment_name=chop_up[-1]
    else:
      experiment_name=chop_up[-1].split('-')[0]
      experiment_id  =chop_up[-1].split('-')[1]
      experiment_year=chop_up[-1].split('-')[2]
    mt_number=chop_up[-2]
    library = chop_up[-3]
    # if library.lower() == 'tendl.2015':
    #   library='talys.2015'            
    nucleon_number = chop_up[-4]

    if nucleon_number.endswith('m') or nucleon_number.endswith('n'):
      protons_and_neutrons = nucleon_number[:-1]
    else:
     protons_and_neutrons=nucleon_number


    element = chop_up[-5]
    proton_number= str(find_protons_from_element_symbol(element))
    incident_particle = chop_up[-6]
    products = mtlookup(incident_particle,mt_number)

    if products.startswith('none found')==False:
      
      #print('nucleon_number',nucleon_number)
      #print('proton_number',proton_number)
      

      if nucleon_number == '000':
        neutron_number='natural'
        nucleon_number='natural'
      else:
        neutron_number = str(int(protons_and_neutrons)-int(proton_number))
        if int(neutron_number)<0:
          print('neutron number can not be negative ',neutron_number)
          print('chop_up',chop_up)
          print('protons_and_neutrons',protons_and_neutrons)
          print('proton_number',proton_number)                
          print(root,dirs,file)
          sys.exit()

      element_full = element_lookup(element).lower()
      energy,xs,error_xs,error_energy =np.genfromtxt(fname=os.path.join(root, file), usecols = (0, 1, 2,3) ,unpack=True,comments='#')
      #print(np.array2string(energy))
      # if experiment_name =='all':
      #     #textfield =  element_full+ ' '+element+' ' +nucleon_number +' '+incident_particle+','+products+  ' MT'+mt_number +' '+ library + ' '+experiment_name
      #     data = {'element_full':element_full,
      #           'element':element,
      #           'nucleon_number':nucleon_number,
      #           'products':products,
      #           'mt_number':mt_number,
      #           'proton_number':proton_number,
      #           'neutron_number':neutron_number,
      #           'incident_particle':incident_particle,
      #           'library':library,
      #           'experiment_name':experiment_name,
      #           'experiment_id':experiment_id,
      #           'experiment_year':experiment_year,                      
      #           #'xs':np.array2string(xs).replace('\n', ''),
      #           #'error_xs':np.array2string(error_xs).replace('\n', ''),
      #           #'error_energy':np.array2string(error_energy).replace('\n', ''),
      #           #'energy':np.array2string(energy).replace('\n', ''),                    
      #           #'textfield':textfield}             
      # else:
          #textfield =  element_full+ ' '+element+' ' +nucleon_number +' '+incident_particle+','+products+  ' MT'+mt_number +' '+ library + ' '+experiment_name+'-'+experiment_id+'-'+experiment_year
      data = {'element_full':element_full,
          'element':element,
          'nucleon_number':nucleon_number,
          'products':products,
          'mt_number':mt_number,
          'proton_number':proton_number,
          'neutron_number':neutron_number,
          'incident_particle':incident_particle,
          'library':library,
          'experiment_name':experiment_name,
          'experiment_id':experiment_id,
          'experiment_year':experiment_year,
          'xs':np.array2string(xs).replace('\n', ''),
          'error_xs':np.array2string(error_xs).replace('\n', ''),
          'error_energy':np.array2string(error_energy).replace('\n', ''),
          'energy':np.array2string(energy).replace('\n', ''),                   
          #'textfield':textfield
          }    
      return data

def find_all_files(folder_to_look_at):
    outputfile = open('missingMT.txt','w')
    missing_MT_list=[]
    data = {}
    list_of_data=[]
    list_of_unique_keys=[]

    error_files=''
    for root, dirs, files in os.walk(folder_to_look_at):
    #for root, dirs, files in os.walk("/media/jshim/Data/website5_angles/xs/n/ag/000/exfor/"):
    #for root, dirs, files in os.walk("/media/jshim/Data/website5_angles/xs/n/ag/"):
        for file in files:
           #print root
            if 'exfor' not in root:
                if 'jeff3.3' in root:

                    data = make_json_obj_from_evaluation_file(root,file)
                    list_of_data.append(data)
              # else:
              #   if file not in missing_MT_list:
              #     outputfile.write(file+'\n')
              #     missing_MT_list.append(file)
                
                    
           # if 'exfor' in root:   
  
           #      data = make_json_obj_from_exfor_file(root,file) 
           #      list_of_data.append(data) 
           #    else:
           #      if mt_number not in missing_MT_list:
           #        outputfile.write(mt_number+'\n')
           #        missing_MT_list.append(mt_number)
                  
    outputfile.close()
    return list_of_data


def full_text_search(cloud_or_local,search_this_string= "9 be n,2n"):

  if cloud_or_local =='cloud':
    connection_string="mongodb://jshim:connectionpassword@cluster0-shard-00-00-wmnjb.mongodb.net:27017,cluster0-shard-00-01-wmnjb.mongodb.net:27017,cluster0-shard-00-02-wmnjb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
  
    client = pymongo.MongoClient(connection_string)
  else:
    client = pymongo.MongoClient()
    
  #use test; 
  
  database_name = 'xs_database_full'
  #database_name = 'xs_database'
  collection_name = 'cross_sections_collection_full'
  #collection_name = 'cross_sections_collection'
  
  db = client[database_name]
  collection = db[collection_name]

  limit=10
  print('\n')
  print('\n'+search_this_string)
  number_of_matching_results= collection.find({"$text": {"$search": search_this_string}}).count()
  #print '\nnumber of matching results' ,number_of_matching_results,'\n'
  print('showing closest maching ', limit, ' of ',number_of_matching_results)


  result = collection.find({"$text": {"$search": search_this_string}}, {'score': {'$meta': 'textScore'}})
  result.sort([('score', {'$meta': 'textScore'})])
  result.limit(limit)
  #print(type(result))# mongo cursor
  search_results=''
  for item in result:
    #print(type(item)) #dictionary
    for field in item:
        if field =='textfield':
          #print str(field),
          print(str(item[field]))
          search_results=search_results+ str(item[field])+'\n'

    #pprint.pprint(item)
    #print('  ',item)
    #return jsonify(result=search_results)





  #procced_que_items = []
  #while not q.empty() :
  #  item = q.get()
  #  procced_que_items.append(item)




def save_list_of_all_files(list_of_data,filename):
    print('saving data')
    with open(filename, 'w') as fout:
        json.dump(list_of_data, fout, encoding='utf-8', indent = 4)



def find_entries_for_each_dictionary_key(list_of_data,output_filename):
  
    element_list=[]
    nucleon_number_list=[]
    products_list=[]
    proton_number_list=[]
    neutron_number_list=[]
    incident_particle_list=[]
    library_list=[]
    experiment_name_list=[]
    experiment_id_list=[]
    experiment_year_list=[]

    unique_data_list={'element':[],'element_full':[],'nucleon_number':[],'mt_number':[],'products':[],'proton_number':[],'neutron_number':[],'incident_particle':[],'library':[],'experiment_name':[],'experiment_year':[]}

    for entry in list_of_data:
        for item_to_look_for in ['element','element_full','nucleon_number','mt_number','products','proton_number','neutron_number','incident_particle','library','experiment_name','experiment_year']:
            if item_to_look_for in entry.keys():
                if entry[item_to_look_for] not in unique_data_list[item_to_look_for]:
                    unique_data_list[item_to_look_for].append(entry[item_to_look_for])
    print(unique_data_list)
    with open(output_filename, 'w') as fout:
        json.dump(unique_data_list, fout)
    return output_filename


def sort_unique_data(input_filename,output_filename):

  print('loading data')
  list_of_unique_data = json.load(open(input_filename))
  for key in list_of_unique_data.keys():
    print(key)

  sorted_unique_data_list={'proton_element_element_full':[],'nucleon_number':[],'mt_number':[],'products':[],'neutron_number':[],'incident_particle':[],'library':[],'experiment_name':[],'experiment_year':[]}

  for item_to_look_for in ['nucleon_number','mt_number','products','neutron_number','incident_particle','library','experiment_name','experiment_year']:
    sorted_unique_data_list[item_to_look_for]=natsort.natsorted(list_of_unique_data[item_to_look_for])
   
    print(list_of_unique_data[item_to_look_for])
    print(sorted_unique_data_list[item_to_look_for])
    


  combined_proton_element_list_without_value=[]
  for p,e,ef in zip(list_of_unique_data['proton_number'], list_of_unique_data['element'], list_of_unique_data['element_full']):
       label = p+' '+e.title()+' ' +ef
       combined_proton_element_list_without_value.append(label) 
  combined_proton_element_list_without_value=natsort.natsorted(combined_proton_element_list_without_value)
  sorted_unique_data_list['proton_element_element_full'] = combined_proton_element_list_without_value
# combined_proton_element_list=[]
# for item in combined_proton_element_list_without_value:
#      combined_proton_element_list.append({'label':item,'value':item.split()[0]})


  with open(output_filename, 'w') as fout:
      json.dump(sorted_unique_data_list, fout)



cloud_or_local ='cloud'
list_of_data=find_all_files("/media/jshim/Data/mongodb/cross-section-plotter/xs")
save_list_of_all_files(list_of_data,'list_of_data.txt')


#find_entries_for_each_dictionary_key(list_of_data=list_of_data,output_filename='unique_data_list.txt')
#sort_unique_data(input_filename='unique_data_list.txt',output_filename='sorted_unique_data_list.txt')

print('done')


