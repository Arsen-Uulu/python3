#!/usr/local/bin/python3
import boto3
from pprint import pprint
from kubernetes.client.rest import ApiException
import kubernetes.client
from kubernetes import client, config
import base64

def create_secret_objects(secret_name,name_space: str, lst: list):
    """
    function: create_secret_objects() creates Kubernetes Secret Object using credentilas from ~/.kube/config
    if Kubernetes Secret Object already exist it will perform update in place if your secret_list has new secrets
    args: 
        - secret_name - name of Secret Oject identified by Kubernetes
        - name_space  - name of the namespace where to create Secret Object
        - lst         - define a list in secrets.py file and import, list of secrets to get from AWS KMS
    """
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        metadata = {'name': secret_name, 'namespace': name_space, 'labels': {'name': secret_name}}
        namespace = name_space
        string_data = encode_64(lst)
        api_version,kind = 'v1','Secret'
        body = kubernetes.client.V1Secret(api_version, string_data, kind, metadata, type='Opaque')
        api_response = v1.create_namespaced_secret(namespace,body)
        pprint(api_response)
    except ApiException as err:
        if (err.reason == "Conflict") and (err.status == 409):
            api_response = v1.replace_namespaced_secret(secret_name, namespace, body)
            pprint(api_response)
        else:
            print("Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % err)

def encode_64(lst: list) -> dict:
    """
    function: encode64() return type <dict> with encoded base64 values
    args: lst - inherits lst argument from create_secret_objects() function
    """
    try:
        data = generate_secrets_data(lst)
        for k in data:
            try:
                values_bytes = data[k].encode('ascii') 
                base64_bytes = base64.b64encode(values_bytes)
                base64_value = base64_bytes.decode('ascii')
                data[k] = base64_value
            except Exception as err:
                return err
        return data 
    except Exception as err:
        return err

def generate_secrets_data(lst: list) -> dict:
    """
    function: generate_secrets_data() makes API call to AWS KMS and generates type <dict> with dict[secretName] = value and returns it
    """
    secrets_name_value = {}
    client = boto3.client('secretsmanager')
    for secret in lst:
        try:
            response = client.get_secret_value(
                SecretId = secret
            )
            secrets_name_value[response['Name']] = response['SecretString']
        except client.exceptions.ResourceNotFoundException as err:
            return err
    return secrets_name_value
