import json
import os
from dudu.config import dir_path, file_path, get_instance, default_region
import boto3

def configure_template():
   # configure the instance launch template
   
    region              =  input("region: ")
    vpc_id              =  input("vpc-id: ")
    subnet_id           =  input("subnet-id: ")
    image_id            =  input("image-id: ")
    instance_type       =  input("instance-type: ")
    name                =  input("instance-name: ")
    instance_profile    =  input("instance-profile : ")
    key_name            =  input("SSH-Key: ")
    security_groups     =  input("security_groups: ")
    template_name       =  input("template-name: ")
    
    template = {
        "region":                   region,
        "vpc-id":                   vpc_id,
        "subnet-id":                subnet_id,
        "image-id":                 image_id,
        "instance-type":            instance_type,
        "name":                     name,
        "instance-profile":         instance_profile,
        "key-name":                 key_name,
        "security-groups":          security_groups
    }

    if not os.path.exists(file_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        open(file_path, 'a').close()
    
    with open(file_path, 'r') as f:
        template_file = f.read()
        if template_file:
            template_json = json.loads(template_file)
            template_json[template_name] = template
        else:
            template_json = {template_name:template}
            
    with open(file_path, 'w') as f:        
        template_file = json.dumps(template_json, sort_keys=True, indent=4)
        f.write(template_file)
    
    print(template_name, "is saved.")
    print(template_file)
    
    
    
def configure_template_options(inp_options):
    # configure/modify instance launch template with options

    try:
        with open(file_path, 'r') as f:
            template_file = f.read()
            template_name = inp_options.pop('--template-name', 'default')
        
        if '--copy-instance-from' in inp_options:
            region = inp_options.pop('--region', default_region)
            copy_from_instance = inp_options.pop('--copy-instance-from')
            profile = inp_options.pop('--profile','')
            
            if profile:
                session = boto3.session.Session(profile_name=profile, region_name=region)
            else:
                session = boto3.session.Session(region_name=region)
            
            instance_json = get_instance(copy_from_instance, session)
            if inp_options:
                for k, v in inp_options.items():
                    instance_json[k[2:]] = v
            
            if template_file:
                template_json = json.loads(template_file)
                template_json[template_name] = instance_json
            else:
                template_json = {template_name:instance_json}
                
        elif template_file:
            template_json = json.loads(template_file)
            if inp_options:
                for k, v in inp_options.items():
                    template_json[template_name][k[2:]] = v
        else:
            template_json = {template_name:inp_options}
                
        with open(file_path, 'w') as f:   
            template_file = json.dumps(template_json, sort_keys=True, indent=4)
            f.write(template_file)

        print(template_name, "is updated.")
        print(template_file)
            
    except Exception as e:
        print("Exception: ", str(e))