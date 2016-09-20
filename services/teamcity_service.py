#! /usr/bin/env python
#################################################################################
#     File Name           :     services/teamcity_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:55]
#     Last Modified       :     [2016-09-20 12:46]
#     Description         :      
#################################################################################
import json
import urllib2
import base64
import requests
import sys
from xml.sax.saxutils import quoteattr
class teamcity_service():
    def additional_options(self,parser):
        parser.add_option("--teamcity_command",
                help="teamcity COMMAND to execute: trigger",
                metavar="COMMAND")
        parser.add_option("--teamcity_command_args",
                help="teamcity command executable COMMAND arguments e.g." +   
                "COMMAND /buildfolder/123")
        parser.add_option("--teamcity_server",
                help="teamcity server url e.g. http://localhost")
        parser.add_option("--teamcity_port",
                help="teamcity server port e.g. 80")
        parser.add_option("--teamcity_user",
                help="teamcity user to login with")
        parser.add_option("--teamcity_password",
                help="teamcity password to login with")

    def __init__(self):
        print("Started Teamcity Service...")

    def run(self, options):
        print("Running with options %s" % options)
        if not options.teamcity_command:
            print("No command given to run...")

        if not options.teamcity_server or not options.teamcity_port:
            print("No teamcity server defined")
            exit(0)

        tc_rest_url = "http://%s:%s/httpAuth/app/rest/" % (options.teamcity_server, 
                options.teamcity_port)

        if "trigger" in options.teamcity_command:
            if not options.teamcity_command_args:
                print("Requires build ID as the teamcity_command_arg")
                exit(0)

            template = '<build><buildType id={id}/></build>'
            url = tc_rest_url + 'buildQueue'
            headers = {'Content-Type':'application/xml'}
            data = template.format(id=quoteattr(options.teamcity_command_args))

            r = requests.post(url,headers=headers,data=data,auth=(options.teamcity_user,
                options.teamcity_password),timeout=10) 

