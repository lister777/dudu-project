from dudu.config import default_region
import boto3


def list_instances(inp_options={}):
    
    global instances
    region  = inp_options.get('--region',default_region)
    profile = inp_options.get('--profile')
    try:
        if profile:
            session = boto3.session.Session(profile_name=profile, region_name=region)
        else:
            session = boto3.session.Session(region_name=region)
            
        ec2 = session.resource('ec2')
            
        def check_tag(tags):
            if tags:
                for tag in tags:
                    if tag['Key'] == "Name":
                        return tag['Value']
            return " "

        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','pending']}])
        
        print("{:<5} {:<30} {:<23} {:<18} {:<12} {:<10} {:<15} {:<18} {:<10}".format("No.", "Name", 
            "Id", "Public IP", "Type", "State", "VPC_id", "Subnet_id", "Image_id"))
            
        for i, instance in enumerate(instances):
            print("{:<5} {:<30} {:<23} {:<18} {:<12} {:<10} {:<15} {:<18} {:<10}".format(
                i, check_tag(instance.tags), instance.id, instance.public_ip_address, instance.instance_type,
                list(instance.state.values())[-1], instance.vpc_id, instance.subnet_id, instance.image_id))
                
    except Exception as e:
        print(e)