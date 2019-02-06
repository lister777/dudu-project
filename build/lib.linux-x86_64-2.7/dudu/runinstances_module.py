from config import default_region, dir_path, file_path,get_instance

import boto3
import json
import os


def run_instances(inp_options={}):
    region  = inp_options.get('--region',default_region)
    profile = inp_options.get('--profile')
    
    if profile:
        session = boto3.session.Session(profile_name=profile, region_name=region)
    else:
        session = boto3.session.Session(region_name=region)
    
    
    try:
        if "--copy-instance-from" in inp_options:
            copy_from_instance  = inp_options.get('--copy-instance-from')
    
            instance_template = get_instance(copy_from_instance, session)
            
        elif "--template-name" in inp_options:
            with open(file_path, 'r') as f:
                instance_template = json.loads(f.read())[inp_options['--template-name']]
    
        else:
            with open(file_path, 'r') as f:
                instance_template = json.loads(f.read())['default']
        
        subnet_id               = inp_options.get('--subnet-id',instance_template['subnet-id'])
        instance_type           = inp_options.get('--instance-type',instance_template['instance-type'])
        key_name                = inp_options.get('--key-name',instance_template['key-name'])
        image_id                = inp_options.get('--image-id',instance_template['image-id'])
        name                    = inp_options.get('--name',instance_template['name'])
        iam_instance_profile    = {'Arn': inp_options.get('--instance-profile',instance_template['instance-profile'])}
        security_groups         = inp_options.get('--security-groups',instance_template['security-groups']).split(',')
        
        
            
        ec2 = session.client('ec2')
        
        ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            SecurityGroupIds=security_groups,
            SubnetId=subnet_id,
            KeyName=key_name,
            IamInstanceProfile=iam_instance_profile,
            MinCount=1,
            MaxCount=1,
            DryRun=False,
            TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': name
                            },
                        ]
                    },
                ],
            )
    except Exception as e:
        print(e)
