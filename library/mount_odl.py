"""
post-node.

adds a node to ODL

parameter:
* ODL IP address
* node IP address
* node name
* netconf port (optional - default is 830)
* netconf user (optional - default is 'cisco')
* netconf pass (optional - default is 'cisco')

uses HTTP POST with JSON payload
"""

import sys
import os
import requests

# set up the request
request_template = '''
{
  "module": [
    {
      "type": "odl-sal-netconf-connector-cfg:sal-netconf-connector",
      "name": "%s",
      "odl-sal-netconf-connector-cfg:address": "%s",
      "odl-sal-netconf-connector-cfg:port": %s,
      "odl-sal-netconf-connector-cfg:username": "%s",
      "odl-sal-netconf-connector-cfg:password": "%s",
      "odl-sal-netconf-connector-cfg:tcp-only": false,
      "odl-sal-netconf-connector-cfg:binding-registry": {
        "type": "opendaylight-md-sal-binding:binding-broker-osgi-registry",
        "name": "binding-osgi-broker"
      },
      "odl-sal-netconf-connector-cfg:between-attempts-timeout-millis": 2000,
      "odl-sal-netconf-connector-cfg:processing-executor": {
         "type": "threadpool:threadpool",
         "name": "global-netconf-processing-executor"
      },
      "odl-sal-netconf-connector-cfg:max-connection-attempts": 0,
      "odl-sal-netconf-connector-cfg:sleep-factor": 1.5,
      "odl-sal-netconf-connector-cfg:client-dispatcher": {
        "type": "odl-netconf-cfg:netconf-client-dispatcher",
        "name": "global-netconf-dispatcher"
      },
      "odl-sal-netconf-connector-cfg:dom-registry": {
        "type": "opendaylight-md-sal-dom:dom-broker-osgi-registry",
        "name": "dom-broker"
      },
      "odl-sal-netconf-connector-cfg:event-executor": {
        "type": "netty:netty-event-executor",
        "name": "global-event-executor"
      },
      "odl-sal-netconf-connector-cfg:connection-timeout-millis": 20000
    }
  ]
}
'''
devices = [
            {'address':'172.26.170.83',
             'name':'kevios2',
             'port':830,
             'username':'admin',
             'password':'c1sco123'
            },
            {'address':'172.26.170.84',
             'name':'kevios3',
             'port':830,
             'username':'admin',
             'password':'c1sco123'
            }
          ]
ODL_SERVER = '10.203.27.104'
headers = {'Content-Type': 'application/json'}
odl_user = os.environ.get('ODL_USER', 'admin')
odl_pass = os.environ.get('ODL_PASS', 'admin')

for item in devices:
  url = 'http://' + ODL_SERVER + \
      ':8181/restconf/config/network-topology:network-topology' + \
      '/topology/topology-netconf/node/controller-config' + \
      '/yang-ext:mount/config:modules'
  request_body = request_template % (item['name'], item['address'],
                                   item['port'], item['username'], item['password'])
  print 'adding ' + item['name']
  print requests.post(url, data=request_body, headers=headers,
                   auth=(odl_user, odl_pass))
