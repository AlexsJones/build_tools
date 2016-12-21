#! /usr/bin/env python
#################################################################################
#     File Name           :     services/nmap_service.py
#     Created By          :     jonesax
#     Creation Date       :     [2016-12-21 14:20]
#     Last Modified       :     [2016-12-21 15:13]
#     Description         :      
#################################################################################
import nmap
import ipaddress


class nmap_service():

  def additional_options(self, parser):
    parser.add_argument("--command",
        help="nmap COMMAND to execute: unused_ip",
        metavar="COMMAND")
    parser.add_argument("--range",
        help="Please specify the ip range e.g. 10.0.0.1/26")

  def __init__(self):
    print("Started Nmap Service...")
    self.nm = nmap.PortScanner()

  def run(self, options):
    print("Running with options %s" % options)
    if not options.command:
      print("No command given to run...")
      exit(0)
    if "unused_ip" in options.command:
      if not options.range:
        print("Requires an ip range")
      print("Scanning...")
      start_range = options.range
      self.nm.scan(start_range, arguments="-sP")
      hosts = self.nm.all_hosts()
      free_hosts=[]
      for current_pot in list(str(x) for x  in ipaddress.ip_network(start_range).hosts()):
        found=False
        for found_host in hosts:
          if found_host in current_pot:
            found=True

        if not found:
          free_hosts.append(current_pot)

      print("Available hosts ip addresses----------------")
      print("\n".join(str(z) for z in free_hosts))
      print("--------------------------------------------")