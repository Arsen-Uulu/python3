import boto3

client = boto3.client('ecs')

def list_task_definitions(serviceName,taskStatus="ACTIVE",sortOrder='DESC'):
    """
    func: list_task_definitions() return list of taskDefinition arn's depending on arguments

    """
    try:
        response = client.list_task_definitions(
                familyPrefix = serviceName,
                status       = taskStatus,
                sort         = sortOrder
                )
        return response['taskDefinitionArns'] 
    except KeyError as err:
        return err,"Unable to describe task definition"

def get_active_task_definition(taskDefinition):
    """
    func: get_active_task_definition() returns ACTIVE TaskDefinition currently running.

    """
    try:
        response = client.describe_task_definition(taskDefinition=taskDefinition)   
        return response['taskDefinition']['taskDefinitionArn']
    except KeyError as err:
        return err,"Wrong Key"

def delete_not_active_task_definitions(taskDefinitionName):
    """
    func: delete_not_active_task_definitions() deactivates taskDefinitions,

    """
    result = []
    try:
        task_definitions = list_task_definitions(taskDefinitionName)
        active_task_definition = get_active_task_definition(taskDefinitionName)
        for task in task_definitions:
            if task == active_task_definition:
                task_definitions.remove(task)
                if len(task_definitions) == 0:
                    return task, "ACTIVE"
                break
        for task in task_definitions:
            result.append(task)
            response = client.deregister_task_definition(taskDefinition=task)
        return result,response['taskDefinition']['status']
    except Exception as err:
        return err, "Couldn't remove item from the list"
