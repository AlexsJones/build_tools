#! /usr/bin/env python
#################################################################################
#     File Name           :     build_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 11:31]
#     Last Modified       :     [2016-09-19 13:24]
#     Description         :      
#################################################################################
import os
import sys
import inspect
from optparse import OptionParser
def load_modules():
    res = {}
    lst = os.listdir("services")
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
        print("Loading %s" % d)
        a,_ = os.path.splitext(d)
        res[d] = __import__("services." + a,
                fromlist = ["*"])
        for name, obj in inspect.getmembers(res[d]):
            if inspect.isclass(obj):
                if a in obj.__name__:
                    try:
                        klass = getattr(res[d],a)
                        d = klass()
                        res[a] = d
                    except:
                        print("Error loading module %s" % a)
    return res
if __name__ == "__main__" :
    print("Loading Modules...")
    m = load_modules()
    # Options
    parser = OptionParser()
    parser.add_option("-s","--service",
            help="Name of the service to run e.g. shell")
    (options,args) = parser.parse_args()

    if not options.service:
        print("Please provide the name of a service module to run...")
        exit(0)

    service = options.service
    if not "_service" in options.service:
        service = options.service + "_service"

    if not service in m.keys():
        print("Service not found: %s" % service)
        exit(0)

    m[service].run(options)
