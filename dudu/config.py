import boto3
import os


default_region = "ap-southeast-2"

dir_path = os.path.expanduser("~") + '/.dudu'
file = '/instance_template.json'
file_path = dir_path + file

option_dict = {
    'listinstances': ['--region', '--profile'],
    'listvpcs': ['--region', '--profile'],
    'runinstances': ['--region', '--profile' ,'--subnet-id', '--image-id', '--instance-type', '--name', '--instance-profile', '--key-name',
                '--security-groups','--template-name', '--copy-instance-from'],
    'configure':['--region', '--profile', '--subnet-id', '--image-id', '--instance-type', '--name', '--instance-profile', '--key-name',
                '--security-groups','--template-name', '--copy-instance-from'],
    'terminate':['--region', '--profile', '--instance-ids', '--ids']
    }
    
    
    
def option_verify(inp_dict, options):
    if list(inp_dict.values())[-1] and set(inp_dict.keys()).issubset(set(options)):
        return True
    else:
        return False
        
        
        
def get_instance(instance_id, session):
    
    ec2 = session.resource('ec2')

    instance = ec2.Instance(instance_id)
    
    subnet_id               = instance.subnet_id
    instance_type           = instance.instance_type
    key_name                = instance.key_name
    image_id                = instance.image_id
    instance_profile        = instance.iam_instance_profile.get('Arn') if instance.iam_instance_profile else None
    security_groups         = ','.join([i['GroupId'] for i in instance.security_groups])
    name                    = '{}_copy'.format(list(filter(lambda x: x['Key']=='Name', instance.tags))[0]['Value'])
    
    return {'subnet-id':subnet_id, 'instance-type':instance_type, 'key-name':key_name,'image-id':image_id,
            'instance-profile': instance_profile, 'name':name, 'security-groups':security_groups}