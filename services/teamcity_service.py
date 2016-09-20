#! /usr/bin/env python
#################################################################################
#     File Name           :     services/teamcity_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-19 14:55]
#     Last Modified       :     [2016-09-20 11:35]
#     Description         :      
#################################################################################
import json
import urllib2
import base64
import sys

class teamcity_service():
    def additional_options(self,parser):
        parser.add_option("--teamcity_command",
                help="teamcity COMMAND to execute: trigger|agents
                ",metavar="COMMAND")
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
   
    def build_full_url(self,resource):
        self.resource = self.tc_rest_url + resource
        full_url = self.resource
        if self.locators:
            locators = 'locator='+ ','.join([
                "%s:%s" % (k,v)
                for k,v in self.locators.iteritems()
                ])
        else:
            locators = ''
        get_args = '&'.join([locators] + [
            '%s=%s' % (k,v)
            for k, v in self.parameters.iteritems()
            ])
        if get_args:
            full_url = self.resource + '?' + get_args
        return full_url
   
    def build_request(self,resource):
        full_url = self.build_full_url(resource)
        print("Using full uri %s" % full_url)
        req = urllib2.Request(full_url)
        base64str = base64.encodestring(self.userpass).replace('\n','')
        req.add_header("Authorization","Basic %s" % base64str)
        req.add_header("Accept", "application/json")
        return req

    def send_with_response(self,req):
        response = urllib2.urlopen(req)
        res = response.read()
        data= json.loads(res)
        response.close()
        return data

    def __init__(self):
        self.tc_rest_url = "http://%s:%d/httpAuth/app/rest/"
        self.locators = {}
        self.parameters = {}
        self.userpass = '%s:%s'
        self.resource = ''
        print("Started Teamcity Service...")
    
    def run(self, options):
        self.tc_rest_url = "http://%s:%s/httpAuth/app/rest/"
        self.locators = {}
        self.parameters = {}
        self.resource = ''
        print("Running with options %s" % options)
        if not options.teamcity_command:
            print("No command given to run...")
        
        if not options.teamcity_server or not options.teamcity_port:
            print("No teamcity server defined")
            exit(0)

        self.tc_rest_url = self.tc_rest_url % (options.teamcity_server, 
                options.teamcity_port)

        if options.teamcity_user and options.teamcity_password:
            self.userpass = self.userpass % (options.teamcity_user, 
                    options.teamcity_password)

        if "test" in options.teamcity_command:
            req = self.build_request('agents')
            print(self.send_with_response(req))
