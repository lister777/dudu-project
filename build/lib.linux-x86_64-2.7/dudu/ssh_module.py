import listinstances_module
import subprocess
import os

def remote_ssh(number, user):
    instance    =   list(listinstances_module.instances)[int(number)]
    key_path    =   "{}/.ssh/{}.pem".format(os.path.expanduser("~"),instance.key_name)
    command     =   "ssh -i {} {}@{}".format(key_path, user, instance.public_ip_address)
    subprocess.call(command, shell=True)