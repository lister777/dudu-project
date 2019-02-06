from dudu.config import default_region
import boto3

def terminate_instances(inp_options={}):
    if len(inp_options) == 0:
        retrun
    
    region  = inp_options.get('--region',default_region)
    profile = inp_options.get('--profile')
    
    if profile:
        session = boto3.session.Session(profile_name=profile, region_name=region)
    else:
        session = boto3.session.Session(region_name=region)
        
    ec2_client   = session.client('ec2')
    ec2_resource = ec2 = session.resource('ec2')
    
    try:
        if '--instance-ids' in inp_options:
            instance_ids = inp_options['--instance-ids'].split(',')
        
        elif '--ids' in inp_options:
            instances = ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending']}])
            instance_ids = list()
            for i in inp_options.get('--ids').split(','):
                instance_ids.append(list(instances)[int(i)].instance_id)
        
        ec2_client.terminate_instances(InstanceIds=instance_ids)
    except Exception as e:
        print(e)
            
            
    
    