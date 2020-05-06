import boto3
import json
import logging 

log = logging.getLogger('aws')
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
log.setLevel(logging.DEBUG)

def create_access_key(userName):
    """
    func: createAccessKey() generate API keys and return the values. 
    Note: User can't have more than 2 API keys at a time.  
    error: LimitExceededException will occur
    """
    client = boto3.client('iam')
    try:
        response = client.create_access_key(
            UserName = userName 
        )
        json_data = json.dumps(response['AccessKey'], indent=4, sort_keys=True, default=str)
        return json_data
    except client.exceptions.LimitExceededException as err:
        log.error(err)

def list_access_keys(userName):
    result = []
    client = boto3.client('iam')
    try:
        response = client.list_access_keys(
            UserName = userName
        )
        try:
            for index in range(len(response['AccessKeyMetadata'])):
                result.append(response['AccessKeyMetadata'][index]['AccessKeyId'])
            return result
        except KeyError as err:
            log.error(err)
    except client.exceptions.NoSuchEntityException as err:
        log.error(err)

print(listAccessKeys('test-user'))
