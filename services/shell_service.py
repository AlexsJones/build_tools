#! /usr/bin/env python
#################################################################################
#     File Name           :     services/shell.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 11:52]
#     Last Modified       :     [2016-09-19 13:24]
#     Description         :      
#################################################################################


class shell_service():
    def __init__(self):
        print("Started Shell Service...")
    def run(self, options):
        print("Running with options %s" % options)
