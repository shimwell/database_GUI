




from data_formatting_tools import *
from database_tools import *

import sys

list_of_json_objects = read_in_json_file('a/list_of_data.txt')
print(list_of_json_objects[0])

collection, client, db = connect_to_database()

delete_database(client)

upload_json_objects_to_database(list_of_json_objects,collection)

all_database_fields = get_database_fields(collection)

print('all_database_fields',all_database_fields)