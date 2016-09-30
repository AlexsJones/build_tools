#! /usr/bin/env python
#################################################################################
#     File Name           :     services/build_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:36]
#     Last Modified       :     [2016-09-30 11:58]
#     Description         :      
#################################################################################
import os

class version_service():
    def additional_options(self, parser):
        parser.add_option("--version_increment",
                help="version_increment either creates or increments a version file") 
    def __init__(self):
        print("Started Build Service...")
    def increment_version(self,version_str):
        i = int(version_str)
        i += 1
        return "%06d" % i
        
    def create_version_file(self, path,opt_value=None):
        print("Creating version file...")
        with open(path,"w+") as a:
            if opt_value:
                print("Incrementing existing file...")
                a.write(opt_value + "\n")
            else:
                a.write("000000\n")
            a.close()
    def update_version_file(self, path):
        print("Using existing file...")
    
        with open(path,"a+") as f:
            i = str(f.read())
            n = self.increment_version(i)
            f.close()
            os.remove(path)
            self.create_version_file(path,n)
    def run(self, options):
        print("Running with options %s" % options)
        if options.version_increment:
            if os.path.isdir(options.version_increment):
                print("Cannot increment a directory...")
                exit(0)
            if  os.path.isfile(options.version_increment):#this logic seems inverse :S
                self.update_version_file(options.version_increment)
            else:
                self.create_version_file(options.version_increment)
