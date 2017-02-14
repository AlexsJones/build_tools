#! /usr/bin/env python
#################################################################################
#     File Name           :     services/gitlab_service.py
#     Created By          :     anon
#     Creation Date       :     [2016-09-21 13:59]
#     Last Modified       :     [2017-02-10 13:49]
#     Description         :
#################################################################################
import datetime
from datetime import datetime, timedelta
from utils.rate_limit import RateLimited


def parse_datetime(d):
    s = d.split('-')
    sub_split = s[2].split('T')
    f = "%s/%s/%s" % (sub_split[0], s[1], s[0][-2:])
    dt = datetime.strptime(f, "%d/%m/%y")
    return dt

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
                            help="max size of pagination (branches/merges", default=2000)
        parser.add_argument("--gitlab_stats_start_date",
                            help="For pruning and stats this overrides the default start date please use DD/M/YYYY")
        parser.add_argument("--gitlab_stats_end_date",
                            help="For pruning and stats this overrides the default start date please use DD/M/YYYY")

    def __init__(self):
        print("Started Gitlab Service...")

    def walk_merge_request(self, max_size, gitlab_token, gitlab_url, comparison_operator=None):

        import requests
        headers = {'PRIVATE-TOKEN': gitlab_token}
        raw = requests.get(gitlab_url, headers=headers, verify=False)
        first_json = raw.json()

        data = []
        data.append(first_json)
        num_pages = raw.headers['x-total-pages']

        for page in range(2, int(num_pages) + 1):
            r = requests.get(gitlab_url + "?page=" + str(page), headers=headers, verify=False, params={'page': page})
            data.append(r.json())

        for cpage in data:
            for m in cpage:
                comparison_operator(m)

    @RateLimited(0.5)
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

        if "print_stats" in options.command:
            if not options.gitlab_project:
                print("Requires gitlab project e.g. myname/project")
                exit(0)

            class UserInfo:
                def __init__(self, name):
                    self.name = name
                    self.merges = []
                    self.closed_requests = []
                    self.open_requests = []
                    self.wip_requests = []

                def sort_merge(self, merge):

                    datetime_object = parse_datetime(merge.get('created_at', None))
                    if datetime_object < stime:
                        return
                    if datetime_object > etime:
                        return
                    if "WIP" in merge.get("title", None) and merge.get('state', None) == 'opened':
                        self.wip_requests.append(merge)

                    if merge.get('state', None) == 'opened':
                        self.open_requests.append(merge)

                    if merge.get('state', None) == 'closed':
                        self.closed_requests.append(merge)

            user_info = dict()

            if options.gitlab_stats_start_date and options.gitlab_stats_end_date:
                stime = datetime.strptime(options.gitlab_stats_start_date, "%d/%m/%Y")
                etime = datetime.strptime(options.gitlab_stats_end_date, "%d/%m/%Y")
            else:
                print("Requires time range")
                exit(0)

            def comparison_operator(merge):
                datetime_object = parse_datetime(merge.get("created_at", None))
                if datetime_object < stime:
                    print("Ignoring merge too old!")
                    return
                if datetime_object > etime:
                    print("Ignoring merge too young!")
                    return

                if merge.get("author", None).get("name", None) not in user_info:
                    user_info[merge.get("author", None).get("name", None)] = UserInfo(
                        merge.get("author", None).get("name", None))

                user_info[merge.get("author", None).get("name", None)].sort_merge(merge)

            self.walk_merge_request(options.gitlab_max_size, options.gitlab_token, options.gitlab_server,
                                    comparison_operator)

            to = 0
            tc = 0
            tw = 0
            print("---------------------------------------------------------------------------")
            total_mr = 0
            for u in user_info:
                user = user_info[u]

                to += len(user.open_requests)
                tc += len(user.closed_requests)
                tw += len(user.wip_requests)

            print("Total open requests %d, closed requests %d, wip requests %d" % (to, tc, tw))
            print("Total requests %d" % (to + tc + tw))

            return user_info
