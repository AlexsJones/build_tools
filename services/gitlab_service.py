#! /usr/bin/env python
#################################################################################
#     File Name           :     services/gitlab_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-21 13:59]
#     Last Modified       :     [2016-11-07 10:05]
#     Description         :      
#################################################################################
import gitlab
class gitlab_service():
    def additional_options(self, parser):
        parser.add_option("--gitlab_command",
                help="gitlab COMMAND to execute: trigger|log",
                metavar="COMMAND")
        parser.add_option("--gitlab_project",
                help="gitlab project e.g. username/project")
        parser.add_option("--gitlab_build_number",
                help="gitlab build number is used for fetching logs")
        parser.add_option("--gitlab_server",
                help="gitlab server url e.g. http://localhost")
        parser.add_option("--gitlab_token",
                help="gitlab private token  to login with")

    def __init__(self):
        print("Started Gitlab Service...")

    def run(self, options):
        print("Running with options %s " % options)
        if not options.gitlab_command:
            print("No command given to run...")
            exit(0)
        if not options.gitlab_server or not options.gitlab_token:
            print("No gitlab server defined")
            exit(0)
        if "trigger" in options.gitlab_command:
            if not options.gitlab_build_number:
                print("Requires build ID as the gitlab_build_number")
                exit(0)

            gl = gitlab.Gitlab(options.gitlab_server, options.gitlab_token)
            gl.auth()
        
        if "log" in options.gitlab_command:
            if not options.gitlab_build_number:
                print("Requires build ID as the gitlab_build_number")
                exit(0)
            if not options.gitlab_build_number:
                print("Requires build NUMBER as the gitlab_build_number")
                exit(0)

            gl = gitlab.Gitlab(options.gitlab_server, options.gitlab_token)
            gl.auth()
            if not options.gitlab_project:
                print("Requires gitlab project")
                exit(0)
            project = gl.projects.get(options.gitlab_project)

            build = project.builds.get(options.gitlab_build_number)

            print build
