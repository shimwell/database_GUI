from flask import Flask
from flask import Flask, jsonify, render_template, request, Response, send_file


import json
import pandas as pd

import requests
import json
from bson import json_util
from bson.objectid import ObjectId
import requests
import re
from flask import Flask
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS, cross_origin
import os
from data_formatting_tools import *
from database_tools import *
from io import BytesIO
from io import StringIO

#collection, client, db = connect_to_database()
collection, client, db = connect_to_docker_database()

all_database_fields = get_database_fields(collection)


# meta_data_fields = get_database_fields(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3'])
# print(meta_data_fields)

meta_data_fields = find_all_fields_not_of_a_particular_types_in_database(collection,'list')
print('meta_data_fields',meta_data_fields)

axis_option_fields = find_all_fields_of_a_particular_types_in_database(collection,'list')
print('axis_option_fields',axis_option_fields)

# metadata_values=[]
metadata_fields_and_their_distinct_values={}
for entry in meta_data_fields:
    values = get_entries_in_field(collection,entry)
    # metadata_values.append(values)
    metadata_fields_and_their_distinct_values[entry]=values


meta_data_fields_and_distinct_entries = []
for field in meta_data_fields:
    meta_data_fields_and_distinct_entries.append({'field':[field],'distinct_values':metadata_fields_and_their_distinct_values[field]})

#print(meta_data_fields_and_distinct_entries)
#print(find_metadata_fields_and_their_distinct_values(collection, ignore_fields=['Time [sec]', 'Stroke', 'Extens', 'Load', 'Temp1', 'Temp2', 'Temp3']))

# print('all_database_fields',all_database_fields)
# print('meta_data_fields',meta_data_fields)
# print('meta_data_fields',metadata_values)


template_dir = os.path.abspath('../build')
static_dir= os.path.abspath("../build/static")
print('static_dir',static_dir)
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir )

CORS(app)


def convert_query_string_to_query_dict(query_string):
    try:
        query ={}
        for x in query_string.strip('{}').split(','):
            entry=x.split(':')
            query[entry[0]]=entry[1]
    except:
        query={}
    return query


def get_entries_in_field(collection, field, query=None):
    if query != {}:
      result = collection.distinct(field,query)
    else:
      result = collection.distinct(field)
    return result


@app.route('/download_py2' ,methods=['GET','POST'])
@cross_origin()
def download2():
    ids = request.args.get('ids')
    ids = ids.strip("'")
    ids = ids.strip('"')
    ids = ids.strip("[")
    ids = ids.strip("]")
    ids = ids.split(',')
    list_of_matching_database_entries = []
    print('ids', ids  )
    for id in ids:
        id = id.strip("'")
        id = id.strip('"')        
        print('id', id)
        query={'_id':{"$oid":id}}
        result = collection.find_one(query)
        results_json = json_util.dumps(result)
        list_of_matching_database_entries.append(results_json)
    file_data = str(list_of_matching_database_entries)
    print('making file')
    return send_file(BytesIO(file_data), attachment_filename='test.txt', as_attachment=True)


@app.route('/download_py3' ,methods=['GET','POST'])
@cross_origin()
def download4():
    ids = request.args.get('ids')
    ids = ids.strip("'")
    ids = ids.strip('"')
    ids = ids.strip("[")
    ids = ids.strip("]")
    ids = ids.split(',')
    list_of_matching_database_entries = []
    print('ids', ids  )
    for id in ids:
        id = id.strip("'")
        id = id.strip('"')             
        print('id', id)
        query={'_id':ObjectId(id)}
        result = collection.find_one(query)
        results_json = json_util.dumps(result)
        list_of_matching_database_entries.append(results_json)

    file_data = BytesIO()
    # file_data = StringIO()
    file_data.write(str(list_of_matching_database_entries).encode('utf-8'))
    #file_data.write(b'list_of_matching_database_entries')
    file_data.seek(0)
    print('making file')
    return send_file(file_data, attachment_filename='my_data.txt', as_attachment=True)



