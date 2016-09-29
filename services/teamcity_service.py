#! /usr/bin/env python
#################################################################################
#     File Name           :     services/teamcity_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:55]
#     Last Modified       :     [2016-09-21 14:07]
#     Description         :      
#################################################################################
import json
import urllib2
import base64
import requests
import sys
from xml.sax.saxutils import quoteattr
from xml.dom import minidom

class teamcity_service():
    def additional_options(self,parser):
        parser.add_option("--teamcity_command",
                help="teamcity COMMAND to execute: trigger|log",
                metavar="COMMAND")
        parser.add_option("--teamcity_build_id",
                help="teamcity build id to work with") 
        parser.add_option("--teamcity_build_number",
                help="teamcity build number is used for fetching logs")
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
            exit(0)
        if not options.teamcity_server or not options.teamcity_port:
            print("No teamcity server defined")
            exit(0)

        tc_rest_url = "http://%s:%s/httpAuth/app/rest/" % (options.teamcity_server, 
                options.teamcity_port)

        if "trigger" in options.teamcity_command:
            if not options.teamcity_build_id:
                print("Requires build ID as the teamcity_build_id")
                exit(0)

            template = '<build><buildType id={id}/><comment><text>Build triggered via build_tools</text></comment></build>'
            url = tc_rest_url + 'buildQueue'
            headers = {'Content-Type':'application/xml'}
            data = template.format(id=quoteattr(options.teamcity_build_id))

            r = requests.post(url,headers=headers,data=data,auth=(options.teamcity_user,
                options.teamcity_password),timeout=10) 
            xmldoc = minidom.parseString(r.text)
            itemlist = xmldoc.getElementsByTagName('build')
            print("Started build with id %s and is available to view here %s" % 
                    (itemlist[0].attributes['id'].value,
                        itemlist[0].attributes['webUrl'].value))
        if "log" in options.teamcity_command:
            if not options.teamcity_build_number:
                print("Requires teamcity_build_number")
                exit(0)
            sub_url = tc_rest_url.replace('/app/rest/','/')
            url = sub_url+ "downloadBuildLog.html?buildId=" + options.teamcity_build_number
            r = requests.get(url,auth=(options.teamcity_user,options.teamcity_password),timeout=10)
            print(r.text)
