import boto3
import json
import time

client = boto3.client('ec2')

def lambda_handler(event, context):

    # Insert your Instance ID here
    instance_id = event.get('instance_id','')
    new_instance_type = event.get('new_instance_type','')    # m5.4xlarge, t3.2xlarge
    
    # Get instance information
    instance = {}
    try:
        print(f'Describe instance for {instance_id}')
        response = client.describe_instances(InstanceIds=[instance_id])
        reservations = response.get('Reservations', [])
        instances = reservations[0].get('Instances', []) if reservations else []
        instance = instances[0] if instances else {}
    except Exception as ex:
        print(ex)
        raise Exception(f'Instance with {instance_id} not found')
    
    # Get current instance type and state
    print(json.dumps(instance, indent=4, sort_keys=True, default=str))
    instance_type = instance.get('InstanceType')
    instance_state = instance.get('State')
    
    # No change required if same instance type
    if instance_type == new_instance_type:
        raise Exception(f'Same instance type {instance_type}. No change required.')
    
    # get the start time
    start_time = time.time()
    
    # Stop the instance
    print(f'Stopping instance {instance_id}')
    client.stop_instances(InstanceIds=[instance_id])
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])
    
    # Change the instance type
    print(f'Changing instance type from {instance_type} to {new_instance_type}')
    client.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=new_instance_type)
    
    # Start the instance
    print(f'Starting instance {instance_id}')
    client.start_instances(InstanceIds=[instance_id])
    # Wait till instance is running
    waiter=client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    # get the end time
    end_time = time.time()
    # get the execution time
    elapsed_time = end_time - start_time
    print('Execution time:', round(elapsed_time,1), 'seconds')


if __name__ == '__main__':
    event = { "instance_id": "i-07b8ea23e20d96173", "new_instance_type": "m5.4xlarge" }
    context = None
    lambda_handler(event, context)
