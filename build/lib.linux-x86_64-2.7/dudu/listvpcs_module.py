import boto3
import itertools

from config import default_region

def list_vpcs(inp_options={}):
    
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
            
        def check_defaultvpc(inp):
            if inp:
                return "(Default)"
            else:
                return ""

        def return_subnet(subnets_row):
            s = []
            for subnet in subnets_row:
                if subnet:
                    s.append(str('-{}, {}'.format(subnet.subnet_id, subnet.cidr_block)).ljust(45))
                else:
                    s.append(str('').ljust(45))
            return '|'.join(s)
                    
        vpc_iterator = ec2.vpcs.all()
            
        vpcs, subnets = [], []
        
        for vpc in vpc_iterator:
            vpcs.append(vpc)
            subnets.append(list(vpc.subnets.all()))
        subnets = list(itertools.zip_longest(*subnets, fillvalue=""))
        subnets.insert(0,tuple(vpcs))

        for i,k in enumerate(subnets):
            if i == 0:
                l = '|'.join(str('{}, {} {}'.format(x.vpc_id, check_tag(x.tags), check_defaultvpc(x.is_default))).ljust(45) for x in k)
            else:
                l = return_subnet(k)
            print(l)

    except Exception as e:
        print(e)