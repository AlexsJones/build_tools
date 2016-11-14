#! /usr/bin/env python
#################################################################################
#     File Name           :     services/build_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:36]
#     Last Modified       :     [2016-11-14 14:42]
#     Description         :      
#################################################################################
import os
import tarfile


class build_service():
    def additional_options(self, parser):
        parser.add_option("--build_command",
                help="use to decompress|compress directory")
        parser.add_option("--build_folder",
                help="build folder pass to compress or decompress")
        parser.add_option("--build_increment",
                help="build_increment either creates or increments a build file") 
    def __init__(self):
        print("Started Build Service...")
    def increment_build(self,build_str):
        i = int(build_str)
        i += 1
        return "%06d" % i
        
    def create_build_file(self, path,opt_value=None):
        print("Creating build file...")
        with open(path,"w+") as a:
            if opt_value:
                print("Incrementing existing file...")
                a.write(opt_value + "\n")
            else:
                a.write("000000\n")
            a.close()
    def update_build_file(self, path):
        print("Using existing file...")
    
        with open(path,"a+") as f:
            i = str(f.read())
            n = self.increment_build(i)
            f.close()
            os.remove(path)
            self.create_build_file(path,n)
    def run(self, options):
        print("Running with options %s" % options)
        if options.build_increment:
            if os.path.isdir(options.build_increment):
                print("Cannot increment a directory...")
                exit(0)
            if  os.path.isfile(options.build_increment):#this logic seems inverse :S
                self.update_build_file(options.build_increment)
            else:
                self.create_build_file(options.build_increment)
        if options.build_command == "decompress":
            tar = tarfile.open(options.build_folder)
            tar.extractall()
            tar.close()

        if options.build_command == "compress":
            output_file = options.build_folder + ".tar.gz"
            with tarfile.open(output_file, "w:gz") as tar:
                tar.add(options.build_folder, arcname=os.path.basename(options.build_folder))
