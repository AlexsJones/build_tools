#! /usr/bin/env python
#################################################################################
#     File Name           :     services/teamcity_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:55]
#     Last Modified       :     [2016-09-19 14:56]
#     Description         :      
#################################################################################

class teamcity_service():
    def additional_options(self,parser):
        pass    
    def __init__(self):
        print("Started Teamcity Service...")
    def run(self, options):
        print("Running with options %s" % options)

