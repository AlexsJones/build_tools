#! /usr/bin/env python
#################################################################################
#     File Name           :     build_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 11:31]
#     Last Modified       :     [2016-09-29 08:03]
#     Description         :      
#################################################################################
import os
import sys
import inspect
from optparse import OptionParser
# Configuration
SERVICES_PATH="services"
# ------------------------
# Services must follow the following format
# Folder -> services
# Name -> %s_service 
# Bootstrap classname -> %s_service
# Bootstrap class required methods
# class name_service:
#   def __init__(self):
#       print("Starting name_service...")
#   def additional_options(self, parser):
#       parser.add_option("-c","--command",help="")
#   def run(self,options):
#       print("Running with %s, options.command)
# -----------------------

def load_modules(parser):
    res = {}
    lst = os.listdir(SERVICES_PATH)
    dir = []
    for d in lst:
        s = os.path.abspath("services") + os.sep + d
        file,ext = os.path.splitext(s)
        if "__init__" in d:
            continue
        if ext == ".pyc":
            continue
        if os.path.isdir(s):
            continue   
        dir.append(d)
    for d in dir:
        a,_ = os.path.splitext(d)
        res[d] = __import__(SERVICES_PATH + "." + a,
                fromlist = ["*"])
        for name, obj in inspect.getmembers(res[d]):
            if inspect.isclass(obj):
                if a in obj.__name__:
                    try:
                        klass = getattr(res[d],a)
                        d = klass()
                        # Load additional options from Modules
                        d.additional_options(parser)                        
                        res[a] = d
                    except:
                        print("Error loading module %s" % a)
    return res

if __name__ == "__main__" :
    # Create parser
    parser = OptionParser()
    print("Loading Modules...")
    m = load_modules(parser)
    # build_service options
    parser.add_option("-s","--service",
            help="Name of the SERVICE to run e.g. shell",metavar="SERVICE")
    parser.add_option("-l","--list",
            action="store_true",
            help="List all SERVICE")
    parser.add_option("-d","--describe",
            help="Describe a SERVICE",metavar="SERVICE")

    (options,args) = parser.parse_args()
    if options.list:
        d = []
        for i in m.keys():
            if ".py" not in i:
                d.append(i)
        print("Services installed: " + str(d))
        exit(0)
    if options.describe:
        s = options.describe
        if not "_service" in options.describe:
            s = options.describe + "_service"
        print("Describing service..")
        try:
            members = inspect.getmembers(m[s],predicate=inspect.ismethod)
            print(s + " has members:")
            for m in members:
                print m[0]
    
        except:
            print("Service not found")
        exit(0)
    if not options.service:
        print("Please provide the name of a service module to run...")
        exit(0)
    # Run selected module
    service = options.service
    if not "_service" in options.service:
        service = options.service + "_service"
    if not service in m.keys():
        print("Service not found: %s" % service)
        exit(0)

    m[service].run(options)
