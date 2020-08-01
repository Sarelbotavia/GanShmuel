import requests
import json
#from flask import jsonify
import jsonschema
from jsonschema import validate
import pycurl
from io import BytesIO 

b_obj = BytesIO() 
crl = pycurl.Curl()
get_body = ''
#r = ''

def get(url):
    #REQUESTS !!!
    r = requests.get(url).json()
    print (r)
    # Set URL value
    crl.setopt(crl.URL, url)
    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)
    # Perform a file transfer 
    crl.perform() 
    # End curl session
    crl.close()
    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()
    # Decode the bytes stored in get_body to HTML and print the result 
    print('Output of GET request:\n%s' % get_body.decode('utf8'))
    #covert to jason - not nessercily must
    #body = json.loads(get_body.decode('utf-8'))
    return r
    #return get_body
    
def validateJson(jsonData,Schema):
    try:
        validate(instance=jsonData, schema=Schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

EXAMPLE = "https://jsonplaceholder.typicode.com/todos/1"
blue = "http://blue.develeap.com:8090/health"

scm = {
    #"type": "object",
    "properties": {
        'userId': {'type': 'number'},
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'completed': {'type': 'boolean'}
        },
    "required": [ "userId", "id", "title", "completed" ]
    }

health = {
    "type" : "array",
    "items" : [{
        "type" : "array",
        "items" : [{
            "type" : "number"
        }, {
            "type" : "string"
        }, {
            "type" : "string"
        }]
    }]
}


r = get(blue)
#validate it
isValid = validateJson(get_body,scm)
#print('Output of GET request:\n%s' % get_body.decode('utf8'))
if isValid:
    print("Given JSON data is Valid, moving to next test")
else:
    print("Given JSON data is InValid")

validate(instance=get_body, schema=scm)

#validate it
isValid = validateJson(r,health)
print (r)
if isValid:
    print("Given JSON data is Valid, moving to next test")
else:
    print("Given JSON data is InValid")

validate(instance=r, schema=health)

