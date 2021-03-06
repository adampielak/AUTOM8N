#!/usr/bin/python

import cgitb
import cgi
import psutil
import platform
import signal
import os
from commoninclude import print_simple_header, print_simple_footer, terminal_call, print_success, print_forbidden


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()

form = cgi.FieldStorage()

def sighupnginx():
    for myprocess in psutil.process_iter():

        # Workaround for Python 2.6
        if platform.python_version().startswith('2.6'):
            mycmdline = myprocess.cmdline
        else:
            mycmdline = myprocess.cmdline()
        if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
            nginxpid = myprocess.pid
            os.kill(nginxpid, signal.SIGHUP)

print_simple_header()

if form.getvalue('ddos'):
    if form.getvalue('ddos') == 'enable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.disabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.enabled")
        sighupnginx()

        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.disabled /etc/nginx/conf.d/dos_mitigate_systemwide.enabled && nginx -s reload\"', 'Enabling Nginx DDOS mitigation cluster-wide...', 'Nginx DDOS mitigation enabled cluster-wide!')
            print_success('Nginx DDOS mitigation is now enabled cluster-wide!')
        else:
            print_success('Nginx DDOS mitigation is now enabled!')

    elif form.getvalue('ddos') == 'disable':
        os.rename("/etc/nginx/conf.d/dos_mitigate_systemwide.enabled", "/etc/nginx/conf.d/dos_mitigate_systemwide.disabled")
        sighupnginx()

        # Do this clusterwide if we are on a cluster
        if os.path.isfile(cluster_config_file):
            terminal_call('ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"mv /etc/nginx/conf.d/dos_mitigate_systemwide.enabled /etc/nginx/conf.d/dos_mitigate_systemwide.disabled && nginx -s reload\"', 'Disabling Nginx DDOS mitigation cluster-wide...', 'Nginx DDOS mitigation disabled cluster-wide!')
            print_success('Nginx DDOS mitigation is now disabled cluster-wide!')
        else:
            print_success('Nginx DDOS mitigation is now disabled!')

else:
    print_forbidden()

print_simple_footer()
