#!/usr/bin/env python


import sys
import json
import subprocess
import os


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


# Define a function to silently remove files
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


# Define a function to silently add files
def silentadd(filename):
    try:
        os.mknod(filename)
    except OSError:
        pass


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cpjson = json.load(sys.stdin)
mydict = cpjson["data"]
domainname = mydict["web_vhost_name"]


with open("/etc/userdatadomains.json", "r") as userdatadomains:
    json_parsed_userdata = json.load(userdatadomains)
cpaneluserdata = json_parsed_userdata.get(domainname)
cpaneluser = cpaneluserdata[0]

if not os.path.isfile('/var/cpanel/mgmt_queue/apache_update_no_restart'):
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
    print(("1 nDeploy:WHMTLSAutoSSLtrigger:"+cpaneluser))
else:
    silentadd('/opt/nDeploy/conf/skip_nginx_reload')
    silentadd('/opt/nDeploy/conf/skip_php-fpm_reload')
    silentadd('/opt/nDeploy/conf/skip_tomcat_reload')
    subprocess.call("/opt/nDeploy/scripts/generate_config.py "+cpaneluser, shell=True)
    silentremove('/opt/nDeploy/conf/skip_nginx_reload')
    silentremove('/opt/nDeploy/conf/skip_php-fpm_reload')
    silentremove('/opt/nDeploy/conf/skip_tomcat_reload')
    print(("1 nDeploy:WHMTLSAutoSSLtrigger:DeferReload:"+cpaneluser))
