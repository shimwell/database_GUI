
import json
import os
import sys

import numpy as np

from data_formatting_tools import *
from database_tools import *
from nuc_data_lib import *


def make_json_obj_from_nuclear_data_file(root,file):
    if 'exfor' in root:
        data = make_json_obj_from_exfor_file(root,file)
    else:
        data = make_json_obj_from_evaluation_file(root,file)
    return data



def make_json_obj_from_evaluation_file(root,file):
    print('getting data from ',root, file)
    chop_up = root.split(os.sep)
    mt_number = file
    library = chop_up[-1]
    nucleon_number = chop_up[-2]
    element = chop_up[-3]
    incident_particle = chop_up[-4]
    proton_number = str(find_protons_from_element_symbol(element))
    element_full = element_lookup(element).lower()

    if nucleon_number.endswith('m') or nucleon_number.endswith('n'):
        protons_and_neutrons = nucleon_number[:-1]
    else:
        protons_and_neutrons = nucleon_number

    if nucleon_number == '000':
        neutron_number = 'natural'
        nucleon_number = 'natural'
    else:
        neutron_number = str(int(protons_and_neutrons)-int(proton_number))

    products = mtlookup(incident_particle,mt_number)

    if products.startswith('none found') ==False:

        #textfield =  element_full+ ' '+element+' ' +nucleon_number +' '+incident_particle+','+products+  ' MT'+mt_number +' '+ library
        try:
            energy,xs, =np.genfromtxt(fname=os.path.join(root, file), usecols = (0, 1) ,unpack=True,comments='#')
        except ValueError:
            print('file contains no xs data',os.path.join(root, file) )
            return None

        data = {#'Element':element_full,
                #'Element symbol':element.title(),
                #'Proton number':proton_number,
                'Protons / Element':str(proton_number) +' ' + element +' ' + element_full,
                'Nucleon number':nucleon_number,
                'Neutron number':neutron_number,
                'Incident particle':incident_particle,
                'Products':products,
                'MT number':mt_number,
                'Library':library,
                'filename':str(element.title()+nucleon_number+' '+incident_particle+','+products+' '+ library).replace(' ','_'),
                'Energy':list(energy),
                'Cross section':list(xs),
                #'textfield':textfield
                }
        return data

def make_json_obj_from_exfor_file(root,file):
    print(os.path.join(root, file))
    chop_up = (os.path.join(root, file)).split(os.sep)
    experiment_name=chop_up[-1].split('-')[0]
    experiment_id  =chop_up[-1].split('-')[1]
    experiment_year=chop_up[-1].split('-')[2]
    mt_number=chop_up[-2]
    library = chop_up[-3]
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
      try:
        energy,xs,error_xs,error_energy =np.genfromtxt(fname=os.path.join(root, file), usecols = (0, 1, 2, 3) ,unpack=True,comments='#')
      except ValueError:
        print('file contains no xs data',os.path.join(root, file) )
        return None

      if type(energy).__name__ == 'float64':
        energy = [energy]
        xs = [xs]
        error_xs = [error_xs]
        error_energy = [error_energy]
      else:
        energy = list(energy)
        xs = list(xs)
        error_xs = list(error_xs)
        error_energy = list(error_energy)

      data = {#'Element':element_full,
              #'Element symbol':element,
              #'Proton number':proton_number,
              'Protons / Element':str(proton_number) +' ' + element +' ' + element_full,
              'Nucleon number':nucleon_number,
              'Neutron number':neutron_number,
              'Incident particle':incident_particle,
              'Products':products,
              'MT number':mt_number,
              'Library':library,
              'Experiment name':experiment_name,
              'Experiment id':experiment_id,
              'Experiment year':experiment_year,
              'filename':str(element.title()+nucleon_number+' '+incident_particle+','+products+' '+ library).replace(' ','_'),
              'Energy': energy,
              'Cross section': xs,
              'Cross section error': error_xs,
              'Energy error': error_energy,
              #'textfield':textfield
             }
      return data

def make_json_objs_from_files(list_of_files):

    list_of_data=[]

    for dir_and_file in list_of_files:
        root,file =os.path.split(dir_and_file)
        db_entry = make_json_obj_from_nuclear_data_file(root,file)
        if db_entry != None:
          list_of_data.append(db_entry)

    return list_of_data

def save_list_of_all_files(list_of_data,filename):
    print('saving data')
    with open(filename, 'w') as fout:
        #json.dump(list_of_data, fout, encoding='utf-8', indent = 4) #python 2
        json.dump(list_of_data, fout, indent = 4)




list_of_csv_filenames = find_files_recursive(folder="xs", extension="", ignore='.json')

print(list_of_csv_filenames)

list_of_json_objects = make_json_objs_from_files(list_of_csv_filenames)

os.system('mongod --bind_ip_all &')
for i in list_of_json_objects:
    save_list_of_all_files(i,i['filename']+'.json')
    os.system('mongoimport --collection collection_one --db my_database --file '+i['filename']+'.json')
print(list_of_json_objects[0])
os.system('rm *.json')


collection, client, db = connect_to_docker_database()
# delete_database(client)

# upload_json_objects_to_database(list_of_json_objects, collection)

all_database_fields = get_database_fields(collection)

print('all_database_fields',all_database_fields)
