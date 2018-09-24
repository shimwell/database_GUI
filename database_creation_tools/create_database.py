#!/usr/bin/env python

"""
create_database.py: 

This file shows how to use the database_tools and data_formatting tools
A database is made from a combination of:
 text files containgin x,y data
 MS excel files containing meta data
 The filename of the file containing meta data
 A custom meta data tag added to the database during the script
"""

__author__      = "Jonathan Shimwell"

from data_formatting_tools import *
from database_tools import *





list_of_csv_filenames = find_files(data_folders=["dummy_data"], extension=".txt")
                                                     
list_of_json_filenames  = [s[:-4] + '.json' for s in list_of_csv_filenames]

list_of_json_meta_data_filenames = [s[:-4] + '_meta.json' for s in list_of_csv_filenames]

list_of_excel_filenames = [s[:-4] + '.xlsx' for s in list_of_csv_filenames]


list_of_dataframes_objects = convert_csv_files_to_dataframe_objects(filenames=list_of_csv_filenames,
                                                                    schema = ['Time','Height'])                

list_of_json_filenames = convert_dataframe_objects_to_json_files(list_of_dataframes=list_of_dataframes_objects,
                                                                 filenames=list_of_json_filenames )

list_of_json_objects = read_in_json_files(list_of_json_filenames)

list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'Time')

list_of_json_objects = add_meta_data_to_json_objects(json_object=list_of_json_objects,
                                                     keyname=['filename']*len(list_of_json_objects),
                                                     keyvalue=list_of_csv_filenames)

for i in list_of_json_objects :
    print(i)

for i, filename in enumerate(list_of_excel_filenames):
    
    excel_file = open_excel_file(filename=filename)

    val=get_value_of_excel_file(excel_file,row=0,column=1, worksheet='Sheet1')
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='city',
                                                        keyvalue=val)


    val=get_value_of_excel_file(excel_file,row=1,column=1, worksheet='Sheet1')
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='country',
                                                        keyvalue=val)



#example for adding meta data to all entries
for json_object in list_of_json_objects:
    json_object = add_meta_data_to_json_objects(json_object=json_object,
                                                            keyname='uploader',
                                                            keyvalue='shimwell')


# example for getting meta data from a file
for i, filename in enumerate(list_of_csv_filenames):
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='file number',
                                                        keyvalue=filename.split('/')[-1].split('_')[-1])


#optional to write the json files containing meta data
list_of_json_filenames_with_meta = write_json_files(json_objects=list_of_json_objects,filenames=list_of_json_meta_data_filenames)

for i in list_of_json_objects :
    print(i)

collection, client, db = connect_to_database()

delete_database(client)

upload_json_objects_to_database(list_of_json_objects,collection)


all_database_fields = get_database_fields(collection)

meta_data_fields = get_database_fields(collection)
#meta_data_fields = get_database_fields(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3'])


print('meta_data_fields =',meta_data_fields)
print('all_database_fields=', all_database_fields)