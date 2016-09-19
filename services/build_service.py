#! /usr/bin/env python
#################################################################################
#     File Name           :     services/build_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:36]
#     Last Modified       :     [2016-09-19 14:43]
#     Description         :      
#################################################################################

class build_service():
    def additional_options(self, parser):
        pass
    def __init__(self):
        print("Started Build Service...")
    def run(self, options):
        print("Running with options %s" % options)
