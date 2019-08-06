# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json
import os

"""
Getting started guide with Python3.x and Flask!
$ mkdir ./webhook
$ cd ./webhook
$ pip install Flask
$ vi app.py
$ python app.py
"""

app = Flask(__name__)

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class ResponseBody:
    def __init__(self, output_type=None, output_code='SUCCESS', output_values=None, extras=None):
        # NOTE: output_code = 'SUCCESS' or 'ERROR_[NUMBER]'
        self.outputType = output_type
        self.outputCode = output_code
        self.outputValues = output_values
        self.extras = extras


def handle_action(req_json):
    print(json.dumps(req_json, cls=CustomJsonEncoder, ensure_ascii=False))      

    action_name = req_json['action']['name']
    output_type = None if ('outputType' in req_json['action']) else req_json['action']['outputType']
    webhookPassThrough = req_json['webhookPassThrough'] # If you need
    context = req_json['context'] # If you need
    output_values = None

    if action_name == 'Show.Weather':
        # NOTE: Use the following parameters!!
        """
        req_json['action']['parameters'] = [
            {
                'name' : 'Time',
                'isMandatory' : 'true', 
                'isMultiple' : 'false',
                'openClass' : 'DEFAULT', 
                'origin' : "UserInput||Output",
                'values' : [
                    
                        '_value' : None
                    }

                ]
            },
            {
                'name' : 'Village',
                'isMandatory' : 'true', 
                'isMultiple' : 'false',
                'openClass' : 'DEFAULT', 
                'origin' : "UserInput||Output",
                'values' : [
                    
                        '_value' : None
                    }

                ]
            }
         ]
        """

        # TODO: Write your code here!!

        # NOTE: Your response MUST conform to the following. 
        # outputType = Weather
        output_values = [
            {
                'type' : None
            }
        ]
    elif action_name == 'Show.Temperature':
        # NOTE: Use the following parameters!!
        """
        req_json['action']['parameters'] = [
            {
                'name' : 'Time',
                'isMandatory' : 'true', 
                'isMultiple' : 'false',
                'openClass' : 'DEFAULT', 
                'origin' : "UserInput||Output",
                'values' : [
                    
                        '_value' : None
                    }

                ]
            },
            {
                'name' : 'Village',
                'isMandatory' : 'true', 
                'isMultiple' : 'false',
                'openClass' : 'DEFAULT', 
                'origin' : "UserInput||Output",
                'values' : [
                    
                        '_value' : None
                    }

                ]
            }
         ]
        """

        # TODO: Write your code here!!

        # NOTE: Your response MUST conform to the following. 
        # outputType = Temperature
        output_values = [
            {
                'degreesCelcius' : None
            }
        ]
        
    # NOTE: If necessary, you can return additional information in JSON format.
    extras = {} 
    return ResponseBody(output_type=output_type, output_code='SUCCESS', output_values=output_values, extras=extras)


@app.route(rule='/', methods=['POST'])
def handle_webhook():
    response = None

    try:
        # Handle action
        response_object = handle_action(request.get_json())

        # Response 200, OK
        response_json = json.dumps(response_object, cls=CustomJsonEncoder, ensure_ascii=False)
        response = Response(response_json, status=200, mimetype='application/json')
    except Exception as e:
        # 500, Internal Server Error
        print(e)
        response_object = ResponseBody(output_code='INTERNAL_SERVER_ERROR')
        response_json = json.dumps(response_object, cls=CustomJsonEncoder, ensure_ascii=False)
        response = Response(response_json, status=500, mimetype='application/json')

    return response


@app.route("/health")
def hello():
    return Response(None, status=200, mimetype='application/json')


if __name__ == "__main__":
    port = int(os.getenv('PORT', 27000))
    app.run(host='127.0.0.1', port=port)
