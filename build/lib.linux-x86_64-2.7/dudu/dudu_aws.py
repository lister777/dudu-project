from cmd import Cmd
import sys
sys.path.append('..')
from config import option_dict, option_verify


import subprocess
import itertools

import listinstances_module
import configure_module
import ssh_module
import runinstances_module
import terminate_module
import listvpcs_module

class MyPrompt(Cmd):
    prompt = 'Dd> '
    intro = "Welcome! Type ? to list commands"
    
    def traverse(self,tokens,tree):
        if tree is None:
            return []
        elif len(tokens) == 1:
            if tokens[0] in tree:
                return []
            else:
                return [x[2:] for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree:
                tree.remove(tokens[0])
            return self.traverse(tokens[1:],tree)
            
    def command_complete(self, command_name, line):
        options = option_dict[command_name]
        try:
            tokens = [t for t in line.split() if t.startswith('--')]
            if len(tokens) == 0:
                return []
            else:
                results = self.traverse(tokens,options)
                return results
        except Exception as e:
            print(e)

    def do_exit(self, inp):
        # exit the application. Shorthand: x q.
        print("Bye")
        return True
    
    def do_configure(self, inp):
        options = option_dict['configure']
        warning = "Invaild options. Example: configure --template-name"
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                configure_module.configure_template_options(inp_dict)
            else:
                print(warning)
        else:
            configure_module.configure_template()
            
    def complete_configure(self, text, line, start_index, end_index):
        return self.command_complete('configure', line)

    def do_listinstances(self, inp):
        options = option_dict['listinstances']
        warning = "Invaild options. Example: list --region us-east-1"
        
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                listinstances_module.list_instances(inp_dict)
            else:
                print(warning)
        else:
            listinstances_module.list_instances()
          
          
    def complete_listinstances(self, text, line, start_index, end_index):
        return self.command_complete('listvpcs', line)
        
    def do_listvpcs(self, inp):
        options = option_dict['listvpcs']
        warning = "Invaild options. Example: list --region us-east-1"
        
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                listvpcs_module.list_vpcs(inp_dict)
            else:
                print(warning)
        else:
            listvpcs_module.list_vpcs()
          
          
    def complete_listvpcs(self, text, line, start_index, end_index):
        return self.command_complete('listvpcs', line)
        
    def do_runinstances(self, inp):
        options = option_dict['runinstances']
        warning = "Invaild options."
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                runinstances_module.run_instances(inp_options=inp_dict)
            else:
                print(warning)
        else:
            runinstances_module.run_instances()
    
    def complete_runinstances(self, text, line, start_index, end_index):
        return self.command_complete('runinstances', line)
        
    def do_terminate(self,inp):
        options = option_dict['terminate']
        warning = "Invaild options."
        if inp:
            inp_dict = dict(itertools.zip_longest(*[iter(inp.split())] * 2, fillvalue=""))
            if option_verify(inp_dict, options):
                terminate_module.terminate_instances(inp_options=inp_dict)
            else:
                print(warning)
        else:
            runinstances_module.terminate_instances()
            
    def complete_terminate(self, text, line, start_index, end_index):
        return self.command_complete('terminate', line)
            
    def do_ssh(self, inp, user="ec2-user"):
        ssh_module.remote_ssh(inp, user)

    def do_shell(self, inp):
        subprocess.call(inp, shell=True)

    def default(self, inp):
        if inp == ':x' or inp == ':q':
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    def emptyline(self):
        pass

def main():
    t = MyPrompt()
    t.cmdloop()
    
main()