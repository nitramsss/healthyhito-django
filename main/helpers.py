import json

def convert_to_array(string):
    return json.loads(string.replace("'", '"'))
    

        