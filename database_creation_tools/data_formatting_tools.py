import pandas as pd
import os
import json
import pprint
import collections
import pymongo
from pymongo import MongoClient
#from bson.code import Code
import xlrd


def find_files_recursive(folder,extension,ignore):

    list_of_files=[]

    for root, dirs, files in os.walk(folder):
        for file in files:
          if file.endswith(extension) and not file.endswith(ignore):
              list_of_files.append(os.path.join(root,file))
                  
    return list_of_files

def find_files(data_folders,extension):
    ''' function searches through folders and finds files ending with .txt or .csv
        input: folder(s) to search through
        input type: list of strings
        returns: list of matching filenames
    '''
    list_of_filenames =[]
    for folder in data_folders:
        print(folder)
        for file in os.listdir(folder):
            if file.endswith(extension):
                filename = os.path.join(folder ,file)
                list_of_filenames.append(filename)
    return list_of_filenames


def convert_csv_files_to_dataframe_objects(filenames ,schema):
    ''' Loads csv files into a pandas dataframe
        checks that files match the schema
        inputs: list of filenames, schema [optional]
        input types: list of strings, list of strings
    '''
    list_of_dataframes =[]
    for filename in filenames:
        df = pd.read_csv(filename ,sep=',|\t')
        for header in df.columns.values:
            df.rename(columns={header: header.strip('\t .')}, inplace=True)
        # print(df.columns.values)
        if set(df.columns.values) == set(schema):
            print('converting' ,filename, 'to dataframe')
            list_of_dataframes.append(df)
        else:
            print("\x1b[31m\"" + str(filename) + ' does not conform to schema' + "\x1b[0m")
    return list_of_dataframes


def convert_dataframe_objects_to_json_files(list_of_dataframes, filenames):
    ''' Converts pandas dataframe into a json file
        inputs: list of dataframes
        input types: list of dataframes
    '''
    list_of_filenames = []
    for df, filename in zip(list_of_dataframes, filenames):
        df.to_json(filename, orient='columns')
        # df.to_json(filename, orient='columns', index=False) index setting is not currently supported, perhaps with the next release, see http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html?highlight=to_json#pandas.DataFrame.to_json
        list_of_filenames.append(filename)
    return list_of_filenames

def apply_abs_operation_to_field(json_objects,field):
    for json_object in json_objects:
        json_object[field]=l = [abs(x) for x in json_object[field]]
    return json_objects

def read_in_json_file(filename):
    # read in json file
    with open(filename) as f:
        data = json.load(f)
    return data

def read_in_json_files(filenames):
    # read in json files
    list_of_json_objects = []
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)
            data = remove_df_index_from_json_object(data)
            list_of_json_objects.append(data)
    return list_of_json_objects

def convert_list_of_tuples_to_list(list_of_tuples):
    list_of_single_values=[]
    for x in range(0,len(list_of_tuples)):
        list_of_single_values.append(list_of_tuples[str(x)])
    return list_of_single_values

def remove_df_index_from_json_object(data):
    newdata={}
    for key in data.keys():
        #print(key)
        list_of_tuples = data[key]
        newdata[key] = convert_list_of_tuples_to_list(list_of_tuples) 
    return newdata
       
def write_json_files(json_objects, filenames):
    print('writing json files')
    list_of_json_objects = []
    for filename, json_object in zip(filenames, json_objects):
        with open(filename, 'w') as outfile:
            json.dump(json_object, outfile,  indent=4)
    return filenames


def add_meta_data_to_json_objects(json_object, keyname, keyvalue):
    # add some meta data to json file

    if type(json_object) == list and type(keyname) == list and type(keyvalue) == list:
        for item_json, item_keyname, item_keyvalue in zip(json_object, keyname, keyvalue):
            item_json[item_keyname] = item_keyvalue
            print('added new meta data list', item_keyname, ' = ', item_keyvalue)
        return json_object
    else:
        json_object[keyname] = keyvalue
        print('added new meta data', keyname, ' = ', keyvalue)
        return json_object


def open_excel_file(filename):
    workbook = xlrd.open_workbook(filename)
    return workbook

def get_value_of_excel_file(workbook, row, column, worksheet='Data'):

    worksheet = workbook.sheet_by_name(worksheet)

    value = worksheet.cell(row, column).value

    if value == '':
        raise ValueError('value in row ' ,row, ' column ', column, ' is empty. Check the sheet or try 16,3 for Operator and Material 29,3')

    else:

        return str(value)
