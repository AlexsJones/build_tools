#! /usr/bin/env python
#################################################################################
#     File Name           :     services/shell.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 11:52]
#     Last Modified       :     [2016-11-14 16:34]
#     Description         :      
#################################################################################
from optparse import OptionParser
from subprocess import call


class shell_service():

    def additional_options(self,parser):
        parser.add_argument("--command",
                help="Shell service command to run e.g. ls", required=True)
        
        parser.add_argument("--command_args",
                help="Shell service command arguments for the given command")

    def __init__(self):
        print("Started Shell Service...")
    
    def run(self, options):
        print("Running with options %s" % options)
        if not options.command:
            print("No command given to run...")
        args = ""
        if options.command_args:
            args = options.command_args
        if options.command:
            call([options.command, args])
