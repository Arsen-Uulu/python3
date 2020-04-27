import boto3
import os
import re 

client = boto3.client(
        'lambda'
        )

def list_functions(search_functions):
    try:
        checkout_functions = []
        result = []
        response = client.list_functions()
        data = [data for data in response['Functions']]
        for index in range(len(data)):
            r = re.compile('^'+search_functions)
            result.append(data[index]['FunctionName'])
            filtered_functions = list(filter(r.match, result))
        return filtered_functions
    except Exception as err:
        return err

def delete_functions(search_functions):
    try:
        function_names = list_functions(search_functions)
        for index in range(len(function_names)):
            response = client.delete_function(FunctionName = function_names[index])
        return response
    except InvalidParameterValueException:
        return "One of the parameters in the request is invalid."
