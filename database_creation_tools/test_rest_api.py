from flask import Flask
import urllib
import json

from rest_api_database_functions import convert_query_string_to_query_dict

def test_find_meta_data_fields():

    with urllib.request.urlopen('http://127.0.0.1:5000/find_meta_data_fields') as response:
        json_contents = json.load(response)
    print(json_contents)
    assert 'filename' in json_contents
    assert 'uploader' in json_contents

def test_convert_query_string_to_query_dict():

    query_dict = convert_query_string_to_query_dict("{filename:file1}")
    
    keys = list(query_dict.keys())
    values = list(query_dict.values())

    print(keys)
    print(values)

    assert len(keys) == 1
    assert len(values) == 1

    assert keys[0]== 'filename' 
    assert values[0]== 'file1'

    query_dict = convert_query_string_to_query_dict("{filename:file1,uploader:shimwell}")
    
    keys = list(query_dict.keys())
    values = list(query_dict.values())

    print(keys)
    print(values)

    assert len(keys) == 2
    assert len(values) == 2

    assert keys[0]== 'filename' 
    assert values[0]== 'file1'
    assert keys[1]== 'uploader' 
    assert values[1]== 'shimwell'
