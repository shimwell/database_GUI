




from data_formatting_tools import *
from database_tools import *


list_of_csv_filenames = find_files(data_folders=["a"],extension='.txt')
                                                     # "Small-Punch/p1200",
                                                     # "Small-Punch/p220",
                                                     # "Small-Punch/p4000"
                                                     # ])

list_of_json_filenames  = [s[:-4] + '.json' for s in list_of_csv_filenames]
list_of_excel_filenames = [s[:-4] + '.xlsm' for s in list_of_csv_filenames]

list_of_dataframes_objects = convert_csv_files_to_dataframe_objects(filenames=list_of_csv_filenames,
                                                                    schema = ['Time [sec]', 'Stroke', 'Extens', 'Load', 'TC1', 'TC2', 'TC3'])
                                                                    #schema = ['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3'])

list_of_json_filenames = convert_dataframe_objects_to_json_files(list_of_dataframes=list_of_dataframes_objects,
                                                                 filenames=list_of_json_filenames )


list_of_json_objects = read_in_json_files(list_of_json_filenames)

list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'Load')
list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'Extens')
list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'Stroke')
list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'TC1')
# list_of_json_objects = apply_abs_operation_to_field(json_objects=list_of_json_objects,field= 'Temp1')



list_of_json_objects = add_meta_data_to_json_objects(json_object=list_of_json_objects,
                                                     keyname=['filename']*len(list_of_json_objects),
                                                     keyvalue=list_of_csv_filenames)



for i, filename in enumerate(list_of_excel_filenames):
    excel_file = open_excel_file(filename=filename)

    val=get_value_of_excel_file(excel_file,row=29,column=3)
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='material',
                                                        keyvalue=val)

    # val=get_value_of_excel_file(excel_file,row=16,column=3)
    # list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
    #                                                     keyname='opperator',
    #                                                     keyvalue=val)

    val=get_value_of_excel_file(excel_file,row=15,column=3)
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='diameter',
                                                        keyvalue=val)  

    val=get_value_of_excel_file(excel_file,row=13,column=7)
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='load applied',
                                                        keyvalue=val)   

    val=get_value_of_excel_file(excel_file,row=12,column=7)
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                        keyname='temperature',
                                                        keyvalue=val)                                                                                                                   


for i in [1,2,4,5,7]:
    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                            keyname='uploader',
                                                            keyvalue='shimwell')

    list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
                                                            keyname='uploader',
                                                            keyvalue='shimwell')


#example for getting meta data from a file
# for i, filename in enumerate(list_of_csv_filenames):
#     list_of_json_objects[i] = add_meta_data_to_json_objects(json_object=list_of_json_objects[i],
#                                                         keyname='material',
#                                                         keyvalue=filename.split('/')[-1].split('_')[0])


#optional to write the json files containing meta data
#list_of_json_filenames_with_meta = write_json_files(json_objects=list_of_json_objects,filenames=[s + '_meta.json' for s in list_of_csv_filenames])


collection, client, db = connect_to_database()

delete_database(client)

upload_json_objects_to_database(list_of_json_objects,collection)

all_database_fields = get_database_fields(collection)

meta_data_fields = get_database_fields(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'TC1', 'TC2', 'TC3'])
#meta_data_fields = get_database_fields(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3'])
