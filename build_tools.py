#! /usr/bin/env python
#################################################################################
#     File Name           :     build_service.py
#     Created By          :     AlexsJones
#     Creation Date       :     [2016-09-19 11:31]
#     Last Modified       :     [2016-11-14 16:33]
#     Description         :
#################################################################################
import os
import sys
import inspect
import argparse
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
#   def additional_args.self, parser):
#       parser.add_argument("-c","--command",help="")
#   def run(self):
#       print("Running with %s, args.command)
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
                        # Load additional args.from Modules
                        # Generate sub parser
                        short = a.split("_")[0]
                        module_parser = parser.add_parser(short)
                        d.additional_options(module_parser)
                        res[a] = d
                    except:
                        print("Error loading module %s" % a)
    return res

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    print("Loading Modules...")
    
    subparsers = parser.add_subparsers(help="You can get submodule specific help with [module name] --help",
            dest="subparser_name")
    m = load_modules(subparsers)

    args = parser.parse_args()
    if "_service" not in args.subparser_name:
        args.subparser_name += "_service"
    m[args.subparser_name].run(args)
