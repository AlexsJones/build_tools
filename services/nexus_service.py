#! /usr/bin/env python
#################################################################################
#     File Name           :     services/nexus_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-11-14 13:27]
#     Last Modified       :     [2016-12-21 15:27]
#     Description         :      
#################################################################################
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from os.path import splitext,basename
import sys
import urllib.request, urllib.error, urllib.parse
import base64


class nexus_service():

    def additional_options(self, parser):
        parser.add_argument("--command",
                help="nexus COMMAND to execute: upload|download|delete",
                metavar="COMMAND")
        parser.add_argument("--nexus_server",
                help="nexus server url e.g. http://server/repository/myrepo/test.txt")
        parser.add_argument("--nexus_user",
                help="nexus user to login with")
        parser.add_argument("--nexus_password",
                help="nexus password to login with")
        parser.add_argument("--nexus_file",
                help="file to either upload or download e.g. /home/anon/file.txt")
        parser.add_argument("--nexus_download_file",
                help="path and name for downloaded file")

    def __init__(self):
            print("Started Nexus repository Service...")

    def run(self, options):
        if not options.command:
            print("No command given to run...")
            exit(0) 

        if not options.nexus_user or not options.nexus_password:
            print("Please give --nexus_user and --nexus_password")
            sys.exit(1)

        if options.command in "upload":
            print("Starting upload...")
            url = options.nexus_server
            dissambled = urlparse(url)
            filename, ext = splitext(basename(dissambled.path))
            headers = {}

            with open(options.nexus_file, 'rb') as f:
                content = f.read()
                request = urllib.request.Request(url, content, headers)
                
                base = base64.encodestring("%s:%s" % (options.nexus_user,
                    options.nexus_password)).replace('\n','')
                request.add_header("Content-type","application/x-gtar")
                request.add_header("Authorization", "Basic %s" % base) 
                request.get_method = lambda: 'PUT'
                response = urllib.request.urlopen(request)
                print((response.getcode()))

        if options.command in "download":
            print("Starting download...")
            url = options.nexus_server
            response = requests.get(url, stream=True, auth=HTTPBasicAuth(
                options.nexus_user,
                options.nexus_password))
            dissambled = urlparse(url)
            filename, ext = splitext(basename(dissambled.path))

            with open(options.nexus_download_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)

        if options.command == "delete":
            print("Deleting now...")
            url = options.nexus_server
            response = requests.delete(url, auth=HTTPBasicAuth(options.nexus_user, options.nexus_password))
