"""
put-node.

adds a node to ODL

parameter:
* ODL IP address
* node IP address
* node name
* netconf port (optional - default is 830)
* netconf user (optional - default is 'cisco')
* netconf pass (optional - default is 'cisco')

uses HTTP PUT with JSON payload
"""

import sys
import os
import requests
import yaml

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

request_template = '''{
  "definition": [
    {
      "name": "%s",
      "address-family": {
        "ipv4": {
          "route-target": {
            "export": [
              {
                "asn-ip": "%s"
              }
            ],
            "import": [
              {
                "asn-ip": "%s"
              }
            ]
          }
        }
      },
      "rd": "%s"
    }
  ]
}'''

def yaml_loader(filepath):
  with open(filepath, "r") as file_descsriptor:
    data = yaml.load(file_descsriptor)
  return data

if __name__ == "__main__":
  fabric = yaml_loader("/Users/kekuhls/Documents/CIS/projects/cvd/DNA/vars_files/ODL_global_fabric_vars.yml")
  for vrf in fabric['vrf']:
      vrf_id = str(vrf['vrf_id']) +':'+ str(vrf['vrf_id'])
      request_body = request_template % (vrf['vrf_name'], vrf_id, vrf_id, vrf_id)
      url = 'http://'+ ODL_SERVER + ':8181/restconf/config/network-topology:network-topology' + \
        '/topology/topology-netconf/node/kevios2/yang-ext:mount/ned:native/vrf/definition/' + vrf['vrf_name']
      print url
      print request_body
      print 'Adding Vrf ' + vrf['vrf_name']
      print requests.put(url, data=request_body, headers=headers,auth=(odl_user, odl_pass))    