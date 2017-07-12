#!/usr/bin/env python

import subprocess
import json
import os
import jinja2
import codecs
import yaml


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


iplist_json = json.loads(subprocess.Popen(['/usr/local/cpanel/bin/whmapi1', 'listips', '--output=json'], stdout=subprocess.PIPE).communicate()[0])
data_dict = iplist_json.get('data')
ip_list = data_dict.get('ip')
cpanel_ip_list = []
for myip in ip_list:
    theip = myip.get('ip')
    cpanel_ip_list.append(theip)
    mainaddr_status = myip.get('mainaddr')
    if mainaddr_status == 1:
        mainip = theip
if os.path.isfile('/var/cpanel/ssl/cpanel/mycpanel.pem'):
    cpsrvdsslfile = '/var/cpanel/ssl/cpanel/mycpanel.pem'
else:
    cpsrvdsslfile = '/var/cpanel/ssl/cpanel/cpanel.pem'
slaveiplist = []
if os.path.isfile(installation_path+"/conf/ndeploy_cluster.yaml"):  # get the cluster ipmap
    cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
    cluster_data_yaml = open(cluster_config_file, 'r')
    cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    cluster_data_yaml.close()
    serverlist = cluster_data_yaml_parsed.keys()
    for slaveserver in serverlist:
        server_dict = cluster_data_yaml_parsed.get(slaveserver)
        ipmap_dict = server_dict.get('ipmap')
        theiplist = ipmap_dict.values()
        slaveiplist = slaveiplist + theiplist
# Initiate Jinja2 templateEnv
templateLoader = jinja2.FileSystemLoader(installation_path + "/conf/")
templateEnv = jinja2.Environment(loader=templateLoader)
templateVars = {"CPIPLIST": cpanel_ip_list,
                "MAINIP": mainip,
                "CPSRVDSSL": cpsrvdsslfile,
                "SLAVEIPLIST": slaveiplist
                }
# Generate default_server.conf
default_server_template = templateEnv.get_template('default_server.conf.j2')
default_server_config = default_server_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/default_server.conf', 'w', 'utf-8') as default_server_config_file:
    default_server_config_file.write(default_server_config)
# Generate proxy_subdomain.conf
proxy_subdomain_template = templateEnv.get_template('proxy_subdomain.conf.j2')
proxy_subdomain_config = proxy_subdomain_template.render(templateVars)
with codecs.open('/etc/nginx/conf.d/proxy_subdomain.conf', 'w', 'utf-8') as proxy_subdomain_config_file:
    proxy_subdomain_config_file.write(proxy_subdomain_config)
