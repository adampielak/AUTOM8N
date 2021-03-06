#!/usr/bin/python

import cgi
import cgitb
import yaml
from commoninclude import print_simple_header, print_simple_footer, print_success, print_forbidden


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Production"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('restore_defaults') == 'enabled':
    yaml_parsed_restore_ndeploy_control_conf = {'ndeploy_theme_color': 'light', 'primary_color': '#121212', 'logo_url': 'None', 'app_email': 'None', 'cpanel_documentation_link': 'None', 'whm_documentation_link': 'None'}
    with open(ndeploy_control_file, 'w') as ndeploy_control_conf:
        yaml.dump(yaml_parsed_restore_ndeploy_control_conf, ndeploy_control_conf, default_flow_style=False)

    print_success('The nDeploy aesthetics configuration has been restored to defaults.')
else:
    print_forbidden()

print_simple_footer()
