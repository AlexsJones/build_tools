#! /usr/bin/env python
#################################################################################
#     File Name           :     services/gitlab_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-21 13:59]
#     Last Modified       :     [2016-12-16 20:01]
#     Description         :
#################################################################################
import gitlab
import datetime

class gitlab_service():

    def additional_options(self, parser):
        parser.add_argument("--command",
                help="gitlab COMMAND to execute: log|print_stats|suggest_prune_branches",
                metavar="COMMAND")
        parser.add_argument("--gitlab_project",
                help="gitlab project e.g. username/project")
        parser.add_argument("--gitlab_build_number",
                help="gitlab build number is used for fetching logs")
        parser.add_argument("--gitlab_server",
                help="gitlab server url e.g. http://localhost")
        parser.add_argument("--gitlab_token",
                help="gitlab private token  to login with")
        parser.add_argument("--gitlab_status",
                help="gitlab build status e.g. failed")
        parser.add_argument("--gitlab_max_size",
                            help="max size of pagination (branches/merges", default=1500)

    def __init__(self):
        print("Started Gitlab Service...")

    def parse_datetime(d):
        s = d.split('-')
        sub_split = s[2].split('T')
        f = "%s/%s/%s" % (sub_split[0], s[1], s[0][-2:])
        dt = datetime.strptime(f, "%d/%m/%y")
        return dt

    def walk_merge_request(self,project,max_size, comparison_operator=None):
        mr = project.mergerequests.list(per_page=max_size)
        for m in mr:
            comparison_operator(m)

    def run(self, options):
        print("Running with options %s " % options)
        if not options.command:
            print("No command given to run...")
            exit(0)
        if not options.gitlab_server:
            print("No gitlab server defined")
            exit(0)
        if not options.gitlab_token:
            print("No gitlab token defined")
            exit(0)

        gl = gitlab.Gitlab(options.gitlab_server, options.gitlab_token)
        gl.auth()

        if "log" in options.command:
            if not options.gitlab_build_number:
                print("Requires build NUMBER as the gitlab_build_number")
                exit(0)

            if not options.gitlab_project:
                print("Requires gitlab project")
                exit(0)

            project = gl.projects.get(options.gitlab_project)
            build = project.builds.get(options.gitlab_build_number)
            print(build)

        if "list_builds" in options.command:
            if not options.gitlab_status:
                print ("Requires a status to be given")
                exit(0)

            if options.gitlab_build_number:
                print ("Please don't define a build number")
                exit(0)

            project = gl.projects.get(options.gitlab_project)
            builds = project.builds.list()
            fails = []
            for k in builds:
                if k.status == options.gitlab_status:
                    string_id = str(k.id)
                    fails.append(string_id)
            if not fails:
                print ("No builds were makred as " + options.gitlab_status )
            else:
                print ("The following Builds were marked as " + options.gitlab_status)
                url = "https://gitlab.intranet.sky/ce-devices-ios/Benji/builds/"
                for i in fails:
                    print (url + i)

        if "suggest_prune_branches":
            if not options.gitlab_project:
                print("Requires gitlab project e.g. myname/project")
                exit(0)

            branches = set([])

            def comparison(merge):
                if not merge.state:
                    return
                if merge.state == 'merged':
                    branches.add(merge.source_branch)
            p = gl.projects.get(options.gitlab_project)
            self.walk_merge_request(p, options.gitlab_max_size, comparison)

            for b in branches:
                print(b)

        if "print_stats":
            if not options.gitlab_project:
                print("Requires gitlab project e.g. myname/project")
                exit(0)

            def comparison_operator(merge):
                pass

            p = gl.projects.get(options.gitlab_project)
            self.walk_merge_request(p, options.gitlab_max_size,comparison_operator)