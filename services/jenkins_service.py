#! /usr/bin/env python
#################################################################################
#     File Name           :     services/jenkins_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-21 13:59]
#     Last Modified       :     [2016-11-14 15:42]
#     Description         :      
#################################################################################
import jenkinsapi
from jenkinsapi.jenkins import Jenkins


class jenkins_service():

    def additional_options(self, parser):
        parser.add_argument("--command",
                help="jenkins COMMAND to execute: trigger|log",
                metavar="COMMAND")
        parser.add_argument("--jenkins_build_id",
                help="jenkins build id to work with") 
        parser.add_argument("--jenkins_build_number",
                help="jenkins build number is used for fetching logs")
        parser.add_argument("--jenkins_server",
                help="jenkins server url e.g. http://localhost")
        parser.add_argument("--jenkins_port",
                help="jenkins server port e.g. 80")
        parser.add_argument("--jenkins_user",
                help="jenkins user to login with")
        parser.add_argument("--jenkins_password",
                help="jenkins password to login with")

    def __init__(self):
        print("Started Jenkins Service...")

    def run(self, options):
        print("Running with options %s " % options)
        if not options.command:
            print("No command given to run...")
            exit(0)
        if not options.jenkins_server or not options.jenkins_port:
            print("No jenkins server defined")
            exit(0)
        if "trigger" in options.command:
            if not options.jenkins_build_id:
                print("Requires build ID as the jenkins_build_id")
                exit(0)
            j = Jenkins("http://%s:%s" % (options.jenkins_server,options.jenkins_port),
                    username=options.jenkins_user,password=options.jenkins_password)
            params = {}
            j.build_job(options.jenkins_build_id,params)

        if "log" in options.command:
            if not options.jenkins_build_id:
                print("Requires build ID as the jenkins_build_id")
                exit(0)
            if not options.jenkins_build_number:
                print("Requires build NUMBER as the jenkins_build_number")
                exit(0)
            j = Jenkins("http://%s:%s" % (options.jenkins_server,options.jenkins_port),
                    username=options.jenkins_user,password=options.jenkins_password)
          
            job = j[options.jenkins_build_id]
            print(job) 