@app.route('/find_distinct_entries' ,methods=['GET','POST'])
@cross_origin()
def find_distinct_entries():
    field = request.args.get('field')
    print('field',field)
    distinct_entries = metadata_fields_and_their_distinct_values[field]
    print(distinct_entries)
    return jsonify(distinct_entries)


@app.route('/find_distinct_entries_in_a_field' ,methods=['GET','POST'])
@cross_origin()
def find_distinct_entries_in_a_field():
    field = request.args.get('field')
    query_string = request.args.get('query')

    query = convert_query_string_to_query_dict(query_string)

    result = get_entries_in_field(collection, field, query)

    return jsonify(result)



@app.route('/find_meta_data_fields' ,methods=['GET','POST'])
@cross_origin()
def find_meta_data_fields():
    return jsonify(meta_data_fields)

@app.route('/find_axis_data_fields' ,methods=['GET','POST'])
@cross_origin()
def find_axis_data_fields():
    return jsonify(axis_option_fields)


@app.route('/find_meta_data_fields_and_distinct_entries' ,methods=['GET','POST'])
@cross_origin()
def find_meta_data_fields_and_distinct_entries():
    return jsonify(meta_data_fields_and_distinct_entries)




@app.route('/get_number_of_matching_entrys' ,methods=['GET','POST'])
@cross_origin()
def get_number_of_matching_entrys():
    query_string = request.args.get('query')

    query = convert_query_string_to_query_dict(query_string)

    results = collection.find(query)
    counter=0
    for document in results:
        counter=counter+1
    return jsonify(counter)


@app.route('/get_matching_entrys' ,methods=['GET','POST'])
@cross_origin()
def get_matching_entrys():
    query_string = request.args.get('query')
    limit = request.args.get('limit', default=100, type=int)

    print('query_string',query_string)
    try:
        query ={}
        query_string= query_string.replace('"', '').replace("'", '')
        for x in query_string.strip('{}').split(','):
            entry=x.split(':')
            query[entry[0]]=entry[1]
    except:
        query={}
    print('query = ',query)
    result = collection.find(query).limit(limit)
    results_json = json_util.dumps(result)
    return results_json

@app.route('/get_matching_entrys_limited_fields' ,methods=['GET','POST'])
@cross_origin()
def get_matching_entrys_limited_fields():
    query_string = request.args.get('query')
    requested_fields_string = request.args.get('fields')
    limit = request.args.get('limit', default=100, type=int)



    print('query_string',query_string)
    print('fields_string',requested_fields_string)

    try:
        query ={}
        query_string= query_string.replace('"', '').replace("'", '')
        for x in query_string.strip('{}').split(','):
            entry=x.split(':')
            query[entry[0]]=entry[1]
    except:
        query={}

    try:
        fields ={}
        requested_fields_string= requested_fields_string.replace('"', '').replace("'", '')
        for x in requested_fields_string.strip('{}').split(','):
            entry=x.split(':')
            fields[entry[0]]=int(entry[1])
    except:
        fields={}


    print('fields = ',fields)
    print('query = ',query)

    result = collection.find(query,fields).limit(limit)
    results_json = json_util.dumps(result)
    return results_json


@app.route('/get_matching_entry' ,methods=['GET','POST'])
@cross_origin()
def get_matching_entry():
    query_string = request.args.get('query')

    print('query_string',query_string)
    try:
        query ={}
        query_string= query_string.replace('"', '').replace("'", '')
        for x in query_string.strip('{}').split(','):
            entry=x.split(':')
            query[entry[0]]=entry[1]
    except:
        query={}
    print('query = ',query)
    result = collection.find_one(query)
    results_json = json_util.dumps(result)
    return results_json



@app.route('/index' ,methods=['GET','POST'])
@cross_origin()
def return_index():
    return render_template('index.html')


@app.route('/' ,methods=['GET','POST'])
@cross_origin()
def return_index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
