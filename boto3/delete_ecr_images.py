import boto3 

client = boto3.client('ecr')

def list_images(registry_id, registry_name:str, tag_status:str) -> list: # registryId is AWS Account number 
    """
    func: list_images() returns a list of docker images stored in ECR for any given RepoName
    """
    try: 
        result = []
        response = client.list_images(
                registryId = registry_id,
                repositoryName = registry_name,
                filter={
                    'tagStatus': tag_status # tagStasus Options ANY | TAGGED | UNTAGGED
            }
        )
        for index in range(len(response['imageIds'])):
            result.append(response['imageIds'][index]['imageDigest'])
        return result
    except KeyError as err:
        return err,'Wrong key'

def batch_delete_images(registry_id:str, registry_name:str, tag_status:str) -> dict: 
    """
    func: batch_delete_images() calls list_images() to do batch delete of returned docker images

    """
    try:
        img_to_del = list_images(registry_id,registry_name,tag_status) 
        for index in range(len(img_to_del)):
            response = client.batch_delete_image(
                    registryId = registry_id,
                    repositoryName = registry_name,
                    imageIds = [
                        {
                            'imageDigest': img_to_del[index]
                        }
                    ]
            )
        return response
    except KeyError as error:
        return error, 'Could not delete images, Invalid Key'
